from tools.collect_timeline import collect_timeline
from tools.analyze_startup import generate_startup_report

class StartupAgent:
    def run(self, step, inputs):
        """
        Executes a step in the startup analysis workflow.
        """
        if step == "收集启动数据":
            # The default command in collect_timeline is sufficient for startup analysis
            # as it includes --trace-startup.
            print("[StartupAgent] 开始收集启动性能数据...")
            collect_timeline()
            return {"status": "success", "output_file": "timeline.json"}
            
        elif step == "分析启动耗时":
            timeline_file = inputs.get("timeline_file", "timeline.json")
            print(f"[StartupAgent] 开始分析文件: {timeline_file}")
            analysis_result = generate_startup_report(timeline_file)
            # 返回分析结果，供 Gemini Agent 生成最终报告
            return {"startup_analysis": analysis_result}