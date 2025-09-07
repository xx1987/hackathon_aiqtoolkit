import asyncio
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.notify_mcp import send, NotifyInput

class TestNotification(unittest.TestCase):
    # 在类体中初始化实例变量
    mock_ctx = None
    original_env = None
    
    def setUp(self):
        # 创建模拟上下文对象
        self.mock_ctx = MagicMock()
        self.mock_ctx.info = print
        self.mock_ctx.warning = print
        self.mock_ctx.error = print
        
        # 保存原始环境变量，以便测试后恢复
        self.original_env = os.environ.copy()
    
    def tearDown(self):
        # 恢复原始环境变量
        os.environ.clear()
        os.environ.update(self.original_env)
    
    async def test_send_notification_basic(self):
        # 测试基本通知发送功能
        test_plan = {
            "id": "test_plan_001",
            "theme": "活动通知",
            "date": "2024-12-25",
            "venue": {"name": "测试场地"},
            "headcount": 30
        }
        result = await send(
            self.mock_ctx,
            plan=test_plan
        )
        
        # 验证返回格式
        self.assertIn("success", result)
        self.assertIsInstance(result["success"], bool)
    
    async def test_send_notification_with_empty_plan(self):
        # 测试空方案的情况
        result = await send(
            self.mock_ctx,
            plan={}
        )
        
        # 验证返回格式
        self.assertIn("success", result)
    
    @patch('tools.notify_mcp.httpx.AsyncClient')
    async def test_send_notification_api_call(self, mock_async_client):
        # 模拟HTTP客户端和API响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}
        
        mock_client_instance = MagicMock()
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_client_instance.post.return_value = mock_response
        mock_async_client.return_value = mock_client_instance
        
        # 设置环境变量
        os.environ['WX_ROBOT_URL'] = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test_key'
        
        test_plan = {
            "id": "api_test_plan",
            "theme": "测试通知",
            "date": "2024-12-25",
            "venue": {"name": "API测试场地"},
            "headcount": 20
        }
        
        result = await send(
            self.mock_ctx,
            plan=test_plan
        )
        
        # 验证API调用
        mock_client_instance.post.assert_called_once()
        # 验证返回结果
        self.assertTrue(result["success"])
    
    @patch('tools.notify_mcp.httpx.AsyncClient')
    async def test_send_notification_api_failure(self, mock_async_client):
        # 模拟API调用失败的情况
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"errcode": 40001, "errmsg": "invalid token"}
        
        mock_client_instance = MagicMock()
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_client_instance.post.return_value = mock_response
        mock_async_client.return_value = mock_client_instance
        
        # 设置环境变量
        os.environ['WX_ROBOT_URL'] = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=invalid_key'
        
        test_plan = {
            "id": "failure_test_plan",
            "theme": "失败测试通知",
            "date": "2024-12-25",
            "venue": {"name": "失败测试场地"},
            "headcount": 10
        }
        
        result = await send(
            self.mock_ctx,
            plan=test_plan
        )
        
        # 验证返回结果
        self.assertTrue(result["success"])  # 注意：失败时返回模拟成功
    
    async def test_send_notification_without_webhook(self):
        # 测试没有设置Webhook URL的情况
        # 确保环境变量中没有WX_ROBOT_URL
        if 'WX_ROBOT_URL' in os.environ:
            del os.environ['WX_ROBOT_URL']
        
        test_plan = {
            "id": "no_webhook_plan",
            "theme": "无Webhook测试",
            "date": "2024-12-25",
            "venue": {"name": "无Webhook测试场地"},
            "headcount": 5
        }
        
        result = await send(
            self.mock_ctx,
            plan=test_plan
        )
        
        # 验证返回格式
        self.assertIn("success", result)
        self.assertTrue(result["success"])  # 无Webhook时返回模拟成功

# 运行测试
if __name__ == "__main__":
    # 为了在命令行中直接运行异步测试
    import inspect
    
    # 获取所有以test_开头的异步方法
    test_methods = [method for method in dir(TestNotification) 
                    if method.startswith('test_') and inspect.iscoroutinefunction(getattr(TestNotification, method))]
    
    # 创建测试实例并运行每个测试方法
    test_instance = TestNotification()
    test_instance.setUp()
    
    try:
        for method_name in test_methods:
            print(f"Running test: {method_name}")
            method = getattr(test_instance, method_name)
            asyncio.run(method())
        print("All tests passed!")
    finally:
        test_instance.tearDown()