# Flutter 性能分析多 Agent 工作流

## 安装依赖
```bash
pip install -r requirements.txt
```

## 配置 Gemini Code Assist
1. 打开 VS Code
2. 进入 Gemini Code Assist 设置  
   **Preferences → Extensions → Gemini Code Assist**
3. 在 `mcp_config_path` 中选择本项目 `mcp_config.yaml`

也可以直接编辑项目根目录下 .vscode/settings.json 文件，添加类似配置：
{
  "gemini.experimental.mcp": true,
  "gemini.experimental.mcpConfigPath": "${workspaceFolder}/mcp_config.yaml"
}

## 运行工作流
```bash
mcp run mcp_config.yaml -w fps_workflow
```
```bash
mcp run mcp_config.yaml -w leak_workflow
```
```bash
mcp run mcp_config.yaml -w startup_workflow
```


## 查看结果
优化报告会自动生成在：
```
output/perf_report.md
```