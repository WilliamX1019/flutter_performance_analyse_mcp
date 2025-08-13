from tools.analyze_package_size import analyze_package_size

class PackageSizeAgent:
    def run(self, step, inputs):
        """
        执行应用包大小分析工作流中的一个步骤。
        """
        if step == "分析应用包大小":
            # 从输入中获取平台类型，默认为 'apk'
            platform = inputs.get('platform', 'apk')
            analysis_result = analyze_package_size(platform=platform)
            # 返回分析结果给下一步
            return {"package_size_analysis": analysis_result}
