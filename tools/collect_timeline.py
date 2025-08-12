import subprocess
import os

def collect_timeline(command=None):
    """
    运行 Flutter 命令采集性能 Timeline，默认使用带参数的 profile 模式生成 timeline.json
    """
    # 如果外部没传命令，使用带 trace 参数的默认命令
    if not command:
        # 使用列表形式的命令更安全，避免 shell 注入
        command_list = [
            "flutter", "run", "--profile",
            "--trace-skia", "--trace-startup",
            "--timeline-startup", "--write-skia-profile", "timeline.json"
        ]

    print("[PerfAgent] 正在运行 Flutter 应用并收集 Timeline...")
    # 确保在 Flutter 项目根目录执行
    cwd = os.getcwd()
    print(f"[PerfAgent] 当前工作目录: {cwd}")
    result = subprocess.run(command_list, shell=False, check=False) # 推荐使用 shell=False
    if result.returncode == 0:
        print(f"[PerfAgent] Timeline 数据已生成: {os.path.join(cwd, 'timeline.json')}")
    else:
        print(f"[PerfAgent] Flutter 命令执行失败，返回码: {result.returncode}")