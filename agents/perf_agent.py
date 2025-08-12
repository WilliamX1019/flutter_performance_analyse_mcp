from tools.collect_timeline import collect_timeline
from tools.analyze_fps import analyze_fps ## 简单分析脚本
from tools.analyze_fps_precise import analyze_fps_precise ## 精确分析脚本

class PerfAgent:
    def run(self, step, inputs):
        if step == "收集帧率数据":
            collect_timeline(inputs["command"])
        elif step == "分析帧率曲线":
            timeline_file = inputs.get("timeline_file", "timeline.json")
            analyze_fps_precise(timeline_file)