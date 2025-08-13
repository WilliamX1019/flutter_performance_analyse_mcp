from tools.collect_timeline import collect_timeline
from tools.analyze_startup import generate_startup_report

class StartupAgent:
    def run(self, step, inputs):
        """
        Executes a step in the startup analysis workflow.
        """
        if step == "收集启动数据":
            # 从输入中获取渲染器类型，默认为 'impeller'
            renderer = inputs.get('renderer', 'impeller')
            collect_timeline(renderer=renderer)
            return {"status": "success", "output_file": "timeline.json"}
            
        elif step == "分析启动耗时":
            timeline_file = inputs.get("timeline_file", "timeline.json")
            print(f"[StartupAgent] 开始分析文件: {timeline_file}")
            analysis_result = generate_startup_report(timeline_file)
            # 返回分析结果，供 Gemini Agent 生成最终报告
            return {"startup_analysis": analysis_result}