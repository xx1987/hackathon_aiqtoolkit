#!/usr/bin/env python3
import os
import sys
import requests
import subprocess
import time

# 颜色定义
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    NC = '\033[0m'  # 无颜色

# 打印函数
def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.NC}")

def print_info(message):
    print(f"{Colors.BLUE}{message}{Colors.NC}")

def print_warning(message):
    print(f"{Colors.YELLOW}! {message}{Colors.NC}")

# 检查进程是否在运行
def is_process_running(process_name):
    try:
        result = subprocess.run(f"pgrep -f '{process_name}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pids = result.stdout.strip().split('\n')
        return len(pids) > 0 and pids[0] != ''
    except Exception:
        return False

# 获取进程PID
def get_process_pid(process_name):
    try:
        result = subprocess.run(f"pgrep -f '{process_name}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pids = result.stdout.strip().split('\n')
        if len(pids) > 0 and pids[0] != '':
            return pids
    except Exception:
        pass
    return []

# 检查端口占用情况
def check_port_usage(port):
    try:
        result = subprocess.run(f"netstat -tuln | grep {port}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception:
        return "无法获取端口信息"

# 检查文件是否存在
def check_file_exists(file_path):
    return os.path.exists(file_path)

# 检查前端文件内容
def check_frontend_file():    
    frontend_file = "frontend.html"
    if not check_file_exists(frontend_file):
        print_error(f"前端文件 {frontend_file} 不存在")
        return False
    
    # 检查文件大小
    file_size = os.path.getsize(frontend_file)
    if file_size == 0:
        print_error(f"前端文件 {frontend_file} 为空")
        return False
    
    print_success(f"前端文件 {frontend_file} 存在，大小: {file_size} 字节")
    return True

# 尝试不同的访问方式
def test_frontend_access():
    print_info("\n测试前端访问方式...")
    
    urls = [
        ("标准URL", "http://localhost:8081/frontend.html"),
        ("IP地址", "http://127.0.0.1:8081/frontend.html"),
        ("根路径", "http://localhost:8081"),
        ("无扩展名", "http://localhost:8081/frontend")
    ]
    
    success = False
    for name, url in urls:
        try:
            print_info(f"测试 {name}: {url}")
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print_success(f"✓ 成功访问 {name}，状态码: {response.status_code}")
                success = True
                break
            else:
                print_error(f"✗ 访问 {name} 失败，状态码: {response.status_code}")
        except Exception as e:
            print_error(f"✗ 访问 {name} 异常: {str(e)}")
    
    return success

# 检查防火墙设置
def check_firewall():
    print_info("\n检查防火墙设置...")
    try:
        result = subprocess.run("iptables -L -n", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "8081" in result.stdout:
            print_warning("发现防火墙规则中包含8081端口")
            print(result.stdout)
        else:
            print_success("未发现8081端口的防火墙限制")
    except Exception:
        print_warning("无法检查防火墙设置")

# 主诊断函数
def diagnose_frontend():
    print_info("=" * 60)
    print_info("主题党日智能体前端服务诊断工具")
    print_info("=" * 60)
    
    # 1. 检查前端服务进程
    print_info("\n1. 检查前端服务进程...")
    frontend_process = "python run_frontend.py"
    if is_process_running(frontend_process):
        pids = get_process_pid(frontend_process)
        print_success(f"前端服务正在运行，PID: {', '.join(pids)}")
        
        # 检查资源使用情况
        for pid in pids:
            try:
                result = subprocess.run(f"ps -p {pid} -o %cpu,%mem,cmd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print_info(f"PID {pid} 资源使用情况:")
                print(result.stdout)
            except Exception:
                print_warning(f"无法获取PID {pid} 的资源使用情况")
    else:
        print_error("前端服务未在运行")
        return
    
    # 2. 检查8081端口
    print_info("\n2. 检查8081端口占用...")
    port_info = check_port_usage(8081)
    if port_info:
        print_success(f"端口8081被占用:")
        print(port_info)
    else:
        print_error("端口8081未被占用")
        return
    
    # 3. 检查前端文件
    print_info("\n3. 检查前端文件...")
    if not check_frontend_file():
        return
    
    # 4. 测试访问方式
    print_info("\n4. 测试前端访问...")
    access_success = test_frontend_access()
    
    # 5. 检查防火墙
    check_firewall()
    
    # 6. 提供诊断报告和建议
    print_info("\n" + "=" * 60)
    print_info("诊断报告")
    print_info("=" * 60)
    
    if access_success:
        print_success("前端服务访问成功！")
    else:
        print_error("前端服务访问失败")
        print_info("\n建议解决方案:")
        print_info("1. 确认前端服务是否正确绑定到了0.0.0.0地址")
        print_info("2. 尝试使用不同的浏览器访问")
        print_info("3. 检查网络代理设置")
        print_info("4. 尝试重启前端服务: kill -9 PID && python run_frontend.py")
        print_info("5. 检查run_frontend.py中的服务器配置")
    
    print_info("\n诊断完成！")

if __name__ == "__main__":
    diagnose_frontend()