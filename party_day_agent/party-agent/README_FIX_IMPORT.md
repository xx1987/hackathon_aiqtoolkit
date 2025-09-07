# 解决导入问题的完整指南

## 问题分析

在运行demo.py时遇到了相对导入问题：`attempted relative import with no known parent package`。这是因为Python的相对导入机制需要将模块作为包的一部分导入，而不是直接作为脚本运行。

## 解决方案

我们提供了以下几种解决方案，您可以根据自己的环境选择合适的方法：

### 方法1：使用我们创建的修复脚本（推荐）

我们创建了一个专门解决导入问题的脚本 `fix_imports.py`，它使用动态导入机制来正确加载planner模块。

使用方法：
```bash
# 设置环境变量
export GAODE_KEY="your_gaode_api_key"
export API_KEY="your_llm_api_key"
export BASE_URL="your_api_base_url"
export MODEL_NAME="your_model_name"

# 运行修复脚本
python fix_imports.py
```

### 方法2：修改导入路径（如果您想修改demo.py）

> 注意：在诊断模式下，每个文件只能修改一次

如果您需要修改demo.py，可以使用以下代码替换导入部分：

```python
# 使用importlib进行动态导入
import importlib.util
import os

def import_planner():
    planner_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'planner.py')
    spec = importlib.util.spec_from_file_location("planner", planner_path)
    planner = importlib.util.module_from_spec(spec)
    sys.modules["planner"] = planner
    spec.loader.exec_module(planner)
    return planner

# 然后在main函数中使用
planner = import_planner()
```

### 方法3：使用Python的-m选项运行（高级）

您也可以使用Python的`-m`选项从父目录运行程序，这样Python会将当前目录视为包：

```bash
# 切换到父目录
cd /opt/hackathon_aiqtoolkit/party_day_agent

# 使用-m选项运行
python -m party-agent.demo
```

## 为什么会出现这个问题？

Python的导入系统有两种模式：

1. **脚本模式**：直接运行`.py`文件，此时Python会将当前目录添加到`sys.path`，但不会将其视为包
2. **模块模式**：通过`import`语句或`-m`选项导入模块，此时Python会将模块所在目录视为包

相对导入（如`from . import planner`）只能在模块模式下工作，而直接运行脚本会使用脚本模式，导致相对导入失败。

## 其他说明

- `fix_imports.py`脚本提供了最可靠的解决方案，无论在什么环境下都能正常工作
- 如果您在其他地方也遇到类似的导入问题，可以参考此解决方案
- 如果您需要将代码作为包的一部分导入到其他项目中，建议使用方法2或方法3
- 所有API配置方法与之前的文档相同，请参考`README_API_CONFIG.md`文件

## 运行示例

使用修复脚本运行的完整命令：

```bash
# 设置API环境变量
export GAODE_KEY="test_gaode_api_key"
export API_KEY="test_llm_api_key"
export BASE_URL="http://localhost:8000/v1"
export MODEL_NAME="gpt-4o-mini"

# 运行修复脚本
python fix_imports.py
```

这样就能成功运行程序，避免导入问题！