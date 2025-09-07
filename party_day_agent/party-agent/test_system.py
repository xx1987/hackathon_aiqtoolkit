#!/usr/bin/env python3
import requests
import subprocess
import time
import os
import sys

def print_success(message):
    print(f"\033[92m✓ {message}\033[0m")

def print_error(message):
    print(f"\033[91m✗ {message}\033[0m")

def print_info(message):
    print(f"\033[94m{message}\033[0m")

def is_process_running(process_name):
    try:
        # 使用pgrep命令检查进程是否在运行
        subprocess.check_output(f"pgrep -f '{process_name}'", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_service(url, timeout=3):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def start_frontend():
    print_info("尝试启动前端服务...")
    try:
        # 停止可能存在的前端进程
        subprocess.run("pkill -f 'python run_frontend.py' || true", shell=True)
        time.sleep(1)
        
        # 检查8081端口是否被占用
        port_used = subprocess.call("netstat -tuln | grep 8081", shell=True) == 0
        if port_used:
            print_error("端口 8081 被占用，请先停止占用该端口的进程")
            return False
        
        # 在后台启动前端服务
        subprocess.Popen(["python", "run_frontend.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())
        print_success("前端服务已在后台启动")
        return True
    except Exception as e:
        print_error(f"启动前端服务时出错: {e}")
        return False

def test_system():
    print_info("主题党日智能体系统测试")
    print_info("=" * 50)
    
    # 检查进程是否在运行
    services = [
        ("后端服务", "python planner.py"),
        ("前端服务", "python run_frontend.py"),
        ("日历检查工具", "python -m tools.calendar_mcp"),
        ("通知发送工具", "python -m tools.notify_mcp"),
        ("总结生成工具", "python -m tools.summary_mcp"),
        ("场地搜索工具", "python -m tools.venue_mcp")
    ]
    
    running_services = 0
    all_processes_running = True
    for service_name, process_name in services:
        if is_process_running(process_name):
            print_success(f"{service_name} 正在运行")
            running_services += 1
        else:
            print_error(f"{service_name} 未在运行")
            all_processes_running = False
    
    print_info("\n服务端点测试")
    print_info("=" * 50)
    
    # 检查服务端点
    endpoints = [
        ("后端API", "http://localhost:8000/docs"),
        ("前端界面", "http://localhost:8081/frontend.html")
    ]
    
    accessible_endpoints = 0
    all_endpoints_accessible = True
    for endpoint_name, url in endpoints:
        if check_service(url):
            print_success(f"{endpoint_name} 可访问: {url}")
            accessible_endpoints += 1
        else:
            print_error(f"{endpoint_name} 不可访问: {url}")
            all_endpoints_accessible = False
    
    print_info("\n系统测试总结")
    print_info("=" * 50)
    
    # 计算系统健康状态
    health_score = (running_services + accessible_endpoints) / (len(services) + len(endpoints)) * 100
    print_info(f"系统健康度: {health_score:.1f}%")
    
    if all_processes_running and all_endpoints_accessible:
        print_success("恭喜！主题党日智能体系统所有服务运行正常！")
    else:
        print_error("警告：主题党日智能体系统存在服务问题。")
        print_info(f"- 运行中服务: {running_services}/{len(services)}")
        print_info(f"- 可访问端点: {accessible_endpoints}/{len(endpoints)}")
        
        # 如果前端服务没有运行，提供启动选项
        if not is_process_running("python run_frontend.py"):
            print_info("\n是否尝试启动前端服务？(y/n)")
            user_input = input().strip().lower()
            if user_input == 'y':
                start_frontend()
                print_info("\n5秒后再次检查前端服务状态...")
                time.sleep(5)
                if is_process_running("python run_frontend.py"):
                    print_success("前端服务已成功启动！")
                else:
                    print_error("前端服务启动失败，请手动检查。")
    
    print_info("\n使用指南:")
    print_info("1. 前端界面: http://localhost:8081/frontend.html")
    print_info("2. API文档: http://localhost:8000/docs")
    print_info("3. 停止服务: ./stop_full_system.sh")
    print_info("4. 启动全部服务: ./start_full_system.sh")
    print_info("5. 重新测试系统: python test_system.py")

if __name__ == "__main__":
    test_system()