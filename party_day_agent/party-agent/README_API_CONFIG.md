# 使用真实API运行程序的配置指南

## 1. 高德地图API配置

高德地图API用于搜索活动场地。根据代码分析，有两种调用模式：

### 1.1 REST API模式
- 配置环境变量：`GAODE_KEY` - 您的高德地图API密钥
- 默认使用REST API模式，无需额外配置
- API调用示例：`https://restapi.amap.com/v3/place/around?key={gaode_key}&location={lng},{lat}&radius={radius_km*1000}&types=150200|150300|150400|170200|170201&sortrule=distance&offset=20`

### 1.2 MCP模式（可选）
- 设置环境变量：`USE_GAODE_MCP=true` 启用MCP模式
- 配置环境变量：
  - `GAODE_MCP_URL` - MCP服务器地址
  - `GAODE_MCP_KEY` - MCP服务器密钥

## 2. 大模型API配置

程序支持三种大模型调用方式，按优先级自动选择：

### 2.1 API模式
- 配置环境变量：
  - `API_KEY` - 大模型API密钥
  - `BASE_URL` - API基础URL（如：`http://localhost:8000/v1`）
  - `MODEL_NAME` - 模型名称（如：`gpt-4o-mini`）

### 2.2 Ollama本地模型模式
- 确保已安装Ollama并启动服务
- 配置环境变量：`MODEL_NAME` - Ollama模型名称（如：`qwen2:7b`）
- 清除`API_KEY`和`BASE_URL`环境变量

### 2.3 模拟模式
- 无需配置任何环境变量
- 程序会自动使用模拟数据和响应

## 3. 运行程序的步骤

### 3.1 基本运行
```bash
# 设置环境变量
export GAODE_KEY="your_gaode_api_key"
export API_KEY="your_llm_api_key"
export BASE_URL="your_llm_api_base_url"
export MODEL_NAME="your_model_name"

# 运行demo.py
python demo.py
```

### 3.2 使用提供的脚本
使用已创建的测试脚本来快速测试不同配置：

```bash
# 使用API配置运行
./run_with_real_apis.sh

# 测试不同配置场景
./test_api_configs.sh
```

## 4. 程序容错机制

- 当无法连接到真实API时，程序会自动回退到模拟数据
- 场地搜索、日程检查、通知发送和总结生成等功能都有独立的模拟实现
- 即使在没有网络连接的环境下，程序也能运行并提供模拟结果

## 5. 注意事项

- 实际使用时，请替换为有效的API密钥和URL
- 模拟数据仅供测试和开发使用，生产环境应配置真实API
- 程序会在日志中记录API调用状态和错误信息，方便调试
- 对于高德API，搜索范围默认为10公里半径，可以在代码中调整`radius_km`参数