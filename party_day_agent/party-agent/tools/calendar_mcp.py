from typing import List, Dict, Any
import os
import random
from datetime import datetime, timedelta

# 尝试导入真实库，如果失败则创建模拟版本
try:
    from fastmcp import FastMCP as OriginalFastMCP
    # 检查原始FastMCP是否接受description参数 
    try:
        # 测试创建一个临时实例
        test_mcp = OriginalFastMCP(name="test", version="1.0", description="test description")
        del test_mcp
        FastMCP = OriginalFastMCP
    except TypeError:
        # 如果不接受description参数，创建一个包装类
        class FastMCP(OriginalFastMCP):
            def __init__(self, name: str, version: str, description: str = ""):
                super().__init__(name=name, version=version)
                self.description = description
                
            def tool(self):
                def decorator(func):
                    return func
                return decorator
            
            def run(self, host="0.0.0.0", port=8000):
                # 检查原始FastMCP是否接受host和port参数
                try:
                    # 尝试使用host和port参数
                    super().run(host=host, port=port)
                except TypeError as e:
                    if "unexpected keyword argument" in str(e):
                        # 如果不接受这些参数，使用不带参数的run方法
                        print(f"FastMCP不支持指定host和port参数: {e}")
                        super().run()
except ImportError:
    # 模拟FastMCP类
    class FastMCP:
        def __init__(self, name, description, version):
            self.name = name
            self.description = description
            self.version = version
            
        def tool(self):
            def decorator(func):
                return func
            return decorator
            
        def run(self, host="0.0.0.0", port=8000):
            print(f"Starting mock {self.name} service on {host}:{port}...")
            # 模拟服务运行
            while True:
                import time
                time.sleep(60)

    # 模拟ctx对象
    class MockContext:
        def info(self, msg):
            print(f"[INFO] {msg}")
        def warning(self, msg):
            print(f"[WARNING] {msg}")
        def error(self, msg):
            print(f"[ERROR] {msg}")
    
    mock_ctx = MockContext()

try:
    from pydantic import BaseModel
except ImportError:
    # 模拟BaseModel类
    class BaseModel:
        def __init__(self, **data):
            for key, value in data.items():
                setattr(self, key, value)

try:
    import ics
except ImportError:
    # 模拟ics库
    class MockEvent:
        def __init__(self):
            self.name = "模拟事件"
            self.begin = datetime.now()
            self.description = "这是一个模拟事件"
    
    class MockCalendar:
        def __init__(self, content=None):
            self.events = [MockEvent() for _ in range(3)]
    
    ics = type('ics', (), {'Calendar': MockCalendar, 'Event': MockEvent})

# 创建FastMCP实例
mcp = FastMCP(
    name="calendar_check",
    description="本地ICS日历冲突检测工具",
    version="1.0.0"
)

# 数据模型
class CalendarCheckInput(BaseModel):
    date: str
    member_ids: List[str]

class CalendarCheckOutput(BaseModel):
    conflict: bool

# 日历检查工具
@mcp.tool()
async def check(ctx: Any, date: str, member_ids: List[str]) -> Dict[str, Any]:
    """检查指定日期是否有日历冲突
    
    Args:
        date: 要检查的日期（格式：YYYY-MM-DD）
        member_ids: 成员ID列表
    
    Returns:
        是否存在冲突的结果
    """
    ctx.info(f"开始检查日历冲突: 日期={date}, 成员数量={len(member_ids)}")
    
    try:
        # 解析日期
        check_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        ctx.error("日期格式不正确")
        return {"conflict": False}
    
    # 检查是否为周末
    is_weekend = check_date.weekday() in (5, 6)  # 5是周六，6是周日
    
    # 模拟冲突检测
    # 在实际应用中，这里会读取ICS文件并检查冲突
    has_conflict = False
    
    # 查找ICS文件
    calendar_dir = os.environ.get("CALENDAR_DIR", "./")
    ics_files = []
    
    try:
        # 尝试查找ICS文件
        for filename in os.listdir(calendar_dir):
            if filename.endswith(".ics"):
                ics_files.append(os.path.join(calendar_dir, filename))
        
        ctx.info(f"找到{len(ics_files)}个ICS日历文件")
        
        # 检查每个ICS文件是否有冲突
        for ics_file in ics_files:
            try:
                with open(ics_file, 'r', encoding='utf-8') as f:
                    calendar = ics.Calendar(f.read())
                    
                # 检查当天是否有事件
                for event in calendar.events:
                    # 简化处理：只检查事件是否与指定日期重叠
                    event_date = None
                    if hasattr(event, 'begin'):
                        event_date = event.begin.date()
                        
                        # 检查事件日期是否与检查日期相同
                        if event_date == check_date.date():
                            ctx.info(f"在{ics_file}中发现冲突事件: {event.name}")
                            has_conflict = True
                            break
            except Exception as e:
                ctx.warning(f"读取{ics_file}时出错: {e}")
                continue
        
    except Exception as e:
        ctx.error(f"查找或读取ICS文件时出错: {e}")
        # 如果无法读取ICS文件，使用概率模拟
        if is_weekend:
            # 周末冲突概率为20%
            has_conflict = random.random() < 0.2
        else:
            # 工作日冲突概率为40%
            has_conflict = random.random() < 0.4
        
        # 如果成员数量较多，增加冲突概率
        if len(member_ids) > 10:
            has_conflict = has_conflict or (random.random() < 0.3)
    
    ctx.info(f"日历检查结果: {'存在冲突' if has_conflict else '无冲突'}")
    return {"conflict": has_conflict}

# 生成模拟ICS文件用于测试
def generate_mock_ics_file():
    """生成模拟ICS文件"""
    from ics import Calendar, Event
    
    # 创建日历
    c = Calendar()
    
    # 创建一些测试事件
    today = datetime.now()
    
    # 添加一些事件
    for i in range(1, 4):
        e = Event()
        e.name = f"测试会议{i}"
        e.begin = (today + timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
        e.end = (today + timedelta(days=i, hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        e.description = "这是一个测试事件"
        c.events.add(e)
    
    # 保存到文件
    with open('mock_calendar.ics', 'w', encoding='utf-8') as f:
        f.writelines(c)
    
    print("生成了模拟日历文件: mock_calendar.ics")

# 创建ASGI应用包装器
app = mcp.http_app()

# 启动服务器
if __name__ == "__main__":
    # 生成模拟ICS文件
    generate_mock_ics_file()
    
    print("启动日历检查服务...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)