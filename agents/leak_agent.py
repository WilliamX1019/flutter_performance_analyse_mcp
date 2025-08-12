from tools.dump_heap import dump_heap
from tools.analyze_leak_precise import analyze_leak_precise

class LeakAgent:
    def run(self, step, inputs):
        if step == "导出 Heap Snapshot":
            # 假设dump_heap会输出固定路径文件，比如 'heap.json'
            dump_heap()  
        elif step == "分析内存泄漏":
            # 从inputs中拿heap快照文件路径，默认用dump_heap的输出路径
            heap_snapshot_file = inputs.get("heap_snapshot_file", "heap.json")
            analyze_leak_precise(heap_snapshot_file)