	# •	解析 Dart/Flutter Heap Snapshot（通常是 JSON 格式，具体格式视工具不同会有差异）
	# •	找出疑似泄漏对象（比如长时间存在且引用链复杂的对象）
	# •	提取创建该对象的调用栈（如果有的话）
	# •	映射到具体 Dart 文件名、行号、函数名
	# •	生成带具体代码定位的 Markdown 报告

# 运行脚本 
# python tools/analyze_leak_precise.py heap_snapshot.json
# 可以根据真实堆栈 heap snapshot 格式 定制 这个脚本

	# •	精确找出占用较大内存的泄漏对象
	# •	解析对象创建时的调用栈，定位泄漏起源的具体源码位置
	# •	报告中包含对象类型、保留大小、调用栈及代码行号
	# •	让开发者准确知道哪段代码可能导致内存泄漏

import json
import os
import re
import sys

def load_heap_snapshot(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_leaking_objects(snapshot, retention_threshold=1000000):
    """
    示例查找疑似泄漏对象：
    retention_threshold 是示例的保留大小阈值（字节）
    实际根据快照字段调整
    """
    leaks = []
    # 示例字段，实际快照格式需要你确认
    for obj in snapshot.get("objects", []):
        retained_size = obj.get("retainedSize", 0)
        if retained_size > retention_threshold:
            leaks.append(obj)
    return leaks

def extract_creation_stack(leak_obj):
    """
    从泄漏对象中提取创建调用栈，假设在字段 creationStack
    格式类似：
    [
      "#0 SomeClass.someMethod (package:yourapp/src/file.dart:123:45)",
      ...
    ]
    """
    stack = []
    stack_trace_list = leak_obj.get("creationStack", [])
    if stack_trace_list:
        for line in stack_trace_list:
            m = re.match(r"#\d+\s+(\S+)\s+\(([^:]+):(\d+):(\d+)\)", line)
            if m:
                func, file, line_no, col_no = m.groups()
                stack.append({
                    "func": func,
                    "file": file,
                    "line": int(line_no),
                    "col": int(col_no)
                })
    else:
        stack.append({"func": "unknown", "file": "unknown", "line": 0, "col": 0})
    return stack

def generate_report(leaks):
    report_lines = ["# 内存泄漏精确分析报告\n"]
    if not leaks:
        report_lines.append("未发现明显内存泄漏对象。\n")
        return "\n".join(report_lines)

    for i, leak in enumerate(leaks, 1):
        size = leak.get("retainedSize", 0)
        type_name = leak.get("type", "unknown")
        report_lines.append(f"## 第 {i} 个泄漏对象: 类型 `{type_name}`，保留大小 {size} 字节\n")
        stack = extract_creation_stack(leak)
        report_lines.append("创建调用栈（从创建点到主入口）：\n")
        for call in stack:
            report_lines.append(f"- 函数 `{call['func']}` 在 `{call['file']}` 文件第 {call['line']} 行，列 {call['col']}")
        report_lines.append("\n优化建议：\n")
        top_func = stack[0]
        report_lines.append(f"- 请重点检查 `{top_func['file']}` 文件中第 {top_func['line']} 行的 `{top_func['func']}` 函数，确认是否有未释放的资源或多余引用。\n")
        report_lines.append(f"```dart\n// 示例代码片段\nvoid dispose() {{\n  // TODO: 确保清理相关资源，防止内存泄漏\n}}\n```\n")
    return "\n".join(report_lines)

def analyze_leak_precise(heap_snapshot_file):
    print(f"[AnalyzeLeak] 正在加载堆快照文件: {heap_snapshot_file}")
    snapshot = load_heap_snapshot(heap_snapshot_file)
    print("[AnalyzeLeak] 查找疑似泄漏对象中...")
    leaks = find_leaking_objects(snapshot)
    print(f"[AnalyzeLeak] 找到 {len(leaks)} 个疑似泄漏对象")

    print("[AnalyzeLeak] 生成报告中...")
    report = generate_report(leaks)

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "leak_precise_report.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[AnalyzeLeak] 精确内存泄漏分析报告已生成：{output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_leak_precise.py heap_snapshot.json")
        sys.exit(1)
    analyze_leak_precise(sys.argv[1])