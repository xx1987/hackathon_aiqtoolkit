#!/bin/bash

# 设置模拟API环境变量
echo "设置模拟API环境变量..."
export GAODE_KEY="6d467c5a115a42a99f49125fc4fc1bac"
export API_KEY="sk-73bcaaf1038d435da7ed32bdeeb42d9a"
export BASE_URL="http://localhost:8000/v1"
export MODEL_NAME="gpt-4o-mini"

echo "已设置环境变量："
echo "GAODE_KEY=$GAODE_KEY"
echo "API_KEY=$API_KEY"
echo "BASE_URL=$BASE_URL"
echo "MODEL_NAME=$MODEL_NAME"

echo "\n正在使用修复脚本运行程序..."
python fix_imports.py