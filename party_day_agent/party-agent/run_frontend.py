#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
import webbrowser
import threading
import time

# 设置端口号
PORT = 8082

# 获取当前目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CURRENT_DIR, **kwargs)
        
    # 重写log_message方法，以便更好地控制输出
    def log_message(self, format, *args):
        # 可以在这里添加自定义日志逻辑
        pass

# 启动服务器
def start_server():
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"\n主题党日活动智能助手前端服务器启动成功！")
            print(f"请在浏览器中访问: http://localhost:{PORT}/frontend.html")
            print("\n提示:")
            print("- 按 Ctrl+C 停止服务器")
            print("- 如需与后端API交互，请确保后端服务已启动")
            print("- 当前页面使用模拟数据展示智能体运行效果")
            print("\n正在打开浏览器...")
            
            # 延迟打开浏览器，确保服务器已启动
            def open_browser():
                time.sleep(1)
                webbrowser.open(f"http://localhost:{PORT}/frontend.html")
                
            threading.Thread(target=open_browser).start()
            
            # 运行服务器
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
    except Exception as e:
        print(f"\n启动服务器时出错: {e}")
        print(f"\n请尝试以下解决方案:")
        print(f"1. 检查端口 {PORT} 是否已被占用")
        print(f"2. 尝试使用管理员权限运行此脚本")
        print(f"3. 修改脚本中的PORT变量为其他未使用的端口")

if __name__ == "__main__":
    # 打印欢迎信息
    print("="*60)
    print("主题党日活动智能助手前端服务器")
    print("="*60)
    print("此脚本将启动一个简单的HTTP服务器，用于运行智能体演示前端页面")
    print(f"当前目录: {CURRENT_DIR}")
    print(f"端口号: {PORT}")
    print("="*60)
    
    # 启动服务器
    start_server()