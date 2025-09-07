# 主题党日活动智能助手

## 项目简介

主题党日活动智能助手是一款基于 NVIDIA 先进AI技术栈构建的智能工具，依托NeMo Agent Toolkit和FastMCP 2.0 + LangGraph架构，实现主题党日活动的全流程智能化管理，包括场地检索、日历冲突检测、活动方案生成、通知发送以及活动总结生成，大幅提升党建工作效率。

## 主要功能

- **智能场地检索**：基于地理位置、活动主题和参与人数，通过高德地图API智能推荐合适的活动场地
- **日历冲突自动检测**：自动检查选定日期是否与参与成员的日程安排存在冲突，并提供替代方案
- **AI活动方案生成**：结合大语言模型，根据活动主题、场地和参与人数生成个性化、丰富的活动方案
- **多渠道通知发送**：支持通过邮件等多种渠道发送活动通知
- **自动总结生成**：活动结束后自动生成格式规范的Word文档活动总结报告

## 目录结构

```
party_day_agent/
├── README.md          # 项目说明（本文件）
├── docs/              # 项目技术文档集合
└── party-agent/       # 核心实现目录
    ├── planner.py     # LangGraph工作流主体
    ├── demo.py        # 演示脚本
    ├── tests/         # 测试代码
    └── tools/         # 功能工具集合
        ├── venue_mcp.py     # 场地检索工具
        ├── calendar_mcp.py  # 日历冲突检测工具
        ├── notify_mcp.py    # 通知发送工具
        └── summary_mcp.py   # 活动总结生成工具
```

## 快速开始

### 环境要求
- Python 3.8+ 
- Docker及Docker Compose（推荐）
- NVIDIA GPU环境（最佳性能体验）

### 使用Docker启动

在项目根目录执行以下命令：

```bash
cd /opt/hackathon_aiqtoolkit/party_day_agent/party-agent
# 使用Docker Compose一键启动所有服务
docker compose up --build
```

### 本地开发环境启动

1. 安装依赖
```bash
cd /opt/hackathon_aiqtoolkit/party_day_agent/party-agent
pip install -r requirements.txt
```

2. 配置环境变量
   在party-agent目录下创建.env文件，添加必要的配置：
   ```env
   # 高德地图API密钥
   GAODE_KEY=your_gaode_api_key
   
   # 企业微信机器人Webhook URL
   WX_ROBOT_URL=your_wechat_robot_url
   
   # AI模型配置
   AIQ_LLM_API_KEY=your_api_key
   AIQ_LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   AIQ_LLM_MODEL=qwen-plus-2025-04-28
   ```

2. 启动各个服务组件
```bash
# 启动Planner主服务
python planner.py

# 在不同终端启动各个工具服务
python -m tools.venue_mcp
python -m tools.calendar_mcp
python -m tools.notify_mcp
python -m tools.summary_mcp

# 启动前端服务
python -m http.server 8080 --directory /opt/hackathon_aiqtoolkit/party_day_agent/party-agent
```

3. 访问前端页面
打开浏览器，访问 http://localhost:8080/frontend.html 即可使用系统

## NVIDIA技术应用

- **NeMo Agent Toolkit**：提供智能体构建的核心框架和组件
- **CUDA加速**：利用NVIDIA GPU的CUDA技术加速大语言模型处理能力
- **多智能体协作优化**：基于NVIDIA AI计算框架优化智能体间的协作效率
- **GPU资源智能管理**：通过Docker容器化部署实现GPU资源的高效利用

## 技术栈

- **核心框架**：NVIDIA NeMo Agent Toolkit、FastMCP 2.0、LangGraph
- **大语言模型**：支持Ollama等本地部署和API调用
- **Web服务**：FastAPI、HTTP Server
- **容器化**：Docker + Docker Compose
- **数据处理**：python-docx、ics等

## 应用领域

本项目主要应用于党政机关、企事业单位的主题党日、团建等集体活动策划与管理，通过智能化手段提升活动组织效率，降低人工成本，确保活动质量。

## License

[MIT License](LICENSE)

## 常见问题

1. **服务启动失败**：检查Docker和Docker Compose是否正确安装，以及环境变量配置是否正确
2. **场地搜索无结果**：确保提供了有效的地理位置坐标和合理的搜索半径
3. **通知发送失败**：检查企业微信机器人Webhook URL是否正确
4. **总结生成失败**：确保Word模板文件存在且格式正确

## 技术文档

项目包含完整的技术文档，存放在docs目录下，包括：
- 项目立项书
- 技术架构设计说明书
- 多智能体协作机制
- 系统集成&功能测试用例
- 性能优化&Bug修复记录等