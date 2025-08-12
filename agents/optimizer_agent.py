from tools.consolidate_reports import consolidate_reports

class OptimizerAgent:
    def run(self, step, inputs):
        if step == "整合分析报告":
            report_context = consolidate_reports()
            # 将整合后的报告内容作为输出，传递给下一步
            return {"consolidated_reports": report_context}