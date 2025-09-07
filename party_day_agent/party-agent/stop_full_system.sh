#!/bin/bash

# 停止主题党日智能体的所有服务

# 设置颜色变量
green='\033[0;32m'
red='\033[0;31m'
blue='\033[0;34m'
nc='\033[0m' # 无颜色

# 停止后端服务
echo -e "\n\033[0;34m正在停止后端服务...\033[0m"
if pgrep -f "python planner.py" > /dev/null; then
    pkill -f "python planner.py"
    echo -e "\033[0;32m后端服务已停止！\033[0m"
else
    echo -e "\033[0;34m后端服务未在运行中。\033[0m"
fi

# 停止前端服务
echo -e "\n\033[0;34m正在停止前端服务...\033[0m"
if pgrep -f "python run_frontend.py" > /dev/null; then
    pkill -f "python run_frontend.py"
    echo -e "\033[0;32m前端服务已停止！\033[0m"
else
    echo -e "\033[0;34m前端服务未在运行中。\033[0m"
fi

# 停止日历检查工具服务
echo -e "\n\033[0;34m正在停止日历检查工具服务...\033[0m"
if pgrep -f "python -m tools.calendar_mcp" > /dev/null; then
    pkill -f "python -m tools.calendar_mcp"
    echo -e "\033[0;32m日历检查工具服务已停止！\033[0m"
else
    echo -e "\033[0;34m日历检查工具服务未在运行中。\033[0m"
fi

# 停止通知发送工具服务
echo -e "\n\033[0;34m正在停止通知发送工具服务...\033[0m"
if pgrep -f "python -m tools.notify_mcp" > /dev/null; then
    pkill -f "python -m tools.notify_mcp"
    echo -e "\033[0;32m通知发送工具服务已停止！\033[0m"
else
    echo -e "\033[0;34m通知发送工具服务未在运行中。\033[0m"
fi

# 停止总结生成工具服务
echo -e "\n\033[0;34m正在停止总结生成工具服务...\033[0m"
if pgrep -f "python -m tools.summary_mcp" > /dev/null; then
    pkill -f "python -m tools.summary_mcp"
    echo -e "\033[0;32m总结生成工具服务已停止！\033[0m"
else
    echo -e "\033[0;34m总结生成工具服务未在运行中。\033[0m"
fi

# 停止场地搜索工具服务
echo -e "\n\033[0;34m正在停止场地搜索工具服务...\033[0m"
if pgrep -f "python -m tools.venue_mcp" > /dev/null; then
    pkill -f "python -m tools.venue_mcp"
    echo -e "\033[0;32m场地搜索工具服务已停止！\033[0m"
else
    echo -e "\033[0;34m场地搜索工具服务未在运行中。\033[0m"
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
echo -e "\n\033[0;32m所有服务已停止！\033[0m"
echo -e "如需重新启动，请运行： ./start_full_system.sh"
