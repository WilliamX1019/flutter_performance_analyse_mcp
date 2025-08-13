import os

def consolidate_reports(output_dir="output"):
    """
    Reads all .md report files from the output directory and consolidates them into a single string.
    """
    print("[OptimizerAgent] 开始整合所有性能分析报告...")
    consolidated_content = []
    
    if not os.path.isdir(output_dir):
        print(f"[OptimizerAgent] 警告: 输出目录 '{output_dir}' 不存在。请先运行至少一个分析工作流。")
        return ""

    # 动态查找 output 目录下的所有 .md 文件
    for filename in sorted(os.listdir(output_dir)):
        # 只读取分析报告，排除最终的综合报告自身
        if not filename.endswith(".md") or filename == "comprehensive_optimization_plan.md":
            continue

        path = os.path.join(output_dir, filename)
        print(f"[OptimizerAgent] 读取报告: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            # 为每个报告添加标题，方便AI区分
            consolidated_content.append(f"--- 分析报告: {filename} ---\n\n{f.read()}")
            
    if not consolidated_content:
        print("[OptimizerAgent] 错误: 在 'output' 目录中未找到任何报告文件。请先运行分析工作流。")
        return ""
        
    final_report_context = "\n\n".join(consolidated_content)
    print("[OptimizerAgent] 所有报告整合完毕。")
    return final_report_context