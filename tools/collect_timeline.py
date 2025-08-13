import subprocess
import os

def collect_timeline(renderer='impeller'):
    """
    运行 Flutter 命令采集性能 Timeline，并根据指定的渲染后端 (impeller/skia) 使用不同的追踪参数。
    """
    print(f"[TimelineCollector] 准备为 {renderer.upper()} 渲染后端收集性能数据...")

    # 基础命令
    command_list = ["flutter", "run", "--profile", "--timeline-startup"]

    # 根据渲染后端添加特定的追踪标志
    if renderer == 'impeller':
        command_list.extend(["--trace-impeller", "--no-enable-skia"]) # 明确使用 Impeller
    elif renderer == 'skia':
        command_list.extend(["--trace-skia", "--no-enable-impeller"]) # 明确使用 Skia
    else:
        print(f"[TimelineCollector] 警告: 未知的渲染后端 '{renderer}'。将使用默认追踪参数。")

    # 所有追踪数据都输出到 timeline.json
    command_list.extend(["--write-skia-profile", "timeline.json"])

    print(f"[TimelineCollector] 正在运行命令: {' '.join(command_list)}")

    # 确保在 Flutter 项目根目录执行
    cwd = os.getcwd()
    print(f"[TimelineCollector] 当前工作目录: {cwd}")
    result = subprocess.run(command_list, shell=False, check=False) # 推荐使用 shell=False
    if result.returncode == 0:
        print(f"[TimelineCollector] Timeline 数据已生成: {os.path.join(cwd, 'timeline.json')}")
    else:
        print(f"[TimelineCollector] Flutter 命令执行失败，返回码: {result.returncode}")