import json

def analyze_leaks():
    try:
        with open("heap.json") as f:
            data = json.load(f)
        leaks = [obj for obj in data.get("objects", []) if "Leak" in obj.get("type", "")]
        if leaks:
            print(f"发现 {len(leaks)} 个可能的内存泄漏对象:")
            for leak in leaks[:5]:
                print(f" - {leak['type']}")
        else:
            print("✅ 未发现明显内存泄漏")
    except Exception as e:
        print("分析内存泄漏失败:", e)