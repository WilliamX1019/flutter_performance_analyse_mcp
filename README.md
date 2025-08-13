# Flutter 性能分析工具 (基于 Gemini 多 Agent 工作流)

一个强大的、自动化的性能分析工具包，专为 Flutter 应用设计，构建于 Gemini Code Assist 多 Agent 工作流 (MCP) 之上。

## ✨ 功能特性

*   **帧率 (FPS) 分析**: 识别慢帧，并精确定位导致 UI 卡顿的具体耗时操作。
*   **内存泄漏分析**: 检测常见的内存泄漏模式，并高亮显示内存占用异常的对象。
*   **应用启动分析**: 将应用的启动时间分解为引擎加载、框架初始化和首帧渲染等多个阶段。
*   **包大小分析**: 分析 Android (APK/AAB) 和 iOS (IPA) 的包大小，帮助开发者进行瘦身。
*   **AI 综合优化报告**: 整合所有独立的分析结果，利用 Gemini Agent 生成一份带有优先级、可执行的综合优化方案。

## 🚀 开始使用

### 先决条件

在开始之前，请确保您已安装以下软件：

*   [Python 3.8+](https://www.python.org/)
*   [Flutter SDK](https://flutter.dev/docs/get-started/install)
*   [Visual Studio Code](https://code.visualstudio.com/)
*   VS Code 中的 [Gemini Code Assist](https://marketplace.visualstudio.com/items?itemName=GoogleCloudTools.gemini-code-assist) 扩展。

## 安装依赖

### 安装与配置

1.  **克隆仓库**
    ```bash
    git clone https://github.com/<Your-GitHub-Username>/<Your-Repository-Name>.git
    cd <Your-Repository-Name>
    ```

2.  **安装 Python 依赖**
    建议在虚拟环境中安装，以避免包冲突。
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # 在 Windows 上, 使用 `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **在 VS Code 中配置 Gemini**
    您需要告诉 Gemini 扩展去使用本项目的 `mcp_config.yaml` 配置文件。

    *   在 VS Code 中打开克隆下来的项目文件夹。
    *   打开设置 (`Ctrl/Cmd + ,`)，搜索 `gemini.experimental.mcpConfigPath`。
    *   将其值设置为 `${workspaceFolder}/mcp_config.yaml`。这会自动指向当前项目根目录下的配置文件。
    *   确保 `gemini.experimental.mcp` 选项已勾选启用。

## 运行工作流

**重要提示**: 请在您**想要分析的 Flutter 项目的根目录**下运行以下所有 `mcp` 命令。

### 1. 运行独立的分析工作流

您可以独立运行每一个分析任务。`<path-to-this-toolkit>` 是您存放本分析工具的路径。

*   **分析帧率**: `mcp run <path-to-this-toolkit>/mcp_config.yaml -w fps_workflow`
*   **分析内存泄漏**: `mcp run <path-to-this-toolkit>/mcp_config.yaml -w leak_workflow`
*   **分析启动时间**: `mcp run <path-to-this-toolkit>/mcp_config.yaml -w startup_workflow`
*   **分析包大小 (APK)**: `mcp run <path-to-this-toolkit>/mcp_config.yaml -w package_size_apk_workflow`
*   *(其他包大小工作流: `package_size_aab_workflow`, `package_size_ipa_workflow`)*

### 2. 生成综合 AI 优化报告 (推荐)

在运行了任意一个或多个独立分析后，您可以运行 `optimization_workflow` 来获得一份由 AI 生成的、整合所有信息的综合优化方案。

```bash
mcp run <path-to-this-toolkit>/mcp_config.yaml -w optimization_workflow
```

## 查看结果

*   所有报告都将生成在您**被分析的 Flutter 项目**的根目录下的 `output/` 文件夹中。
*   最终的综合优化方案是 **`output/comprehensive_optimization_plan.md`**。

**注意**: 每次运行工作流都会**覆盖**同名的旧报告。如果需要保留历史记录，请在再次运行前备份 `output` 目录或重命名报告文件。
