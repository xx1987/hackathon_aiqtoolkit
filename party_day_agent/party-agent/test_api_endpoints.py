#!/usr/bin/env python3
"""
测试API端点的脚本

此脚本用于测试主题党日智能体的API端点是否正常工作，
包括检查服务健康状态和下载报告功能。
"""
import urllib.request
import urllib.error
import json
import sys
import os

# 检查planner.py是否在运行中
def check_server_running():
    print("检查planner.py服务器是否在运行中...")
    try:
        # 尝试访问健康检查端点
        url = "http://localhost:8000/health"
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print(f"服务器健康状态: {data}")
                return True
            else:
                print(f"服务器响应状态码: {response.status}")
                return False
    except urllib.error.URLError as e:
        print(f"无法连接到服务器: {e}")
        print("注意: 这可能是因为planner.py没有在后台运行")
        return False

# 测试下载报告功能
def test_download_report():
    print("\n测试下载报告功能...")
    event_id = "123"
    url = f"http://localhost:8000/files/{event_id}_summary.docx"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            print(f"API调用返回状态码: {response.status}")
            
            # 检查响应头
            content_disposition = response.getheader('Content-Disposition')
            if content_disposition:
                print(f"Content-Disposition响应头: {content_disposition}")
            
            # 读取响应内容
            content = response.read().decode()
            print(f"响应内容长度: {len(content)} 字符")
            
            # 尝试解析JSON
            try:
                data = json.loads(content)
                print("成功解析JSON内容")
                
                # 检查必要的字段
                if "event_id" in data and data["event_id"] == event_id:
                    print(f"验证通过: event_id 正确 ({event_id})")
                else:
                    print("警告: JSON内容中未找到正确的event_id")
                
                print("JSON内容概览:")
                for key in data:
                    print(f"  - {key}: {type(data[key]).__name__}")
                
            except json.JSONDecodeError:
                print("响应内容不是有效的JSON格式")
                print(f"前100个字符: {content[:100]}...")
                
    except urllib.error.URLError as e:
        print(f"API调用失败: {e}")
        print(f"请确保planner.py正在运行，或尝试访问正确的端点")

# 主函数
def main():
    print("=== 主题党日智能体API端点测试 ===")
    
    # 检查服务器状态
    server_running = check_server_running()
    
    # 测试下载报告功能
    test_download_report()
    
    # 提供使用说明
    print("\n=== 使用说明 ===")
    print("1. 确保planner.py在后台运行:")
    print("   python planner.py")
    print("")
    print("2. 设置API环境变量后运行程序:")
    print("   ./run_with_mock_apis.sh")
    print("")
    print("3. 在实际环境中，替换为真实的API密钥:")
    print("   export GAODE_KEY=your_real_gaode_key")
    print("   export API_KEY=your_real_llm_key")
    print("   export BASE_URL=your_real_api_base_url")
    print("   export MODEL_NAME=your_real_model_name")

if __name__ == "__main__":
    main()