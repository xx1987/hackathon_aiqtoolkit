#!/bin/bash

# 主题党日智能体 - 真实API运行脚本
# 此脚本用于使用真实API密钥运行主题党日智能体，而不是使用模拟数据

# 注意：在运行前，请确保已经设置了真实的API密钥环境变量
# 可以通过以下方式临时设置（替换为您的实际密钥）：
# export AIQ_LLM_API_KEY="your_real_api_key"
# export GAODE_KEY="your_real_gaode_key"

# 检查是否已设置API密钥环境变量
check_api_keys() {
    # 检查大模型API密钥
    if [ -z "$AIQ_LLM_API_KEY" ]; then
        echo "警告: AIQ_LLM_API_KEY 环境变量未设置，将使用默认值"
        # 如果未设置，使用代码中的默认值
        export AIQ_LLM_API_KEY="sk-73bcaaf1038d435da7ed32bdeeb42d9a"
    fi
    
    # 检查高德地图API密钥
    if [ -z "$GAODE_KEY" ]; then
        echo "警告: GAODE_KEY 环境变量未设置，将使用默认值"
        export GAODE_KEY="6d467c5a115a42a99f49125fc4fc1bac"
    fi
    
    # 设置其他必要的环境变量
    if [ -z "$AIQ_LLM_BASE_URL" ]; then
        export AIQ_LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
    fi
    
    if [ -z "$AIQ_LLM_MODEL" ]; then
        export AIQ_LLM_MODEL="qwen-plus-2025-04-28"
    fi
    
    echo "正在使用以下配置运行智能体："
    echo "- AIQ_LLM_API_KEY: ${AIQ_LLM_API_KEY:0:6}********"  # 仅显示部分密钥以保护安全
    echo "- AIQ_LLM_BASE_URL: $AIQ_LLM_BASE_URL"
    echo "- AIQ_LLM_MODEL: $AIQ_LLM_MODEL"
    echo "- GAODE_KEY: ${GAODE_KEY:0:6}********"  # 仅显示部分密钥以保护安全
}

# 运行智能体
run_agent() {
    echo "\n正在启动主题党日智能体（真实API模式）..."
    echo "============================================="
    
    # 使用修复导入的脚本运行智能体
    python fix_imports.py
    
    # 检查执行结果
    if [ $? -eq 0 ]; then
        echo "\n✅ 主题党日智能体运行成功！"
        echo "============================================="
        echo "提示：如果需要使用您自己的真实API密钥，请在运行前设置环境变量："
        echo "export AIQ_LLM_API_KEY=您的真实API密钥"
        echo "export GAODE_KEY=您的真实高德地图API密钥"
    else
        echo "\n❌ 主题党日智能体运行失败！"
        echo "============================================="
        echo "可能的原因："
        echo "1. API密钥不正确"
        echo "2. 网络连接问题"
        echo "3. API服务暂时不可用"
        echo "\n建议：检查API密钥和网络连接，然后重试。"
    fi
}

# 主函数
main() {
    check_api_keys
    run_agent
}

# 运行主函数
main