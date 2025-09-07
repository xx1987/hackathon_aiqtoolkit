import asyncio
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.calendar_mcp import check, generate_mock_ics_file

class TestCalendarCheck(unittest.TestCase):
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
        
        # 设置CALENDAR_DIR环境变量
        os.environ['CALENDAR_DIR'] = os.path.dirname(os.path.abspath(__file__))
    
    def tearDown(self):
        # 恢复原始环境变量
        os.environ.clear()
        os.environ.update(self.original_env)
    
    async def test_calendar_check_valid_date(self):
        # 测试有效的日期格式
        result = await check(
            self.mock_ctx,
            date="2023-10-01",
            members=["张三", "李四", "王五"]
        )
        
        # 验证返回格式
        self.assertIsInstance(result, dict)
        self.assertIn("has_conflict", result)
        self.assertIn("conflicting_members", result)
    
    async def test_calendar_check_empty_members(self):
        # 测试空成员列表
        result = await check(
            self.mock_ctx,
            date="2023-10-01",
            members=[]
        )
        
        # 应该没有冲突
        self.assertFalse(result["has_conflict"])
        self.assertEqual(len(result["conflicting_members"]), 0)
    
    async def test_calendar_check_invalid_date_format(self):
        # 测试无效的日期格式
        result = await check(
            self.mock_ctx,
            date="2023/10/01",  # 使用斜杠分隔的日期
            members=["张三", "李四"]
        )
        
        # 即使日期格式无效，函数也应该正常返回
        self.assertIsInstance(result, dict)
    
    @patch('tools.calendar_mcp.ics.Calendar')
    async def test_calendar_check_with_events(self, mock_calendar_class):
        # 模拟日历事件
        mock_event = MagicMock()
        mock_event.begin = MagicMock()
        mock_event.begin.date.return_value = "2023-10-01"
        
        mock_calendar = MagicMock()
        mock_calendar.events = [mock_event]
        mock_calendar_class.return_value = mock_calendar
        
        # 模拟open函数
        with patch('builtins.open', unittest.mock.mock_open()):
            result = await check(
                self.mock_ctx,
                date="2023-10-01",
                members=["张三"]
            )
            
            # 验证结果
            self.assertIsInstance(result, dict)
    
    @patch('os.path.exists', return_value=False)
    async def test_calendar_check_file_not_exist(self, mock_exists):
        # 测试日历文件不存在的情况
        result = await check(
            self.mock_ctx,
            date="2023-10-01",
            members=["张三", "李四"]
        )
        
        # 即使文件不存在，函数也应该正常返回
        self.assertIsInstance(result, dict)

# 运行测试
if __name__ == "__main__":
    # 为了在命令行中直接运行异步测试
    import inspect
    
    # 获取所有以test_开头的异步方法
    async_test_methods = [method for method in dir(TestCalendarCheck) 
                         if method.startswith('test_') and inspect.iscoroutinefunction(getattr(TestCalendarCheck, method))]
    
    # 创建测试实例
    test_instance = TestCalendarCheck()
    test_instance.setUp()
    
    try:
        # 运行异步测试
        for method_name in async_test_methods:
            print(f"Running test: {method_name}")
            method = getattr(test_instance, method_name)
            asyncio.run(method())
        
        print("All tests passed!")
    finally:
        test_instance.tearDown()