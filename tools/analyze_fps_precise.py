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

def find_hotspots_in_frame(frame_event, all_events, top_n=5):
    """
    Finds the longest-running events (hotspots) that occurred within a given slow frame.
    """
    frame_start = frame_event.get("ts", 0)
    frame_end = frame_start + frame_event.get("dur", 0)
    frame_tid = frame_event.get("tid")

    hotspots = []
    for event in all_events:
        # Find "complete" events ('X' phase) on the same thread that are fully contained within the frame's duration.
        if (event.get("ph") == "X" and
            event.get("tid") == frame_tid and
            event.get("ts", 0) >= frame_start and
            (event.get("ts", 0) + event.get("dur", 0)) <= frame_end and
            event != frame_event): # Exclude the frame event itself
            hotspots.append(event)
    
    # Sort by duration in descending order and return the top N
    return sorted(hotspots, key=lambda x: x.get("dur", 0), reverse=True)[:top_n]

def generate_report(slow_frames, all_events):
    report_lines = ["# 帧率热点分析报告\n"]
    if not slow_frames:
        report_lines.append("未发现明显慢帧。\n")
        return "\n".join(report_lines)

    for i, frame in enumerate(slow_frames, 1):
        dur_ms = frame.get("dur", 0) / 1000
        report_lines.append(f"## 第 {i} 个慢帧: 持续时间 {dur_ms:.2f} ms\n")
        
        hotspots = find_hotspots_in_frame(frame, all_events)
        
        if hotspots:
            report_lines.append("该帧内的主要耗时操作 (热点):\n")
            for spot in hotspots:
                spot_dur_ms = spot.get("dur", 0) / 1000
                spot_name = spot.get("name", "unknown event")
                report_lines.append(f"- **{spot_name}**: 耗时 `{spot_dur_ms:.2f} ms`")
            
            top_hotspot = hotspots[0]
            report_lines.append("\n**优化建议**:\n")
            report_lines.append(f"- 请重点关注耗时最长的操作 **`{top_hotspot.get('name')}`**。它占据了该慢帧的大部分时间，是优化的首要目标。请检查相关的 Widget 是否可以被设为 `const`，或者其 `build` 方法是否可以被优化以减少计算量。")
        else:
            report_lines.append("未能在此慢帧内定位到具体的耗时子事件。问题可能出在多个小任务的累积效应上。")
        report_lines.append("\n---\n")
    return "\n".join(report_lines)

def analyze_fps_precise(timeline_file):
    print(f"[AnalyzeFPS] 正在加载 Timeline 文件: {timeline_file}")
    timeline = load_timeline(timeline_file)
    all_events = timeline.get("traceEvents", [])
    print("[AnalyzeFPS] 查找慢帧中...")
    slow_frames = find_slow_frames(timeline) # This function still works as intended
    print(f"[AnalyzeFPS] 找到 {len(slow_frames)} 个慢帧")
    print("[AnalyzeFPS] 生成报告中...")
    report = generate_report(slow_frames, all_events)
    print("[AnalyzeFPS] 精确帧率分析报告已生成。")
    return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_fps_precise.py timeline.json")
        sys.exit(1)
    analyze_fps_precise(sys.argv[1])