import json
import os
import sys

def load_timeline(path):
    """Loads the timeline JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_startup_time(timeline):
    """
    Analyzes the startup time from Flutter's timeline events.
    It breaks down the startup into: Engine Loading, Framework Init, and First Frame Render.
    """
    trace_events = timeline.get("traceEvents", [])
    
    events = {}

    # Find key milestone events. We only capture the first occurrence.
    for event in trace_events:
        name = event.get("name")
        phase = event.get("ph")
        
        if name == "AppStart" and phase == "i" and "AppStart" not in events:
            events["AppStart"] = event
        elif name == "EngineEnter" and phase == "i" and "EngineEnter" not in events:
            events["EngineEnter"] = event
        elif name == "FrameworkInit" and phase == "i" and "FrameworkInit" not in events:
            events["FrameworkInit"] = event
        elif name == "Frame" and phase == "X" and "FirstFrame" not in events:
            # Ensure this is the first frame after AppStart
            if "AppStart" in events and event.get("ts") > events["AppStart"].get("ts"):
                events["FirstFrame"] = event

    # Check if we have all necessary events for a detailed breakdown
    required_events = ["AppStart", "EngineEnter", "FrameworkInit", "FirstFrame"]
    missing_events = [e for e in required_events if e not in events]
    if missing_events:
        return None, f"无法进行详细分析：缺少关键启动事件: {', '.join(missing_events)}。"

    # Get timestamps (in microseconds)
    ts_app_start = events["AppStart"]["ts"]
    ts_engine_enter = events["EngineEnter"]["ts"]
    ts_framework_init = events["FrameworkInit"]["ts"]
    ts_first_frame_end = events["FirstFrame"]["ts"] + events["FirstFrame"]["dur"]
    
    # Calculate durations (in milliseconds)
    dur_engine_init = (ts_engine_enter - ts_app_start) / 1000.0
    dur_framework_init = (ts_framework_init - ts_engine_enter) / 1000.0
    dur_first_frame = (ts_first_frame_end - ts_framework_init) / 1000.0
    dur_total = (ts_first_frame_end - ts_app_start) / 1000.0
    
    analysis_result = (
        f"应用启动到首帧渲染完成的总耗时为: **{dur_total:.2f} ms**。\n\n"
        "这是一个关键的性能指标，通常被称为“Time to First Frame”。下面是详细的耗时分解：\n\n"
        f"- **原生代码启动 & Flutter 引擎加载**: `{dur_engine_init:.2f} ms`\n"
        f"  - *这是从应用进程开始到 Flutter 引擎准备好执行 Dart 代码的时间。*\n"
        f"- **Dart Framework 初始化**: `{dur_framework_init:.2f} ms`\n"
        f"  - *这是 Flutter 框架自身初始化（包括 `runApp()` 调用之前的部分）所需的时间。*\n"
        f"- **首帧构建与渲染**: `{dur_first_frame:.2f} ms`\n"
        f"  - *这是从 `runApp()` 开始到第一帧完全显示在屏幕上的时间，包含了 Widget 构建、布局和绘制。*\n"
    )
    
    return dur_total, analysis_result

def generate_startup_report(timeline_file):
    """Loads data, analyzes it, and returns the core analysis string."""
    print(f"[AnalyzeStartup] 正在加载 Timeline 文件: {timeline_file}")
    timeline = load_timeline(timeline_file)
    
    print("[AnalyzeStartup] 分析启动时间中...")
    duration, analysis = analyze_startup_time(timeline)
    print(f"[AnalyzeStartup] 分析完成，启动耗时: {duration:.2f} ms" if duration else "[AnalyzeStartup] 分析失败")
    return analysis

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_startup.py timeline.json")
        sys.exit(1)
    report = generate_startup_report(sys.argv[1])
    print("\n--- 分析结果 ---\n")
    print(report)