#!/bin/bash

# 启动所有MCP服务的脚本
echo "正在启动主题党日智能体MCP服务..."
echo "============================================="

# 停止可能已经在运行的服务
echo "停止现有服务..."
pkill -f "uvicorn.*800[1-4]" 2>/dev/null || true
sleep 2

# 启动venue_mcp服务 (端口8001)
echo "启动场地搜索服务 (端口8001)..."
uvicorn tools.venue_mcp:mcp --host 0.0.0.0 --port 8001 > venue_mcp.log 2>&1 &
VENUE_PID=$!
echo "场地搜索服务已启动 (PID: $VENUE_PID)"

# 启动calendar_mcp服务 (端口8002)
echo "启动日历检查服务 (端口8002)..."
uvicorn tools.calendar_mcp:mcp --host 0.0.0.0 --port 8002 > calendar_mcp.log 2>&1 &
CALENDAR_PID=$!
echo "日历检查服务已启动 (PID: $CALENDAR_PID)"

# 启动notify_mcp服务 (端口8003)
echo "启动通知发送服务 (端口8003)..."
uvicorn tools.notify_mcp:mcp --host 0.0.0.0 --port 8003 > notify_mcp.log 2>&1 &
NOTIFY_PID=$!
echo "通知发送服务已启动 (PID: $NOTIFY_PID)"

# 启动summary_mcp服务 (端口8004)
echo "启动总结生成服务 (端口8004)..."
uvicorn tools.summary_mcp:app --host 0.0.0.0 --port 8004 > summary_mcp.log 2>&1 &
SUMMARY_PID=$!
echo "总结生成服务已启动 (PID: $SUMMARY_PID)"

# 等待服务启动
sleep 3

# 检查服务状态
echo -e "\n检查服务状态..."
netstat -tlnp | grep -E ':800[1-4]' | head -10

echo -e "\n✅ 所有MCP服务已启动完成！"
echo "============================================="
echo "服务端口分配："
echo "- 场地搜索服务: http://localhost:8001"
echo "- 日历检查服务: http://localhost:8002"
echo "- 通知发送服务: http://localhost:8003"
echo "- 总结生成服务: http://localhost:8004"
echo "- 主智能体服务: http://localhost:8000"
echo ""
echo "日志文件："
echo "- venue_mcp.log: 场地搜索服务日志"
echo "- calendar_mcp.log: 日历检查服务日志"
echo "- notify_mcp.log: 通知发送服务日志"
echo "- summary_mcp.log: 总结生成服务日志"
echo ""
echo "现在可以运行智能体了："
echo "python fix_imports.py"
echo "或者使用真实API运行："
echo "./run_with_real_apis.sh"
echo ""
echo "要停止所有服务，运行："
echo "pkill -f 'uvicorn.*800[1-4]'"

# 保存PID到文件
echo "$VENUE_PID $CALENDAR_PID $NOTIFY_PID $SUMMARY_PID" > mcp_services.pid

echo -e "\n服务启动完成！现在可以运行主题党日智能体了。"