from tools.collect_timeline import collect_timeline
from tools.analyze_fps_precise import analyze_fps_precise ## 精确分析脚本

class PerfAgent:
    def run(self, step, inputs):
        if step == "收集帧率数据":
            # 从输入中获取渲染器类型，默认为 'impeller'
            renderer = inputs.get('renderer', 'impeller')
            collect_timeline(renderer=renderer)
            return {"status": "success", "output_file": "timeline.json"}

        elif step == "分析帧率曲线":
            timeline_file = inputs.get("timeline_file", "timeline.json")
            analysis_result = analyze_fps_precise(timeline_file)
            return {"fps_analysis": analysis_result}