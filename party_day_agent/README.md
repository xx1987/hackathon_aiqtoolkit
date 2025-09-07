# 主题党日智能体

# 主题党日活动智能助手

## 项目简介

主题党日活动智能助手是一款基于 NVIDIA NeMo Agent Toolkit 和 FastMCP 2.0 + LangGraph 构建的智能工具，能够自动化完成主题党日活动的全流程管理，包括场地检索、日历冲突检测、活动方案生成、通知发送以及活动总结生成。

## 主要功能

- **场地检索**：基于地理位置、活动主题和参与人数智能推荐合适的活动场地
- **日历冲突检测**：自动检查选定日期是否与参与成员的日程安排存在冲突
- **AI方案生成**：结合大语言模型，根据活动主题、场地和参与人数生成详细的活动方案
- **多渠道通知**：支持通过企业微信群机器人发送活动通知
- **自动总结生成**：活动结束后自动生成Word格式的活动总结报告

## 目录结构

```
party_day_agent/
├── README.md          # 项目说明（本文件）
└── party-agent/       # 核心实现目录
    ├── planner.py     # LangGraph工作流主体
    ├── tools/         # 功能工具集合
    ├── docker-compose.yml  # Docker配置文件
    └── requirements.txt    # Python依赖列表
```

## 快速开始

请进入 `party-agent` 目录，按照其中的README.md文件进行操作：

```bash
cd party-agent
# 查看详细的使用说明
cat README.md
# 或使用Docker一键启动
# docker compose up --build
```

## 技术栈

- **核心框架**：NVIDIA NeMo Agent Toolkit、FastMCP 2.0、LangGraph
- **大语言模型**：支持API调用和本地部署
- **Web服务**：FastAPI
- **容器化**：Docker + Docker Compose

## License

[MIT License](LICENSE)