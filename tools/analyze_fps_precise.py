#该脚本适用于 Flutter timeline.json（Profile 模式采集，包含 traceEvents）
# 用于分析 Flutter 应用的帧率热点，识别出持续时间超过 16.6 ms 的帧事件。
# 直接运行脚本，并传入 timeline 文件路径即可生成报告：
# python analyze_fps_precise.py timeline.json
# 
# 可以根据你实际 timeline.json 里调用栈格式，调整 extract_call_stack 里的正则表达式
	# •	能识别慢帧（超过阈值的帧）
	# •	通过解析真实调用栈，定位具体导致慢帧的函数名、文件和代码行
	# •	报告中包含调用栈列表，明确热点代码位置
	# •	方便开发者直接定位性能瓶颈代码点
import json
import os
import re
import sys

def load_timeline(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_slow_frames(timeline, threshold_ms=16.6):
    slow_frames = []
    for event in timeline.get("traceEvents", []):
        # 过滤 Flutter 帧事件，通常名为 "Frame" 且类型为持续事件"X"
        if event.get("name") == "Frame" and event.get("ph") == "X":
            dur_ms = event.get("dur", 0) / 1000
            if dur_ms > threshold_ms:
                slow_frames.append(event)
    return slow_frames

def extract_call_stack(frame_event):
    stack = []
    args = frame_event.get("args", {})
    # 通常调用栈在 args.stackTrace，格式是字符串
    stack_trace_str = args.get("stackTrace", "")

    if stack_trace_str:
        # 逐行解析调用栈，示例格式：
        # #0      Widget.build (package:yourapp/widgets.dart:42:10)
        for line in stack_trace_str.splitlines():
            m = re.match(r"#\d+\s+(\S+)\s+\(([^:]+):(\d+):(\d+)\)", line)
            if m:
                func, file, line_no, col_no = m.groups()
                stack.append({
                    "func": func,
                    "file": file,
                    "line": int(line_no),
                    "col": int(col_no)
                })
    if not stack:
        # fallback 无调用栈信息时填充
        stack.append({"func": "unknown", "file": "unknown", "line": 0, "col": 0})
    return stack

def generate_report(frames):
    report_lines = ["# 帧率热点分析报告\n"]
    if not frames:
        report_lines.append("未发现明显慢帧。\n")
        return "\n".join(report_lines)

    for i, frame in enumerate(frames, 1):
        dur_ms = frame.get("dur", 0) / 1000
        report_lines.append(f"## 第 {i} 个慢帧: 持续时间 {dur_ms:.2f} ms\n")
        stack = extract_call_stack(frame)
        report_lines.append("调用栈（从热点到主入口）：\n")
        for call in stack:
            report_lines.append(f"- 函数 `{call['func']}` 在 `{call['file']}` 文件第 {call['line']} 行，列 {call['col']}")
        report_lines.append("\n优化建议：\n")
        top_func = stack[0]
        report_lines.append(f"- 请重点检查 `{top_func['file']}` 文件中第 {top_func['line']} 行的 `{top_func['func']}` 函数，避免过度 rebuild 或复杂布局。\n")
        report_lines.append(f"```dart\n// 示例代码片段\nWidget build(BuildContext context) {{\n  // TODO: 优化此处性能瓶颈\n}}\n```\n")
    return "\n".join(report_lines)

def analyze_fps_precise(timeline_file):
    print(f"[AnalyzeFPS] 正在加载 Timeline 文件: {timeline_file}")
    timeline = load_timeline(timeline_file)
    print("[AnalyzeFPS] 查找慢帧中...")
    slow_frames = find_slow_frames(timeline)
    print(f"[AnalyzeFPS] 找到 {len(slow_frames)} 个慢帧")

    print("[AnalyzeFPS] 生成报告中...")
    report = generate_report(slow_frames)

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "fps_precise_report.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[AnalyzeFPS] 精确帧率分析报告已生成：{output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_fps_precise.py timeline.json")
        sys.exit(1)
    analyze_fps_precise(sys.argv[1])