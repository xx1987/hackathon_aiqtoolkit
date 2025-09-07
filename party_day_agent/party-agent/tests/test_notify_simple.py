import asyncio
import os
import sys
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 尝试导入通知模块
try:
    from tools.notify_mcp import send
    print("成功导入通知模块")
except ImportError as e:
    print(f"导入通知模块失败: {e}")
    sys.exit(1)

# 创建模拟上下文对象
class MockContext:
    def info(self, message):
        print(f"[INFO] {message}")
    
    def warning(self, message):
        print(f"[WARNING] {message}")
    
    def error(self, message):
        print(f"[ERROR] {message}")

# 测试数据
test_plan = {
    "id": "test_plan_simple_001",
    "theme": "测试通知替代方案（简化版）",
    "date": "2024-12-25",
    "venue": {"name": "测试场地"},
    "headcount": 30
}

async def main():
    print("\n===== 开始测试通知替代方案 =====")
    print(f"测试数据: {json.dumps(test_plan, ensure_ascii=False)}")
    
    # 创建模拟上下文
    ctx = MockContext()
    
    # 确保没有设置企业微信相关的环境变量
    if 'WX_ROBOT_URL' in os.environ:
        print(f"注意: 环境中存在WX_ROBOT_URL，将尝试使用它发送通知")
    
    # 执行发送通知函数
    print("\n开始发送通知...")
    try:
        result = await send(ctx, plan=test_plan)
        print(f"\n通知发送结果: {json.dumps(result, ensure_ascii=False)}")
        
        # 检查是否创建了notifications目录
        notifications_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notifications')
        print(f"\n检查通知目录: {notifications_dir}")
        
        if os.path.exists(notifications_dir):
            print("通知目录已创建")
            # 列出目录中的文件
            files = os.listdir(notifications_dir)
            print(f"目录中的文件数量: {len(files)}")
            
            # 查找包含测试计划ID的文件
            plan_id = test_plan['id']
            found_files = [f for f in files if plan_id in f]
            print(f"找到的相关通知文件数量: {len(found_files)}")
            
            # 显示找到的文件内容预览
            for file in found_files:
                filepath = os.path.join(notifications_dir, file)
                print(f"\n文件: {filepath}")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"文件大小: {len(content)} 字节")
                        # 打印文件内容摘要
                        if len(content) > 500:
                            print(f"内容前500字节:\n{content[:500]}...")
                        else:
                            print(f"完整内容:\n{content}")
                except Exception as e:
                    print(f"读取文件失败: {e}")
        else:
            print("通知目录未创建")
            
    except Exception as e:
        print(f"发送通知时发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n===== 测试完成 =====")

# 运行测试
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"运行测试时发生错误: {e}")
        import traceback
        traceback.print_exc()