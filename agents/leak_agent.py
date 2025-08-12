from tools.dump_heap import dump_heap
from tools.analyze_leaks import generate_leak_report

class LeakAgent:
    def run(self, step, inputs):
        """
        Executes a step in the memory leak analysis workflow.
        """
        if step == "导出 Heap Snapshot":
            print("[LeakAgent] 开始导出 Heap Snapshot...")
            dump_heap()
            return {"status": "success", "output_file": "heap.json"}
            
        elif step == "分析内存泄漏":
            heap_file = inputs.get("heap_snapshot_file", "heap.json")
            print(f"[LeakAgent] 开始分析文件: {heap_file}")
            analysis_result = generate_leak_report(heap_file)
            return {"leak_analysis": analysis_result}