import asyncio
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 尝试导入通知模块
try:
    from tools.notify_mcp import send, save_notification_to_file
except ImportError:
    print("无法导入通知模块，请检查路径是否正确")
    sys.exit(1)

class TestNotificationAlternatives(unittest.TestCase):
    def setUp(self):
        # 创建模拟上下文对象
        self.mock_ctx = MagicMock()
        self.mock_ctx.info = print
        self.mock_ctx.warning = print
        self.mock_ctx.error = print
        
        # 保存原始环境变量，以便测试后恢复
        self.original_env = os.environ.copy()
        
        # 测试数据
        self.test_plan = {
            "id": "test_plan_001",
            "theme": "测试通知替代方案",
            "date": "2024-12-25",
            "venue": {"name": "测试场地"},
            "headcount": 30
        }
    
    def tearDown(self):
        # 恢复原始环境变量
        os.environ.clear()
        os.environ.update(self.original_env)
    
    async def test_save_notification_to_file(self):
        """测试将通知保存到本地文件功能"""
        # 确保没有设置企业微信和邮件相关的环境变量
        if 'WX_ROBOT_URL' in os.environ:
            del os.environ['WX_ROBOT_URL']
        if 'EMAIL_SERVER' in os.environ:
            del os.environ['EMAIL_SERVER']
            
        # 执行发送通知函数
        result = await send(self.mock_ctx, plan=self.test_plan)
        
        # 验证返回结果
        self.assertTrue(result["success"], "通知应该返回成功")
        
        # 检查是否创建了notifications目录
        notifications_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notifications')
        self.assertTrue(os.path.exists(notifications_dir), "应该创建notifications目录")
        
        # 检查是否生成了通知文件
        files = os.listdir(notifications_dir)
        self.assertTrue(len(files) > 0, "应该生成至少一个通知文件")
        
        # 检查文件名是否包含方案ID
        plan_id = self.test_plan['id']
        has_plan_file = any(plan_id in filename for filename in files)
        self.assertTrue(has_plan_file, "应该生成包含方案ID的通知文件")
        
        # 打印生成的文件信息
        print(f"\n生成的通知文件:")
        for file in files:
            if plan_id in file:
                filepath = os.path.join(notifications_dir, file)
                print(f"- {filepath}")
                # 读取文件内容并打印前几行
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.readlines()
                    print("  文件内容预览:")
                    for line in content[:5]:  # 只打印前5行
                        print(f"  {line.strip()}")
                    print("  ...")
    
    @patch('tools.notify_mcp.save_notification_to_file')
    @patch('tools.notify_mcp.ENABLE_EMAIL', False)
    async def test_no_notification_methods(self, mock_save_to_file):
        """测试没有配置任何通知方式的情况"""
        # 模拟保存文件成功
        mock_save_to_file.return_value = True
        
        # 确保没有设置企业微信相关的环境变量
        if 'WX_ROBOT_URL' in os.environ:
            del os.environ['WX_ROBOT_URL']
        
        # 执行发送通知函数
        result = await send(self.mock_ctx, plan=self.test_plan)
        
        # 验证返回结果
        self.assertTrue(result["success"], "即使没有配置通知方式，也应该返回成功")
        mock_save_to_file.assert_called_once()
    
    @patch('tools.notify_mcp.save_notification_to_file')
    async def test_multiple_notification_methods(self, mock_save_to_file):
        """测试配置了多种通知方式的情况"""
        # 模拟保存文件成功
        mock_save_to_file.return_value = True
        
        # 设置企业微信环境变量（使用无效URL以便触发异常）
        os.environ['WX_ROBOT_URL'] = 'http://invalid-url-for-testing'
        
        # 执行发送通知函数
        result = await send(self.mock_ctx, plan=self.test_plan)
        
        # 验证返回结果
        self.assertTrue(result["success"], "即使部分通知方式失败，只要有一个成功就应该返回成功")
        mock_save_to_file.assert_called_once()

# 运行测试
if __name__ == "__main__":
    # 为了在命令行中直接运行异步测试
    import inspect
    
    # 获取所有以test_开头的异步方法
    test_methods = [method for method in dir(TestNotificationAlternatives) 
                    if method.startswith('test_') and inspect.iscoroutinefunction(getattr(TestNotificationAlternatives, method))]
    
    # 创建测试实例并运行每个测试方法
    test_instance = TestNotificationAlternatives()
    test_instance.setUp()
    
    try:
        for method_name in test_methods:
            print(f"\n运行测试: {method_name}")
            method = getattr(test_instance, method_name)
            asyncio.run(method())
        print("\n所有测试通过!")
    finally:
        test_instance.tearDown()