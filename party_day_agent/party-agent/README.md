# 主题党日活动智能助手

## 项目简介

主题党日活动智能助手是一款基于 NVIDIA NeMo Agent Toolkit、FastMCP 2.0 和 LangGraph 构建的智能工具，能够自动化完成主题党日活动的全流程管理，包括场地检索、日历冲突检测、活动方案生成、通知发送以及活动总结生成。该项目旨在提升党建工作效率，为党组织提供便捷的活动策划和管理解决方案。

## 功能特点

- **智能场地检索**：基于高德地图API，根据活动主题、参与人数和地理位置智能推荐合适的活动场地
- **日历冲突检测**：自动检查选定日期是否与参与成员的日程安排存在冲突
- **AI方案生成**：结合大语言模型，根据活动主题、场地和参与人数生成详细的活动方案
- **多渠道通知**：通过企业微信群机器人自动发送活动通知，确保参与人员及时获知活动信息
- **自动总结生成**：活动结束后自动生成Word格式的活动总结报告，减轻工作负担

## 技术栈

- **核心框架**：NVIDIA NeMo Agent Toolkit + FastMCP 2.0 + LangGraph
- **大语言模型**：支持API调用（默认使用阿里云DashScope）和Ollama本地部署，利用CUDA加速处理
- **Web服务**：FastAPI
- **容器化**：Docker + Docker Compose
- **外部API**：高德地图API、企业微信机器人Webhook

## 项目结构

```
party-agent/
├── planner.py          # LangGraph工作流主体，定义智能体核心逻辑
├── demo.py             # 演示脚本
├── tests/              # 测试目录
├── tools/
│   ├── venue_mcp.py    # 场地检索工具，集成高德地图API
│   ├── calendar_mcp.py # 日历冲突检测工具
│   ├── notify_mcp.py   # 通知发送工具，集成企业微信机器人
│   └── summary_mcp.py  # 活动总结生成工具
├── docker-compose.yml  # Docker Compose配置文件
├── Dockerfile.planner  # LangGraph主服务Dockerfile
├── Dockerfile.tools    # 工具服务Dockerfile
├── requirements.txt    # Python依赖列表
└── README.md           # 项目说明文档
```

## 快速开始

### 前提条件

- 安装 Docker 和 Docker Compose
- （可选）高德地图Web API密钥（`GAODE_KEY`）
- （可选）企业微信机器人Webhook URL（`WX_ROBOT_URL`）
- （可选）AI模型API密钥（默认使用内置的API密钥）

### 一键启动

在项目根目录下执行以下命令启动服务：

```bash
docker compose up --build
```

### 服务访问地址

启动后，可以通过以下地址访问服务：
- LangGraph主服务：http://localhost:8000
- API文档：http://localhost:8000/docs
- 场地搜索工具文档：http://localhost:8001/docs
- 日历检查工具文档：http://localhost:8002/docs
- 通知发送工具文档：http://localhost:8003/docs
- 总结生成工具文档：http://localhost:8004/docs

## 配置说明

创建 `.env` 文件配置环境变量：

```env
# 高德地图API密钥
GAODE_KEY=your_gaode_api_key

# 企业微信机器人Webhook URL
WX_ROBOT_URL=your_wechat_robot_url

# Word模板文件路径
DOCX_TEMPLATE=./template.docx

# AI模型配置
AIQ_LLM_API_KEY=your_api_key
AIQ_LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AIQ_LLM_MODEL=qwen-plus-2025-04-28

# FastMCP服务地址
MCP_URL=http://localhost
```

## API使用示例

### Python调用示例

```python
import httpx
import asyncio

async def test_agent():
    # 示例输入数据
    input_data = {
        "theme": "学习贯彻党的二十大精神",
        "headcount": 25,
        "lat": 39.9042,  # 北京坐标示例
        "lng": 116.4074,
        "radius_km": 5,
        "member_ids": ["张三", "李四", "王五"]
    }
    
    # 调用智能体服务
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/run",
            json=input_data,
            timeout=60.0
        )
        
        # 打印结果
        print("智能体返回结果:")
        print(response.json())

# 运行测试
asyncio.run(test_agent())
```

### 输入参数说明

| 参数名 | 类型 | 说明 | 是否必填 |
|--------|------|------|----------|
| theme | string | 活动主题 | 是 |
| headcount | integer | 参与人数 | 是 |
| lat | float | 地理位置纬度 | 是 |
| lng | float | 地理位置经度 | 是 |
| radius_km | float | 搜索半径（公里） | 否（默认10） |
| member_ids | array | 参与成员ID列表 | 否（默认生成10个模拟成员） |

### 返回结果示例

```json
{
  "plan_id": "plan_123456789",
  "theme": "学习贯彻党的二十大精神",
  "date": "2025-09-07",
  "venue": {
    "id": "venue_001",
    "name": "党员活动室",
    "address": "北京市海淀区中关村大街1号",
    "capacity": 50,
    "lat": 39.9042,
    "lng": 116.4074
  },
  "notice_sent": true,
  "summary_file": "http://localhost:8000/files/summary_123456789.docx"
}
```

## 工具服务说明

项目包含四个核心工具服务，每个服务独立运行并提供REST API接口：

### 1. 场地检索服务（venue_mcp.py）
- 端口：8001
- 功能：根据地理位置、活动主题和参与人数搜索合适的活动场地
- API端点：`/tools/venue.search`

### 2. 日历冲突检测服务（calendar_mcp.py）
- 端口：8002
- 功能：检查指定日期是否与成员日历存在冲突
- API端点：`/tools/calendar.check`

### 3. 通知发送服务（notify_mcp.py）
- 端口：8003
- 功能：通过企业微信机器人发送活动通知
- API端点：`/tools/notify.send`

### 4. 总结生成服务（summary_mcp.py）
- 端口：8004
- 功能：生成Word格式的活动总结报告
- API端点：`/tools/summary.generate`

## 健康检查

可以通过以下端点检查服务健康状态：

```bash
curl http://localhost:8000/health
```

## 常见问题

1. **服务启动失败**：检查Docker和Docker Compose是否正确安装，以及环境变量配置是否正确
2. **场地搜索无结果**：确保提供了有效的地理位置坐标和合理的搜索半径
3. **通知发送失败**：检查企业微信机器人Webhook URL是否正确
4. **总结生成失败**：确保Word模板文件存在且格式正确

## 扩展开发

如果需要扩展项目功能，可以参考以下方式：
1. 在`planner.py`中修改工作流逻辑
2. 在`tools`目录下添加新的工具服务
3. 更新`docker-compose.yml`以包含新的服务

## 许可证

[MIT License](LICENSE)

## 工作流程

主题党日活动智能助手的工作流程由LangGraph框架定义，按照以下步骤自动执行：

1. **场地检索（search_venues）**：根据输入的地理位置、活动主题和参与人数，调用场地检索工具搜索合适的活动场地
2. **日历冲突检测（check_calendar）**：生成建议的活动日期，并检查该日期是否与参与成员的日程安排存在冲突
3. **方案生成（generate_plan）**：结合大语言模型，根据活动主题、选定的场地和日期生成详细的活动方案
4. **通知发送（send_notice）**：将生成的活动方案通过企业微信机器人发送给参与成员
5. **总结生成（write_summary）**：生成活动总结报告，便于后续归档和分享

![工作流程图](workflow.png)

节点之间通过边缘连接，形成完整的工作流，确保活动策划过程的自动化和连贯性。任一节点失败会自动重试2次，确保流程稳定运行。

## 开发说明

### 本地开发

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 分别启动各个服务：
   ```bash
   # 启动场地搜索服务
   python -m tools.venue_mcp
   
   # 启动日历检查服务
   python -m tools.calendar_mcp
   
   # 启动通知发送服务
   python -m tools.notify_mcp
   
   # 启动总结生成服务
   python -m tools.summary_mcp
   
   # 启动LangGraph主服务
   python planner.py
   ```

### 注意事项

- 所有服务都提供了模拟数据功能，即使没有配置真实的API密钥也能正常运行
- 在生产环境中，请配置真实的API密钥以获得更好的使用体验
- 服务默认在Docker网络中相互通信，使用`localhost`即可访问彼此

## 依赖说明

主要依赖：
- NVIDIA NeMo Agent Toolkit：提供智能体开发基础组件
- fastmcp>=2.0：FastMCP工具框架
- langgraph>=0.0.40：LangGraph工作流框架
- httpx：HTTP客户端
- python-docx：Word文档生成
- ics：日历文件处理
- uvicorn：ASGI服务器

## License

MIT License