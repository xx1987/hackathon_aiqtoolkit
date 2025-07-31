# NVIDIA NeMo Agent Toolkit MCP 服务器实现要点

## 核心命令

### 启动MCP服务器
```bash
aiq mcp --config_file examples/getting_started/simple_calculator/configs/config.yml
```

### 查看MCP工具
```bash
aiq info mcp
aiq info mcp --tool calculator_multiply
```

### 运行MCP客户端
```bash
aiq run --config_file examples/MCP/simple_calculator_mcp/configs/config-mcp-math.yml --input "Is 2 times 2 greater than the current hour?"
```

## MCP工具配置格式

```yaml
functions:
  calculator_multiply:
    _type: mcp_tool_wrapper
    url: "http://localhost:9901/sse"
    mcp_tool_name: calculator_multiply
    description: "Returns the product of two numbers"
```

## 关键点
1. MCP服务器默认运行在 localhost:9901
2. 使用 `mcp_tool_wrapper` 类型包装远程MCP工具
3. 可以混合本地工具和远程MCP工具
4. 支持工具过滤发布

