import os
import subprocess

def dump_heap():
    print("[LeakAgent] 导出 Heap Snapshot...")
    # 使用 subprocess.run 替代 os.system，以获得更好的错误处理和控制
    command = ["flutter", "pub", "global", "run", "devtools", "dump_heap", "--output", "heap.json"]
    result = subprocess.run(command, shell=False, check=False)
    
    if result.returncode == 0:
        print("[LeakAgent] heap.json 已生成")
    else:
        print(f"[LeakAgent] 导出 Heap Snapshot 失败，返回码: {result.returncode}")
        print(f"[LeakAgent] 错误信息: {result.stderr}")