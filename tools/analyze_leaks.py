import json
import os
import sys
from collections import Counter

# A list of class names that are common sources of memory leaks in Flutter.
# This list can be expanded based on project specifics.
SUSPICIOUS_CLASSES = [
    "_Listener",
    "StreamSubscription",
    "Timer",
    "AnimationController",
    "ChangeNotifier",
    "ScrollController",
    "TextEditingController",
]

def load_heap_snapshot(path):
    """Loads the heap snapshot JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_heap(heap_data):
    """
    Analyzes the heap snapshot to find potential memory leaks.
    It counts instances of all classes and flags suspicious ones.
    """
    graph = heap_data.get("graph", {})
    vertices = graph.get("vertices", [])
    
    if not vertices:
        return "无法分析内存：Heap Snapshot 中未找到对象数据 (vertices)。"

    # 1. 按实例数量分析
    class_counts = Counter(v.get("class_name") for v in vertices if v.get("class_name"))
    leaked_candidates = {cls: count for cls, count in class_counts.items() if cls in SUSPICIOUS_CLASSES and count > 0}
    common_safe_classes = {'String', 'int', 'double', '_List', '_Map', 'bool'}
    top_objects = {cls: count for cls, count in class_counts.most_common(10) if cls not in common_safe_classes and not cls.startswith('_')}

    # 2. 按保留大小分析 (新增)
    # 按类名聚合总保留大小
    class_retained_size = Counter()
    for v in vertices:
        class_name = v.get("class_name")
        if class_name and class_name not in common_safe_classes and not class_name.startswith('_'):
            class_retained_size[class_name] += v.get("retained_size_bytes", 0)
    
    top_retained_size_objects = class_retained_size.most_common(5)

    report_lines = []
    if not leaked_candidates and not top_objects and not top_retained_size_objects:
        report_lines.append("未发现明显的内存泄漏嫌疑对象。应用内存状态看起来比较健康。")
    
    if leaked_candidates:
        report_lines.append("### 发现潜在的泄漏嫌疑对象\n")
        report_lines.append("以下类型的对象通常与资源未释放有关，请重点检查：\n")
        for cls, count in sorted(leaked_candidates.items()):
            report_lines.append(f"- **{cls}**: 发现了 `{count}` 个实例。请确保相关的监听器、控制器或订阅已在 `dispose` 方法中被正确释放。")
        report_lines.append("\n")

    if top_objects:
        report_lines.append("### 实例数量最多的对象类型\n")
        report_lines.append("以下是应用中实例数量最多的对象类型，可能表示存在内存使用不当的问题：\n")
        for cls, count in top_objects.items():
            report_lines.append(f"- **{cls}**: 发现了 `{count}` 个实例。")
        report_lines.append("\n")

    if top_retained_size_objects:
        report_lines.append("### 总保留内存最多的对象类型\n")
        report_lines.append("以下是应用中占用总内存最多的对象类型，可能是内存优化的关键点：\n")
        for cls, size_bytes in top_retained_size_objects:
            size_kb = size_bytes / 1024
            report_lines.append(f"- **{cls}**: 总计占用 `{size_kb:.2f} KB` 内存。")
        report_lines.append("\n")
        
    return "\n".join(report_lines)

def generate_leak_report(heap_file):
    """Loads heap data, analyzes it, and returns the analysis string."""
    print(f"[AnalyzeLeaks] 正在加载 Heap Snapshot 文件: {heap_file}")
    if not os.path.exists(heap_file):
        return f"错误：找不到 Heap Snapshot 文件 '{heap_file}'。请先运行 '导出 Heap Snapshot' 步骤。"
    heap_data = load_heap_snapshot(heap_file)
    print("[AnalyzeLeaks] 分析内存对象中...")
    analysis_result = analyze_heap(heap_data)
    print("[AnalyzeLeaks] 内存分析完成。")
    return analysis_result