import json

def analyze_fps(timeline_file):
    with open(timeline_file) as f:
        data = json.load(f)
    fps_events = [e for e in data["traceEvents"] if "Frame" in e.get("name", "")]
    if len(fps_events) < 2:
        print("⚠️ 采集的帧数据太少，无法分析")
        return
    avg_fps = len(fps_events) / max(1, (fps_events[-1]["ts"] - fps_events[0]["ts"]) / 1e6)
    print(f"平均 FPS: {avg_fps:.2f}")
    if avg_fps < 55:
        print("⚠️ FPS 偏低，建议优化绘制或减少 build 次数")