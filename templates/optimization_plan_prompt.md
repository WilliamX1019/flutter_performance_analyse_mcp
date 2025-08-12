# 任务：生成 Flutter 应用综合性能优化方案

## 背景
你是一位资深的 Flutter 性能优化专家。你收到了以下几份由自动化工具生成的性能分析报告。你的任务是基于这些报告，为开发团队提供一份清晰、可执行、分优先级的综合优化方案。

## 输入的分析报告
```
{{report_context}}
```

## 输出要求
请你生成一份 Markdown 格式的优化方案，包含以下部分：

### 1. **总体性能摘要 (Executive Summary)**
- 简要总结当前应用在启动、帧率、内存方面的主要性能问题。
- 给出整体的性能评价（例如：良好，需要改进，存在严重问题）。

### 2. **优化任务优先级排序 (Prioritized Action Plan)**
- 将所有需要解决的问题列成一个待办事项列表。
- 根据问题的严重性和对用户体验的影响，将它们标记为 **高 (High)**、**中 (Medium)**、**低 (Low)** 三个优先级。
- 对于每个任务，简要说明“为什么”它很重要。

**示例格式:**
- **[高]** 修复 `some_widget.dart` 中的慢帧问题。*原因：直接导致用户界面卡顿，严重影响核心功能体验。*
- **[中]** 优化 `MyController` 导致的内存泄漏。*原因：长期运行可能导致应用崩溃，但短期影响不明显。*
- **[低]** 将启动时间从 1500ms 优化到 1200ms。*原因：当前启动时间尚可接受，属于体验优化。*

### 3. **详细优化方案 (Detailed Optimization Steps)**
- 针对每个 **高** 优先级和 **中** 优先级的任务，提供具体的、可操作的优化步骤和代码建议。
- 如果报告中提到了具体的文件和行号，请直接引用它们。
- 解释背后的原理，帮助开发者理解问题根源。

**示例格式:**

#### **[高] 修复 `some_widget.dart` 中的慢帧问题**
- **问题定位**: 分析报告指出，在 `some_widget.dart` 第 42 行的 `build` 方法中，一个耗时超过 50ms 的帧被触发。
- **根本原因**: 通过调用栈分析，问题可能出在 `build` 方法中进行了大量的同步计算或构建了过于复杂的 Widget 树。
- **优化步骤**:
  1.  **重构 `build` 方法**: 将 `build` 方法中的计算逻辑移出，可以考虑使用 `FutureBuilder` 或其他状态管理方案进行异步计算。
  2.  **使用 `const` 构造函数**: 检查 `some_widget.dart` 中可以被声明为 `const` 的 Widget，以减少不必要的重建。
  3.  **拆分 Widget**: 如果 Widget 过于庞大，请将其拆分为更小的、独立的子 Widget，并利用 `const` 或其他技术避免父 Widget 重建时子 Widget 也跟着重建。
- **代码建议**:
  ```dart
  // some_widget.dart:42
  // Before
  Widget build(BuildContext context) {
    // 模拟耗时操作
    final data = performHeavyCalculation(); 
    return HeavyWidget(data: data);
  }

  // After
  Widget build(BuildContext context) {
    return FutureBuilder<Data>(
      future: performHeavyCalculationAsync(), // 改为异步
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return HeavyWidget(data: snapshot.data!);
        }
        return CircularProgressIndicator();
      },
    );
  }
  ```

### 4. **后续建议与监控 (Next Steps & Monitoring)**
- 提出在完成上述优化后，可以采取的长期监控和预防措施。
- 例如：建议将性能分析集成到 CI/CD 流程中，定期进行性能回归测试。

请确保你的回答是结构化的、专业的，并且直接面向开发者，让他们可以拿着这份方案立即开始工作。
