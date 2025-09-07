#!/bin/bash

# 测试不同的API配置

echo "=== 测试场景1: 使用API模式（默认） ==="
export GAODE_KEY="test_gaode_api_key"
export API_KEY="test_llm_api_key"
export BASE_URL="http://localhost:8000/v1"
export MODEL_NAME="gpt-4o-mini"
echo "GAODE_KEY=$GAODE_KEY"
echo "API_KEY=$API_KEY"
echo "运行demo.py..."
python demo.py

echo "\n=== 测试场景2: 使用Ollama本地模型模式 ==="
unset API_KEY
unset BASE_URL
export MODEL_NAME="qwen2:7b"
echo "MODEL_NAME=$MODEL_NAME"
echo "运行demo.py..."
python demo.py

echo "\n=== 测试场景3: 完全模拟模式 ==="
unset GAODE_KEY
unset API_KEY
unset BASE_URL
unset MODEL_NAME
echo "所有API环境变量已清除"
echo "运行demo.py..."
python demo.py