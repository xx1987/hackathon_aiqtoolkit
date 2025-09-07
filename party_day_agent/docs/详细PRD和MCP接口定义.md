# 主题党日智能体详细PRD和MCP接口定义

## 1. 概述

本文档详细描述了主题党日活动智能助手项目的产品需求规格（PRD）和MCP（Multi-agent Communication Protocol）接口定义。文档分为两部分：第一部分为产品需求规格，描述系统的功能、性能、用户体验等方面的要求；第二部分为MCP接口定义，描述智能体间通信的协议规范和接口格式。

## 2. 产品需求规格（PRD）

### 2.1 产品概述

主题党日活动智能助手是一款基于人工智能技术的智能体系统，旨在帮助党组织自动化、智能化地规划和管理主题党日活动，提高活动策划效率和质量。

### 2.2 核心功能需求

#### 2.2.1 活动方案生成功能

**功能描述**：根据用户输入的活动信息，自动生成完整的活动方案。

**输入**：
- 活动主题
- 活动日期
- 活动地点
- 参与人数
- 其他特殊需求

**输出**：
- 完整的活动方案，包括：
  - 推荐场地信息（名称、地址、容量、联系方式等）
  - 活动日程安排（时间节点、活动内容等）
  - 活动注意事项
  - 活动物资准备清单

#### 2.2.2 场地检索功能

**功能描述**：根据地理位置、活动主题和参与人数，搜索合适的活动场地。

**输入**：
- 地理位置
- 活动主题
- 参与人数
- 场地类型（可选）
- 预算范围（可选）

**输出**：
- 场地列表，每个场地包含：
  - 场地名称
  - 详细地址
  - 地理坐标
  - 容量
  - 联系方式
  - 场地图片（可选）
  - 推荐指数

#### 2.2.3 日历检查功能

**功能描述**：检查指定日期是否与参与成员的日程安排存在冲突。

**输入**：
- 检查日期
- 参与成员列表
- 活动时间段

**输出**：
- 冲突检测结果（是否存在冲突）
- 冲突详情（如果有冲突）
- 建议的替代日期

#### 2.2.4 通知发送功能

**功能描述**：将生成的活动方案通过企业微信机器人发送给参与成员。

**输入**：
- 活动方案信息
- 参与成员列表
- 通知内容模板

**输出**：
- 通知发送状态（成功/失败）
- 发送时间
- 接收人数

#### 2.2.5 总结生成功能

**功能描述**：生成活动总结报告，支持Word文档格式。

**输入**：
- 活动方案信息
- 活动实际执行情况
- 参与人员反馈（可选）

**输出**：
- Word格式的活动总结报告
- 报告生成状态
- 报告文件路径

### 2.3 非功能需求

#### 2.3.1 性能需求

- 系统响应时间：平均响应时间<2秒，最大响应时间<5秒
- 系统吞吐量：支持100个并发用户，每秒处理50个请求
- 资源占用：在满载情况下，CPU使用率<70%，内存使用率<80%

#### 2.3.2 可靠性需求

- 系统可用性：≥99.9%
- 数据可靠性：数据丢失率<0.1%
- 错误处理：提供完善的错误处理机制，确保系统稳定运行

#### 2.3.3 安全性需求

- 数据安全：敏感数据加密存储和传输
- 访问控制：实现用户身份认证和权限控制
- 防止攻击：防止SQL注入、XSS等常见安全攻击

#### 2.3.4 可扩展性需求

- 模块化设计：系统各组件应采用模块化设计，支持独立部署和扩展
- 接口标准化：采用标准化的接口设计，支持不同系统和组件的集成
- 技术选型：选择具有良好扩展性的技术栈

#### 2.3.5 用户体验需求

- 界面友好：提供简洁、直观的用户界面
- 操作简便：简化用户操作流程，减少用户输入
- 响应及时：提供及时的操作反馈和状态提示
- 兼容性：支持主流浏览器和操作系统

### 2.4 用户界面需求

#### 2.4.1 整体布局

- 采用响应式设计，适应不同屏幕尺寸
- 主要区域包括：顶部导航栏、活动信息输入区、状态显示区、结果展示区
- 布局简洁明了，重点突出

#### 2.4.2 输入表单

- 提供活动主题、日期、地点、人数等信息的输入字段
- 支持表单验证，提示用户输入错误
- 提供默认值和智能提示

#### 2.4.3 结果展示

- 以卡片形式展示活动方案的各个部分
- 提供清晰的视觉层次和信息组织
- 支持结果的导出和分享

## 3. MCP接口定义

### 3.1 MCP协议概述

MCP（Multi-agent Communication Protocol）是系统中智能体间通信的核心协议，采用基于HTTP/HTTPS的RESTful架构，实现了主智能体与工具智能体之间的高效协作。

### 3.2 接口通用格式

#### 3.2.1 请求格式

所有MCP接口请求均采用以下格式：

```json
{
  "tool_name": "string",
  "parameters": {
    // 工具参数，根据不同工具类型有所不同
  }
}
```

#### 3.2.2 响应格式

所有MCP接口响应均采用以下格式：

```json
{
  "success": "boolean",
  "result": "any",  // 工具调用结果，根据不同工具类型有所不同
  "error": "string"  // 错误信息，成功时为null
}
```

### 3.3 工具接口定义

#### 3.3.1 场地检索工具接口

**工具名称**：search_venue

**请求参数**：

```json
{
  "location": "string",  // 地理位置
  "theme": "string",     // 活动主题
  "headcount": "number", // 参与人数
  "venue_type": "string", // 场地类型（可选）
  "budget": "number"      // 预算范围（可选）
}
```

**响应结果**：

```json
{
  "venues": [
    {
      "id": "string",
      "name": "string",
      "address": "string",
      "lat": "number",
      "lng": "number",
      "capacity": "number",
      "contact": "string",
      "rating": "number",
      "images": ["string"],
      "description": "string"
    }
    // 更多场地...
  ]
}
```

#### 3.3.2 日历检查工具接口

**工具名称**：check_calendar

**请求参数**：

```json
{
  "date": "string",  // 检查日期，格式：YYYY-MM-DD
  "members": ["string"], // 参与成员列表
  "start_time": "string", // 活动开始时间，格式：HH:MM
  "end_time": "string"  // 活动结束时间，格式：HH:MM
}
```

**响应结果**：

```json
{
  "conflict": "boolean",
  "conflict_details": [
    {
      "member": "string",
      "event_name": "string",
      "event_time": "string"
    }
    // 更多冲突...
  ],
  "alternative_dates": [
    {
      "date": "string",
      "score": "number" // 推荐分数
    }
    // 更多推荐日期...
  ],
  "conflict_probability": "number" // 冲突概率，范围0-1
}
```

#### 3.3.3 通知发送工具接口

**工具名称**：send_notification

**请求参数**：

```json
{
  "title": "string",  // 通知标题
  "content": "string", // 通知内容
  "recipients": ["string"], // 接收人列表
  "notification_type": "string", // 通知类型：wechat、email等
  "template_id": "string"  // 通知模板ID（可选）
}
```

**响应结果**：

```json
{
  "sent": "boolean",
  "sent_time": "string",
  "recipient_count": "number",
  "success_count": "number",
  "failed_count": "number",
  "failed_recipients": ["string"],
  "message_id": "string",
  "local_file_path": "string" // 本地保存的通知文件路径
}
```

#### 3.3.4 总结生成工具接口

**工具名称**：generate_summary

**请求参数**：

```json
{
  "activity_info": {
    "theme": "string",
    "date": "string",
    "location": "string",
    "headcount": "number",
    "speakers": ["string"],
    "agenda": ["string"]
  },
  "execution_info": {
    "actual_date": "string",
    "attendance": "number",
    "feedback": "string",
    "photos": ["string"]
  },
  "template_name": "string", // 模板名称
  "output_format": "string"  // 输出格式：docx、pdf等
}
```

**响应结果**：

```json
{
  "generated": "boolean",
  "file_path": "string",
  "file_url": "string",
  "generation_time": "string",
  "file_size": "number"
}
```

### 3.4 服务接口定义

#### 3.4.1 主服务API接口

**接口名称**：/run

**请求方法**：POST

**请求参数**：

```json
{
  "theme": "string",
  "date": "string",
  "location": "string",
  "headcount": "number",
  "members": ["string"],
  "requirements": "string",
  "send_notification": "boolean",
  "generate_summary": "boolean"
}
```

**响应结果**：

```json
{
  "success": "boolean",
  "plan": {
    "theme": "string",
    "date": "string",
    "venue": {
      "name": "string",
      "address": "string",
      "capacity": "number",
      "contact": "string"
    },
    "agenda": [
      {
        "time": "string",
        "content": "string"
      }
    ],
    "requirements": "string",
    "notes": "string"
  },
  "notification_result": {}, // 通知发送结果
  "summary_result": {},      // 总结生成结果
  "error": "string"
}
```

#### 3.4.2 工具服务通用接口

**接口名称**：/call

**请求方法**：POST

**请求参数**：见3.2.1节请求格式

**响应结果**：见3.2.2节响应格式

### 3.5 错误码定义

系统定义了以下错误码：

| 错误码 | 错误描述 | HTTP状态码 |
|--------|----------|------------|
| 40001 | 参数错误 | 400 |
| 40002 | 工具不存在 | 404 |
| 50001 | 内部服务器错误 | 500 |
| 50002 | 外部API调用失败 | 500 |
| 50003 | 数据库错误 | 500 |
| 50004 | 系统繁忙 | 503 |

### 3.6 协议版本控制

MCP协议支持版本控制，通过请求头中的"MCP-Version"字段指定协议版本。

当前版本：2.0

## 4. 接口测试规范

### 4.1 测试方法

- 单元测试：对每个接口的功能进行单独测试
- 集成测试：测试接口之间的集成是否正常
- 性能测试：测试接口在不同负载下的性能表现
- 安全性测试：测试接口的安全性

### 4.2 测试工具

- pytest：用于单元测试和集成测试
- requests：用于HTTP接口测试
- locust：用于性能测试
- OWASP ZAP：用于安全性测试

### 4.3 测试用例设计

测试用例应包括以下内容：

- 测试用例ID和名称
- 测试目标
- 测试环境
- 测试步骤
- 输入数据
- 预期输出
- 实际输出
- 测试结论

## 5. 接口变更管理

### 5.1 变更流程

1. **变更申请**：提出接口变更需求，包括变更内容、原因、影响范围等
2. **变更评审**：由相关人员对变更需求进行评审
3. **变更实施**：根据评审结果实施接口变更
4. **变更测试**：对变更后的接口进行测试
5. **变更发布**：发布变更后的接口，并更新相关文档
6. **变更通知**：通知相关团队和人员接口变更情况

### 5.2 版本兼容性

接口变更应保持向后兼容性，确保旧版本客户端能够正常使用新版本接口。如确需不兼容变更，应在新版本中提供迁移方案和足够的过渡期。

---
版本：v1.0.0
编制日期：2025-09-07