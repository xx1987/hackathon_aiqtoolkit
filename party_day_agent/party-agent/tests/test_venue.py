import asyncio
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.venue_mcp import search, VenueSearchInput, generate_mock_venues

class TestVenueSearch(unittest.TestCase):
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
    
    async def test_venue_search_basic(self):
        # 测试基本搜索功能
        result = await search(
            self.mock_ctx,
            theme="学习吴某文精神",
            headcount=30,
            lat=39.9042,
            lng=116.4074,
            radius_km=5
        )
        
        # 验证返回格式
        self.assertIsInstance(result, list)
        # 即使是模拟数据，也应该返回一些场地
        self.assertTrue(len(result) > 0)
        
        # 检查每个场地是否包含必要字段
        for venue in result:
            self.assertIn("name", venue)
            self.assertIn("address", venue)
            self.assertIn("capacity", venue)
            self.assertIn("lat", venue)
            self.assertIn("lng", venue)
    
    async def test_venue_search_with_different_params(self):
        # 测试不同参数的搜索
        result = await search(
            self.mock_ctx,
            theme="党史",
            headcount=50,
            lat=31.2304,
            lng=121.4737,
            radius_km=10
        )
        
        # 验证返回格式
        self.assertIsInstance(result, list)
    
    async def test_venue_search_with_zero_headcount(self):
        # 测试人数为0的情况
        result = await search(
            self.mock_ctx,
            theme="星期日",
            headcount=0,
            lat=39.9042,
            lng=116.4074,
            radius_km=5
        )
        
        # 即使人数为0，也应该返回一些场地
        self.assertIsInstance(result, list)
    
    @patch('tools.venue_mcp.httpx.AsyncClient')
    async def test_venue_search_api_call(self, mock_async_client):
        # 模拟HTTP客户端和API响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "1",
            "count": "3",
            "pois": [
                {"id": "poi_1", "name": "测试场地1", "address": "测试地址1", "location": "116.4074,39.9042", "type": "060400"},
                {"id": "poi_2", "name": "测试场地2", "address": "测试地址2", "location": "116.4174,39.9142", "type": "060400"},
                {"id": "poi_3", "name": "测试场地3", "address": "测试地址3", "location": "116.3974,39.8942", "type": "060400"}
            ]
        }
        
        mock_client_instance = MagicMock()
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None
        mock_client_instance.get.return_value = mock_response
        mock_async_client.return_value = mock_client_instance
        
        # 设置环境变量
        os.environ['GAODE_KEY'] = 'test_key'
        
        result = await search(
            self.mock_ctx,
            theme="测试主题",
            headcount=20,
            lat=39.9042,
            lng=116.4074,
            radius_km=5
        )
        
        # 验证API调用
        mock_client_instance.get.assert_called_once()
        # 验证返回结果
        self.assertEqual(len(result), 3)
    
    def test_generate_mock_venues(self):
        # 测试模拟场地生成函数
        mock_ctx = MagicMock()
        venues = generate_mock_venues(
            mock_ctx,
            theme="测试主题",
            headcount=20,
            lat=39.9042,
            lng=116.4074
        )
        
        # 验证生成的场地数量和格式
        self.assertEqual(len(venues), 5)
        for venue in venues:
            self.assertIn("name", venue)
            self.assertIn("address", venue)
            self.assertIn("capacity", venue)
            self.assertIn("lat", venue)
            self.assertIn("lng", venue)

# 运行测试
if __name__ == "__main__":
    # 为了在命令行中直接运行异步测试
    import inspect
    
    # 获取所有以test_开头的异步方法
    async_test_methods = [method for method in dir(TestVenueSearch) 
                         if method.startswith('test_') and inspect.iscoroutinefunction(getattr(TestVenueSearch, method))]
    
    # 获取所有以test_开头的同步方法
    sync_test_methods = [method for method in dir(TestVenueSearch) 
                        if method.startswith('test_') and not inspect.iscoroutinefunction(getattr(TestVenueSearch, method))]
    
    # 创建测试实例
    test_instance = TestVenueSearch()
    test_instance.setUp()
    
    try:
        # 运行同步测试
        for method_name in sync_test_methods:
            print(f"Running sync test: {method_name}")
            method = getattr(test_instance, method_name)
            method()
        
        # 运行异步测试
        for method_name in async_test_methods:
            print(f"Running async test: {method_name}")
            method = getattr(test_instance, method_name)
            asyncio.run(method())
        
        print("All tests passed!")
    finally:
        test_instance.tearDown()