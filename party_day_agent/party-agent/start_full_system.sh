#!/bin/bash

# 主题党日智能体 - 完整系统启动脚本
# 此脚本用于同时启动前端、后端和所有工具服务，方便您进行完整的测试

# 设置颜色变量
green='\033[0;32m'
red='\033[0;31m'
blue='\033[0;34m'
nc='\033[0m' # 无颜色

# 检查是否已设置API密钥环境变量
check_api_keys() {
    echo -e "${blue}检查API密钥配置...${nc}"
    
    # 检查大模型API密钥
    if [ -z "$AIQ_LLM_API_KEY" ]; then
        echo -e "${blue}警告: AIQ_LLM_API_KEY 环境变量未设置，将使用默认值${nc}"
        # 如果未设置，使用代码中的默认值
        export AIQ_LLM_API_KEY="sk-73bcaaf1038d435da7ed32bdeeb42d9a"
    fi
    
    # 检查高德地图API密钥
    if [ -z "$GAODE_KEY" ]; then
        echo -e "${blue}警告: GAODE_KEY 环境变量未设置，将使用默认值${nc}"
        export GAODE_KEY="6d467c5a115a42a99f49125fc4fc1bac"
    fi
    
    # 设置其他必要的环境变量
    if [ -z "$AIQ_LLM_BASE_URL" ]; then
        export AIQ_LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
    fi
    
    if [ -z "$AIQ_LLM_MODEL" ]; then
        export AIQ_LLM_MODEL="qwen-plus-2025-04-28"
    fi
    
    echo -e "${green}正在使用以下配置运行智能体：${nc}"
    echo -e "- AIQ_LLM_API_KEY: ${AIQ_LLM_API_KEY:0:6}********"  # 仅显示部分密钥以保护安全
    echo -e "- AIQ_LLM_BASE_URL: $AIQ_LLM_BASE_URL"
    echo -e "- AIQ_LLM_MODEL: $AIQ_LLM_MODEL"
    echo -e "- GAODE_KEY: ${GAODE_KEY:0:6}********"  # 仅显示部分密钥以保护安全
}

# 启动后端服务
start_backend() {
    echo -e "\n${blue}正在启动后端服务...${nc}"
    echo -e "----------------------------------------"
    
    # 检查是否已有后端服务在运行
    if pgrep -f "python planner.py" > /dev/null; then
        echo -e "${green}后端服务已经在运行中！${nc}"
        echo -e "访问 http://localhost:8000/docs 查看API文档"
    else
        # 在新终端中启动后端服务
        echo -e "${blue}启动后端服务，请查看相应终端窗口...${nc}"
        python planner.py &
        BACKEND_PID=$!
        echo $BACKEND_PID > .backend.pid
        sleep 2  # 等待服务启动
        
        # 检查后端服务是否启动成功
        if ps -p $BACKEND_PID > /dev/null; then
            echo -e "${green}后端服务启动成功！${nc}"
            echo -e "访问 http://localhost:8000/docs 查看API文档"
        else
            echo -e "${red}后端服务启动失败！${nc}"
        fi
    fi
    echo -e "----------------------------------------"
}

# 启动日历检查工具服务
start_calendar_tool() {
    echo -e "\n${blue}正在启动日历检查工具服务...${nc}"
    echo -e "----------------------------------------"
    
    # 检查是否已有日历检查工具服务在运行
    if pgrep -f "python -m tools.calendar_mcp" > /dev/null; then
        echo -e "${green}日历检查工具服务已经在运行中！${nc}"
    else
        # 在新终端中启动日历检查工具服务
        echo -e "${blue}启动日历检查工具服务，请查看相应终端窗口...${nc}"
        python -m tools.calendar_mcp &
        CALENDAR_PID=$!
        echo $CALENDAR_PID > .calendar.pid
        sleep 1  # 等待服务启动
        
        # 检查日历检查工具服务是否启动成功
        if ps -p $CALENDAR_PID > /dev/null; then
            echo -e "${green}日历检查工具服务启动成功！${nc}"
        else
            echo -e "${red}日历检查工具服务启动失败！${nc}"
        fi
    fi
    echo -e "----------------------------------------"
}

# 启动通知发送工具服务
start_notify_tool() {
    echo -e "\n${blue}正在启动通知发送工具服务...${nc}"
    echo -e "----------------------------------------"
    
    # 检查是否已有通知发送工具服务在运行
    if pgrep -f "python -m tools.notify_mcp" > /dev/null; then
        echo -e "${green}通知发送工具服务已经在运行中！${nc}"
    else
        # 在新终端中启动通知发送工具服务
        echo -e "${blue}启动通知发送工具服务，请查看相应终端窗口...${nc}"
        python -m tools.notify_mcp &
        NOTIFY_PID=$!
        echo $NOTIFY_PID > .notify.pid
        sleep 1  # 等待服务启动
        
        # 检查通知发送工具服务是否启动成功
        if ps -p $NOTIFY_PID > /dev/null; then
            echo -e "${green}通知发送工具服务启动成功！${nc}"
        else
            echo -e "${red}通知发送工具服务启动失败！${nc}"
        fi
    fi
    echo -e "----------------------------------------"
}

# 启动总结生成工具服务
start_summary_tool() {
    echo -e "\n${blue}正在启动总结生成工具服务...${nc}"
    echo -e "----------------------------------------"
    
    # 检查是否已有总结生成工具服务在运行
    if pgrep -f "python -m tools.summary_mcp" > /dev/null; then
        echo -e "${green}总结生成工具服务已经在运行中！${nc}"
    else
        # 在新终端中启动总结生成工具服务
        echo -e "${blue}启动总结生成工具服务，请查看相应终端窗口...${nc}"
        python -m tools.summary_mcp &
        SUMMARY_PID=$!
        echo $SUMMARY_PID > .summary.pid
        sleep 1  # 等待服务启动
        
        # 检查总结生成工具服务是否启动成功
        if ps -p $SUMMARY_PID > /dev/null; then
            echo -e "${green}总结生成工具服务启动成功！${nc}"
        else
            echo -e "${red}总结生成工具服务启动失败！${nc}"
        fi
    fi
    echo -e "----------------------------------------"
}

# 启动场地搜索工具服务
start_venue_tool() {
    echo -e "\n${blue}正在启动场地搜索工具服务...${nc}"
    echo -e "----------------------------------------"
    
    # 检查是否已有场地搜索工具服务在运行
    if pgrep -f "python -m tools.venue_mcp" > /dev/null; then
        echo -e "${green}场地搜索工具服务已经在运行中！${nc}"
    else
        # 在新终端中启动场地搜索工具服务
        echo -e "${blue}启动场地搜索工具服务，请查看相应终端窗口...${nc}"
        python -m tools.venue_mcp &
        VENUE_PID=$!
        echo $VENUE_PID > .venue.pid
        sleep 1  # 等待服务启动
        
        # 检查场地搜索工具服务是否启动成功
        if ps -p $VENUE_PID > /dev/null; then
            echo -e "${green}场地搜索工具服务启动成功！${nc}"
        else
            echo -e "${red}场地搜索工具服务启动失败！${nc}"
        fi
    fi
    echo -e "----------------------------------------"
}

# 启动所有MCP工具服务
start_all_tools() {
    echo -e "\n${blue}正在启动所有MCP工具服务...${nc}"
    start_calendar_tool
    start_notify_tool
    start_summary_tool
    start_venue_tool
}

# 启动前端服务
start_frontend() {
    echo -e "\n${blue}正在启动前端服务...${nc}"
    echo -e "----------------------------------------"
    
    # 检查是否已有前端服务在运行
    if pgrep -f "python run_frontend.py" > /dev/null; then
        echo -e "${green}前端服务已经在运行中！${nc}"
        echo -e "访问 http://localhost:8081/frontend.html 查看前端界面"
    else
        # 在新终端中启动前端服务
        echo -e "${blue}启动前端服务，请查看相应终端窗口...${nc}"
        python run_frontend.py &
        FRONTEND_PID=$!
        echo $FRONTEND_PID > .frontend.pid
        sleep 2  # 等待服务启动
        
        # 检查前端服务是否启动成功
        if ps -p $FRONTEND_PID > /dev/null; then
            echo -e "${green}前端服务启动成功！${nc}"
            echo -e "访问 http://localhost:8081/frontend.html 查看前端界面"
        else
            echo -e "${red}前端服务启动失败！${nc}"
        fi
    fi
    echo -e "----------------------------------------"
}

# 运行测试脚本
run_test() {
    echo -e "\n${blue}正在运行智能体测试...${nc}"
    echo -e "----------------------------------------"
    
    # 运行智能体测试
    python demo.py
    
    # 检查测试是否成功
    if [ $? -eq 0 ]; then
        echo -e "${green}智能体测试运行成功！${nc}"
    else
        echo -e "${red}智能体测试运行失败！${nc}"
    fi
    echo -e "----------------------------------------"
}

# 创建停止服务的脚本
create_stop_script() {
    echo -e "\n${blue}创建停止服务脚本...${nc}"
    cat > stop_full_system.sh << EOF
#!/bin/bash

# 停止主题党日智能体的所有服务

# 设置颜色变量
green='\\033[0;32m'
red='\\033[0;31m'
blue='\\033[0;34m'
nc='\\033[0m' # 无颜色

# 停止后端服务
echo -e "\\n${blue}正在停止后端服务...${nc}"
if pgrep -f "python planner.py" > /dev/null; then
    pkill -f "python planner.py"
    echo -e "${green}后端服务已停止！${nc}"
else
    echo -e "${blue}后端服务未在运行中。${nc}"
fi

# 停止前端服务
echo -e "\\n${blue}正在停止前端服务...${nc}"
if pgrep -f "python run_frontend.py" > /dev/null; then
    pkill -f "python run_frontend.py"
    echo -e "${green}前端服务已停止！${nc}"
else
    echo -e "${blue}前端服务未在运行中。${nc}"
fi

# 停止日历检查工具服务
echo -e "\\n${blue}正在停止日历检查工具服务...${nc}"
if pgrep -f "python -m tools.calendar_mcp" > /dev/null; then
    pkill -f "python -m tools.calendar_mcp"
    echo -e "${green}日历检查工具服务已停止！${nc}"
else
    echo -e "${blue}日历检查工具服务未在运行中。${nc}"
fi

# 停止通知发送工具服务
echo -e "\\n${blue}正在停止通知发送工具服务...${nc}"
if pgrep -f "python -m tools.notify_mcp" > /dev/null; then
    pkill -f "python -m tools.notify_mcp"
    echo -e "${green}通知发送工具服务已停止！${nc}"
else
    echo -e "${blue}通知发送工具服务未在运行中。${nc}"
fi

# 停止总结生成工具服务
echo -e "\\n${blue}正在停止总结生成工具服务...${nc}"
if pgrep -f "python -m tools.summary_mcp" > /dev/null; then
    pkill -f "python -m tools.summary_mcp"
    echo -e "${green}总结生成工具服务已停止！${nc}"
else
    echo -e "${blue}总结生成工具服务未在运行中。${nc}"
fi

# 停止场地搜索工具服务
echo -e "\\n${blue}正在停止场地搜索工具服务...${nc}"
if pgrep -f "python -m tools.venue_mcp" > /dev/null; then
    pkill -f "python -m tools.venue_mcp"
    echo -e "${green}场地搜索工具服务已停止！${nc}"
else
    echo -e "${blue}场地搜索工具服务未在运行中。${nc}"
fi

# 清理pid文件
if [ -f .backend.pid ]; then
    rm .backend.pid
fi
if [ -f .frontend.pid ]; then
    rm .frontend.pid
fi
if [ -f .calendar.pid ]; then
    rm .calendar.pid
fi
if [ -f .notify.pid ]; then
    rm .notify.pid
fi
if [ -f .summary.pid ]; then
    rm .summary.pid
fi
if [ -f .venue.pid ]; then
    rm .venue.pid
fi

# 提示
echo -e "\\n${green}所有服务已停止！${nc}"
echo -e "如需重新启动，请运行： ./start_full_system.sh"
EOF
    chmod +x stop_full_system.sh
    echo -e "${green}停止服务脚本创建成功！${nc}"
    echo -e "运行 ./stop_full_system.sh 可以停止所有服务"
}

# 显示帮助信息
display_help() {
    echo -e "\n${blue}主题党日智能体使用指南：${nc}"
    echo -e "1. 前端界面：http://localhost:8081/frontend.html"
    echo -e "2. API文档：http://localhost:8000/docs"
    echo -e "3. 运行测试：python demo.py 或 ./run_with_real_apis.sh"
    echo -e "4. 停止服务：./stop_full_system.sh"
    echo -e "\n系统组件："
    echo -e "- 后端服务 (planner.py)：智能体核心，协调各工具服务"
    echo -e "- 前端服务 (run_frontend.py)：用户交互界面"
    echo -e "- 日历检查工具 (tools/calendar_mcp.py)：检查活动日期是否合适"
    echo -e "- 通知发送工具 (tools/notify_mcp.py)：发送活动通知"
    echo -e "- 总结生成工具 (tools/summary_mcp.py)：生成活动总结报告"
    echo -e "- 场地搜索工具 (tools/venue_mcp.py)：搜索适合的活动场地"
    echo -e "\n提示："
    echo -e "- 如需使用自己的API密钥，请在运行前设置环境变量："
    echo -e "  export AIQ_LLM_API_KEY=您的真实API密钥"
    echo -e "  export GAODE_KEY=您的真实高德地图API密钥"
    echo -e "- 详细文档请查看："
    echo -e "  - RUN_STATUS_SUMMARY.md - 当前运行状态总结"
    echo -e "  - API_KEY_CONFIGURATION.md - API密钥配置指南"
    echo -e "  - REAL_API_RUN_GUIDE.md - 真实API运行指南"
}

# 主函数
main() {
    echo -e "${green}主题党日智能体 - 完整系统启动脚本${nc}"
    echo -e "============================================="
    
    check_api_keys
    start_backend
    start_all_tools
    start_frontend
    create_stop_script
    display_help
    
    echo -e "\n${green}完整系统已成功启动！${nc}"
    echo -e "============================================="
    echo -e "您现在可以访问前端界面进行测试了：http://localhost:8081/frontend.html"
}

# 运行主函数
main