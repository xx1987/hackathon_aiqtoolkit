# 主题党日智能体 - 测试指南

本指南将帮助您快速了解如何测试和使用主题党日智能体系统。

## 目录

- [快速开始](#快速开始)
- [启动完整系统](#启动完整系统)
- [测试方式](#测试方式)
- [查看运行状态](#查看运行状态)
- [停止系统](#停止系统)
- [API密钥配置](#api密钥配置)
- [常见问题](#常见问题)

## 快速开始

1. 确保您已在正确的目录下：
   ```bash
   cd /opt/hackathon_aiqtoolkit/party_day_agent/party-agent
   ```

2. 启动完整系统（同时启动前端和后端服务）：
   ```bash
   ./start_full_system.sh
   ```

3. 在浏览器中访问前端界面：
   [http://localhost:8080/frontend.html](http://localhost:8080/frontend.html)

4. 查看API文档：
   [http://localhost:8000/docs](http://localhost:8000/docs)

## 启动完整系统

使用我们提供的启动脚本，可以一键启动前后端服务：

```bash
./start_full_system.sh
```

该脚本会自动：
- 检查并配置API密钥环境变量
- 启动后端服务（planner.py）
- 启动前端服务（run_frontend.py）
- 创建停止服务的脚本
- 显示使用指南

## 测试方式

### 1. 使用前端界面测试

打开浏览器访问：[http://localhost:8080/frontend.html](http://localhost:8080/frontend.html)

在前端界面中，您可以：
- 查看智能体生成的活动方案
- 浏览模拟的活动数据
- 体验完整的主题党日活动流程

### 2. 使用命令行测试

运行测试脚本：

```bash
python demo.py
```

或使用真实API测试：

```bash
./run_with_real_apis.sh
```

### 3. 直接调用API测试

使用curl或其他HTTP工具直接调用API：

```bash
# 检查健康状态
curl http://localhost:8000/health

# 下载活动报告
curl -o report.docx http://localhost:8000/download_report?event_id=123

# 查看生成的总结文件
curl -o summary.docx http://localhost:8000/files/mock_summary.docx
```

## 查看运行状态

要查看系统的详细运行状态，请参考：

```bash
cat RUN_STATUS_SUMMARY.md
```

该文件包含：
- 后端服务运行状态
- 前端服务运行状态
- 智能体运行结果
- 可能的问题与解决方案

## 停止系统

使用我们提供的停止脚本，可以一键停止所有服务：

```bash
./stop_full_system.sh
```

## API密钥配置

### 默认配置

系统默认使用内置的API密钥进行测试，这些密钥可能有限制或仅用于演示目的。

### 使用自己的API密钥

如果您想使用自己的真实API密钥，可以通过设置环境变量来实现：

```bash
# 设置大模型API密钥
export AIQ_LLM_API_KEY=您的真实API密钥

# 设置高德地图API密钥
export GAODE_KEY=您的真实高德地图API密钥

# 可选：设置其他参数
export AIQ_LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
export AIQ_LLM_MODEL=qwen-plus-2025-04-28
```

设置完环境变量后，重新启动系统即可使用您的API密钥。

更多API密钥配置详情，请参考：

```bash
cat API_KEY_CONFIGURATION.md
```

## 常见问题

### 1. 服务启动失败

**问题**：后端或前端服务启动失败
**解决方案**：
- 检查端口是否被占用（8000和8080）
- 检查Python环境和依赖是否正确安装
- 查看终端输出的错误信息进行排查

### 2. API调用失败

**问题**：FastMCP工具调用失败，显示"All connection attempts failed"
**解决方案**：
- 检查网络连接是否正常
- 确认API密钥是否正确
- 系统有容错机制，会自动回退到模拟数据

### 3. 前端页面加载问题

**问题**：前端页面无法加载或显示异常
**解决方案**：
- 确认后端服务是否正常运行
- 清除浏览器缓存后重试
- 尝试使用不同的浏览器

### 4. 如何查看详细日志

**问题**：如何查看系统的详细运行日志
**解决方案**：
- 后端服务日志：查看运行planner.py的终端
- 前端服务日志：查看运行run_frontend.py的终端
- 测试日志：运行测试脚本时的终端输出

## 更多资源

- [README.md](README.md) - 项目总览
- [REAL_API_RUN_GUIDE.md](REAL_API_RUN_GUIDE.md) - 真实API运行指南
- [API_KEY_CONFIGURATION.md](API_KEY_CONFIGURATION.md) - API密钥配置指南
- [RUN_STATUS_SUMMARY.md](RUN_STATUS_SUMMARY.md) - 当前运行状态总结

祝您测试愉快！