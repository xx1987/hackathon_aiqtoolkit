# API密钥配置指南

本文档详细说明在主题党日智能体项目中如何维护和使用真实的API密钥，特别是大模型API和高德地图API的配置方式。

## 一、API密钥的主要配置方式

在项目中，API密钥主要通过以下两种方式进行配置和维护：

### 1. 环境变量配置（推荐方式）

程序会优先从环境变量中读取API密钥配置，这是最灵活和安全的方式。主要环境变量包括：

- **大模型API相关：**
  - `AIQ_LLM_API_KEY`: 大模型API密钥
  - `AIQ_LLM_BASE_URL`: 大模型API基础URL
  - `AIQ_LLM_MODEL`: 大模型名称

- **高德地图API相关：**
  - `GAODE_KEY`: 高德地图API密钥

- **其他服务：**
  - `MCP_URL`: FastMCP服务地址

### 2. 配置文件默认值

如果未设置环境变量，程序会使用默认值。这些默认值源自项目安装时`install.sh`脚本创建的配置文件：

- 配置文件路径：`/opt/hackathon_aiqtoolkit/NeMo-Agent-Toolkit/configs/hackathon_config.yml`
- 该文件包含了默认的大模型API设置

## 二、install.sh脚本中的API配置

`install.sh`脚本在项目安装过程中会创建默认的配置文件：

```bash
# 在install.sh中创建配置文件
cat > configs/hackathon_config.yml << 'EOF'
# NVIDIA NeMo Agent Toolkit 黑客松配置
# 支持用户自定义OpenAI兼容API

# ...其他配置...

llms:
  # 默认使用Bailian API (用户可修改)
  default_llm:
    _type: openai
    model_name: "qwen-plus-2025-04-28"
    api_key: "sk-"  # 默认API密钥
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"  # 默认API地址
    temperature: 0.7
    max_tokens: 2048

# ...其他配置...
EOF
```

## 三、planner.py中如何获取和使用API密钥

在`planner.py`文件中，程序通过以下代码获取和使用API密钥：

```python
# 尝试从环境变量或配置文件读取API配置
API_KEY = os.environ.get('AIQ_LLM_API_KEY', 'sk-')  # 默认使用install.sh中的API Key
BASE_URL = os.environ.get('AIQ_LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')  # 默认使用install.sh中的base_url
MODEL_NAME = os.environ.get('AIQ_LLM_MODEL', 'qwen-plus-2025-04-28')  # 默认使用install.sh中的模型

# 使用API调用大模型的客户端实现
class APILLMClient:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL
        self.model = MODEL_NAME
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_plan(self, theme, venue, date, headcount):
        # 构建提示词和API请求体
        # 发送API请求并处理响应
        # ...
```

## 四、运行脚本中的API密钥设置

项目提供的运行脚本（如`run_with_mock_apis.sh`）中也包含了API密钥的设置：

```bash
#!/bin/bash

# 设置模拟的API环境变量
# 这些值会覆盖默认值，但会被用户实际设置的环境变量覆盖
export GAODE_KEY="demo_gaode_key"
export API_KEY="sk-"
export BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export MODEL_NAME="qwen-plus-2025-04-28"

# 运行修复导入的脚本
python fix_imports.py
```

## 五、API密钥优先级

API密钥的读取和使用遵循以下优先级（从高到低）：

1. **用户直接设置的环境变量**（最高优先级，会覆盖其他所有设置）
2. **运行脚本中设置的环境变量**（如`run_with_mock_apis.sh`）
3. **配置文件中的默认值**（来自`hackathon_config.yml`）
4. **代码中的硬编码默认值**（最低优先级）

## 六、使用真实API密钥运行程序的推荐方法

### 方法一：临时设置环境变量（推荐用于测试）

```bash
# 在终端中设置环境变量，然后运行程序
export AIQ_LLM_API_KEY="your_real_api_key"
export GAODE_KEY="your_gaode_api_key"
python fix_imports.py
```

### 方法二：创建自定义运行脚本

复制`run_with_mock_apis.sh`，修改其中的API密钥为真实值，然后运行自定义脚本：

```bash
# 复制模板脚本
cp run_with_mock_apis.sh run_with_real_apis.sh

# 编辑脚本，修改API密钥
# 然后运行脚本
chmod +x run_with_real_apis.sh
./run_with_real_apis.sh
```

### 方法三：直接修改配置文件

编辑`NeMo-Agent-Toolkit/configs/hackathon_config.yml`文件，替换其中的默认API密钥：

```bash
# 编辑配置文件
nano /opt/hackathon_aiqtoolkit/NeMo-Agent-Toolkit/configs/hackathon_config.yml

# 运行程序
python fix_imports.py
```

## 七、注意事项

1. **安全性**：不要将真实的API密钥直接硬编码到代码中，尤其是在需要提交到版本控制系统的代码中。

2. **密钥保护**：定期更新API密钥，不要在公共场合或不安全的渠道分享密钥。

3. **错误处理**：程序包含了错误处理机制，当API调用失败时会使用模拟数据作为后备，确保程序能够正常运行。

4. **验证**：可以通过检查程序输出日志来确认是否使用了真实的API密钥进行调用。

## 八、常见问题解答

**Q: 我设置了环境变量，但程序似乎没有使用？**
**A:** 请确认环境变量名称是否正确，并检查是否在正确的终端会话中设置了环境变量。可以使用`printenv`命令查看当前设置的环境变量。

**Q: 如何判断程序是否在使用真实的API密钥？**
**A:** 观察程序输出日志，如果看到`Using API LLM client with model: xxx`的信息，说明程序正在尝试使用API调用大模型。如果API调用失败，会显示相应的错误信息并切换到模拟数据。

**Q: 我可以同时配置多个不同的API密钥吗？**
**A:** 是的，可以通过不同的环境变量来配置大模型API和高德地图API等不同服务的密钥。

## 九、文件位置参考

- 安装脚本：`/opt/hackathon_aiqtoolkit/install.sh`
- 配置文件：`/opt/hackathon_aiqtoolkit/NeMo-Agent-Toolkit/configs/hackathon_config.yml`
- 主要程序：`/opt/hackathon_aiqtoolkit/party_day_agent/party-agent/planner.py`
- 运行脚本：`/opt/hackathon_aiqtoolkit/party_day_agent/party-agent/run_with_mock_apis.sh`