from tools.collect_timeline import collect_timeline
from tools.analyze_fps_precise import analyze_fps_precise ## 精确分析脚本

class PerfAgent:
    def run(self, step, inputs):
        if step == "收集帧率数据":
            # The default command in collect_timeline is fine for FPS analysis.
            print("[PerfAgent] 开始收集帧率性能数据...")
            collect_timeline()
            return {"status": "success", "output_file": "timeline.json"}

        elif step == "分析帧率曲线":
            timeline_file = inputs.get("timeline_file", "timeline.json")
            analysis_result = analyze_fps_precise(timeline_file)
            return {"fps_analysis": analysis_result}