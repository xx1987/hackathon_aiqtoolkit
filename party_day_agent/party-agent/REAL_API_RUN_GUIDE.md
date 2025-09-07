# 使用真实API运行主题党日智能体的完整指南

## 1. 当前运行状态

经测试，主题党日智能体程序在当前环境中可以正常运行，包括：

- ✅ **后端服务器**：planner.py 在端口8000上正常运行
- ✅ **API端点**：健康检查(`/health`)和文件下载(`/files/{event_id}_summary.docx`)端点工作正常
- ✅ **模拟数据**：当无法连接到真实API时，程序会自动使用模拟数据
- ✅ **执行流程**：能够完成场地搜索、日程检查、计划生成、通知发送和总结生成的完整流程

## 2. 使用真实API的配置步骤

### 2.1 高德地图API配置

高德地图API用于搜索活动场地，配置方法如下：

```bash
# 设置高德地图API密钥
export GAODE_KEY="your_real_gaode_api_key"

# 可选：使用MCP模式（默认使用REST API模式）
export USE_GAODE_MCP="true"
export GAODE_MCP_URL="your_mcp_server_url"
export GAODE_MCP_KEY="your_mcp_api_key"
```

### 2.2 大模型API配置

大模型API用于生成活动方案和总结，支持以下两种模式：

#### 2.2.1 API模式（推荐）

```bash
export API_KEY="your_real_llm_api_key"
export BASE_URL="your_api_base_url"  # 如：https://api.openai.com/v1
export MODEL_NAME="your_model_name"  # 如：gpt-4o, claude-3-opus-20240229
```

#### 2.2.2 Ollama本地模型模式

```bash
# 清除API模式的环境变量
unset API_KEY
unset BASE_URL

# 设置Ollama模型名称
export MODEL_NAME="your_ollama_model_name"  # 如：qwen2:7b, llama3:8b
```

## 3. 运行程序的方法

### 3.1 启动后端服务

首先确保planner.py服务器正在运行：

```bash
# 在终端中启动后端服务（可使用nohup或tmux保持运行）
cd /opt/hackathon_aiqtoolkit/party_day_agent/party-agent
python planner.py
```

### 3.2 使用修复脚本运行程序

使用我们创建的`fix_imports.py`脚本可以避免导入问题：

```bash
# 设置环境变量
export GAODE_KEY="your_real_gaode_api_key"
export API_KEY="your_real_llm_api_key"
export BASE_URL="your_api_base_url"
export MODEL_NAME="your_model_name"

# 运行修复脚本
python fix_imports.py
```

### 3.3 使用便捷脚本

我们创建了以下便捷脚本：

- `run_with_mock_apis.sh`：使用模拟API配置运行程序
- `run_with_real_apis.sh`：使用真实API配置运行程序
- `test_api_configs.sh`：测试不同的API配置场景
- `test_api_endpoints.py`：测试API端点是否正常工作

使用方法：

```bash
# 给脚本添加执行权限
chmod +x *.sh *.py

# 运行脚本
./run_with_mock_apis.sh
```

## 4. 验证API是否正常工作

使用我们创建的`test_api_endpoints.py`脚本可以验证API端点是否正常工作：

```bash
python test_api_endpoints.py
```

这个脚本会检查：
- 服务器健康状态
- 报告下载功能
- 响应头和内容验证

## 5. 常见问题解决

### 5.1 导入问题

如果遇到`attempted relative import with no known parent package`错误，请使用`fix_imports.py`脚本替代直接运行`demo.py`。

### 5.2 API调用失败

如果API调用失败，程序会自动回退到模拟数据。检查以下几点：
- 环境变量是否正确设置
- API密钥是否有效
- 网络连接是否正常
- 防火墙设置是否阻止了API调用

### 5.3 端口冲突

如果端口8000已被占用，可以修改`planner.py`中的端口设置，或停止占用该端口的其他程序。

## 6. 运行效果展示

当前环境下，程序已经能够：

1. 接收活动主题、人数、位置等输入参数
2. 模拟搜索符合条件的活动场地
3. 生成详细的活动方案
4. 创建活动总结报告并提供下载链接

输出示例：
```
Party Day Agent completed, result: {
  'plan_id': 'plan_mock_venue_1_学习党的二十大精神',
  'theme': '学习党的二十大精神',
  'date': '2025-09-08',
  'venue': {
    'id': 'mock_venue_1',
    'name': '党员活动室',
    'address': '模拟地址',
    'capacity': 50,
    'lat': 39.9042,
    'lng': 116.4074
  },
  'notice_sent': True,
  'summary_file': 'http://localhost:8000/files/mock_summary.docx'
}
```

## 7. 实际环境部署建议

在实际生产环境中部署时，建议：

1. 使用配置文件或环境变量管理API密钥，避免硬编码
2. 设置适当的错误处理和日志记录
3. 考虑使用Docker容器化部署
4. 根据实际需求调整API调用参数（如搜索半径、结果数量等）
5. 定期更新API密钥和模型配置

按照本指南配置后，您可以在实际环境中使用真实API运行主题党日智能体，获得更准确的场地搜索结果和更优质的活动方案！