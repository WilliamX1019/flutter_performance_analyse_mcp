import os

def consolidate_reports(output_dir="output"):
    """
    Reads all .md report files from the output directory and consolidates them into a single string.
    """
    print("[OptimizerAgent] 开始整合所有性能分析报告...")
    consolidated_content = []
    # 定义需要查找的报告文件
    report_files = [
        "fps_precise_report.md",
        "leak_precise_report.md",
        "startup_report.md"
    ]
    
    for filename in report_files:
        path = os.path.join(output_dir, filename)
        if os.path.exists(path):
            print(f"[OptimizerAgent] 读取报告: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                # 为每个报告添加标题，方便AI区分
                consolidated_content.append(f"--- 分析报告: {filename} ---\n\n{f.read()}")
        else:
            print(f"[OptimizerAgent] 警告: 未找到报告文件 {path}，将跳过。请确保已运行过对应的分析工作流。")
            
    if not consolidated_content:
        print("[OptimizerAgent] 错误: 在 'output' 目录中未找到任何报告文件。请先运行分析工作流。")
        return ""
        
    final_report_context = "\n\n".join(consolidated_content)
    print("[OptimizerAgent] 所有报告整合完毕。")
    return final_report_context
