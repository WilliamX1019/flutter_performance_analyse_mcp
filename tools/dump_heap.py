import os

def dump_heap():
    print("[LeakAgent] 导出 Heap Snapshot...")
    # 示例命令，实际根据项目修改
    os.system("flutter pub global run devtools dump_heap --output heap.json")
    print("[LeakAgent] heap.json 已生成")