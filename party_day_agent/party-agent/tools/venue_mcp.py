from typing import List, Dict, Any, Optional, Union, Callable
import os
import random

# 尝试导入真实库，如果失败则创建模拟版本
try:
    from fastmcp import FastMCP  # type: ignore
except ImportError:
    # 模拟FastMCP类
    class MockFastMCP:
        def __init__(self, name, description, version):
            self.name = name
            self.description = description
            self.version = version
            
        def tool(self):
            def decorator(func):
                return func
            return decorator
        
        def run(self, host="0.0.0.0", port=8001):
            # 模拟run方法以避免AttributeError
            print(f"MockFastMCP is running on {host}:{port}...")
    
    FastMCP = MockFastMCP

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
    from pydantic import BaseModel  # type: ignore
except ImportError:
    # 模拟BaseModel类
    class BaseModel:
        def __init__(self, **data):
            for key, value in data.items():
                setattr(self, key, value)

try:
    import httpx  # type: ignore
except ImportError:
    # 模拟httpx库
    class MockAsyncClient:
        def __init__(self):
            pass
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
        
        async def get(self, url, timeout=None):
            class MockResponse:
                def __init__(self):
                    self.status_code = 200
                
                def raise_for_status(self):
                    pass
                
                def json(self):
                    return {
                        "status": "1",
                        "count": "5",
                        "pois": [
                            {"id": "poi_1", "name": "模拟场地1", "location": "120.15,30.27"},
                            {"id": "poi_2", "name": "模拟场地2", "location": "120.16,30.28"},
                            {"id": "poi_3", "name": "模拟场地3", "location": "120.14,30.26"}
                        ]
                    }
            return MockResponse()
    
    class MockHttpx:
        AsyncClient = MockAsyncClient
    
    httpx = MockHttpx()

try:
    # 尝试导入MCP客户端相关库
    from nat.tool.mcp.mcp_client_base import MCPStreamableHTTPClient  # type: ignore
    from mcp.types import ToolCallRequest  # type: ignore
    has_mcp_client = True
except ImportError:
    # 如果导入失败，设置标志为False
    has_mcp_client = False
    
    # 模拟MCP客户端类
    class MockMCPStreamableHTTPClient:
        def __init__(self, url):
            self.url = url
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
        
        async def get_tool(self, tool_name):
            class MockMCPToolClient:
                def __init__(self):
                    self.name = tool_name
                    self.description = "Mock MCP tool"
                
                async def acall(self, params):
                    # 返回模拟数据
                    return {
                        "venues": [
                            {
                                "id": "mcp_venue_1",
                                "name": f"{params.get('theme', '')}MCP场地1",
                                "lat": params.get('lat', 0) + random.uniform(-0.05, 0.05),
                                "lng": params.get('lng', 0) + random.uniform(-0.05, 0.05),
                                "capacity": params.get('headcount', 0) + random.randint(5, 20)
                            }
                        ]
                    }
            return MockMCPToolClient()
    
    MCPStreamableHTTPClient = MockMCPStreamableHTTPClient
    
    # 模拟ToolCallRequest类
    class ToolCallRequest:
        def __init__(self, method, params):
            self.method = method
            self.params = params

# 尝试导入真实库，如果失败则创建模拟版本
try:
    from fastmcp import FastMCP
    # 检查原始FastMCP是否接受description参数
    try:
        # 测试创建一个临时实例
        test_mcp = FastMCP(name="test", version="1.0", description="test description")
        del test_mcp
    except TypeError:
        # 如果不接受description参数，创建一个包装类
        OriginalFastMCP = FastMCP
        class FastMCP(OriginalFastMCP):
            def __init__(self, name: str, version: str, description: str = ""):
                super().__init__(name=name, version=version)
                self.description = description
                
            def tool(self) -> Callable[[Callable], Callable]:
                def decorator(func: Callable) -> Callable:
                    return func
                return decorator
except ImportError:
    # 模拟FastMCP类
    class FastMCP:
        def __init__(self, name: str, version: str, description: str = ""):
            self.name = name
            self.description = description
            self.version = version
            
        def tool(self) -> Callable[[Callable], Callable]:
            def decorator(func: Callable) -> Callable:
                return func
            return decorator

# 创建FastMCP实例
mcp = FastMCP(
    name="venue_search",
    description="高德地图场地搜索工具",
    version="1.0.0"
)

# 数据模型
class VenueSearchInput(BaseModel):
    theme: str
    headcount: int
    lat: float
    lng: float
    radius_km: int = 10

# 场地搜索工具
@mcp.tool()
async def search(ctx: Any, theme: str, headcount: int, lat: float, lng: float, radius_km: int = 10) -> List[Dict[str, Any]]:
    """根据主题、人数和位置搜索合适的场地
    
    Args:
        theme: 活动主题
        headcount: 参与人数
        lat: 纬度
        lng: 经度
        radius_km: 搜索半径（公里）
    
    Returns:
        符合条件的场地列表
    """
    ctx.info(f"开始搜索场地: 主题={theme}, 人数={headcount}, 位置=({lat}, {lng}), 半径={radius_km}km")
    
    # 优先尝试使用MCP协议连接高德地图MCP Server
    use_mcp = os.environ.get("USE_GAODE_MCP", "false").lower() == "true"
    if use_mcp and has_mcp_client:
        return await search_via_mcp(ctx, theme, headcount, lat, lng, radius_km)
    
    # 否则使用现有的REST API方式
    ctx.info("未启用或不支持MCP模式，使用传统REST API方式")
    return await search_via_rest_api(ctx, theme, headcount, lat, lng, radius_km)

async def search_via_mcp(ctx: Any, theme: str, headcount: int, lat: float, lng: float, radius_km: int = 10) -> List[Dict[str, Any]]:
    """通过MCP协议连接高德地图MCP Server搜索场地"""
    ctx.info("使用MCP协议连接高德地图MCP Server")
    
    # 从环境变量获取高德地图MCP Server地址和密钥
    gaode_mcp_url = os.environ.get("GAODE_MCP_URL", "https://lbs.amap.com/api/mcp-server/summary")
    gaode_mcp_key = os.environ.get("GAODE_MCP_KEY", "")
    
    if not gaode_mcp_key:
        ctx.warning("未配置GAODE_MCP_KEY，使用模拟MCP数据")
        return generate_mock_venues(ctx, theme, headcount, lat, lng)
    
    try:
        # 创建MCP客户端连接
        async with MCPStreamableHTTPClient(url=gaode_mcp_url) as client:
            # 获取场地搜索工具
            venue_tool = await client.get_tool("venue_search")
            
            # 准备调用参数
            params = {
                "theme": theme,
                "headcount": headcount,
                "lat": lat,
                "lng": lng,
                "radius_km": radius_km,
                "api_key": gaode_mcp_key
            }
            
            # 调用MCP工具
            ctx.info(f"调用MCP工具: venue_search, 参数: {params}")
            result = await venue_tool.acall(params)
            
            # 解析结果
            if isinstance(result, dict) and "venues" in result:
                venues = result["venues"]
                # 修复类型比较问题，确保capacity是整数
                filtered_venues = []
                for v in venues:
                    try:
                        capacity = int(v.get("capacity", 0))
                        if capacity >= headcount:
                            filtered_venues.append(v)
                    except (ValueError, TypeError):
                        # 处理capacity无法转换为整数的情况
                        ctx.warning(f"场地容量格式错误: {v.get('capacity')}")
                ctx.info(f"通过MCP成功获取{len(filtered_venues)}个符合条件的场地")
                return filtered_venues
            else:
                ctx.warning(f"MCP返回的结果格式不符合预期: {result}")
                return generate_mock_venues(ctx, theme, headcount, lat, lng)
    except Exception as e:
        ctx.error(f"调用高德地图MCP Server失败: {e}")
        # 失败时返回模拟数据
        return generate_mock_venues(ctx, theme, headcount, lat, lng)

async def search_via_rest_api(ctx: Any, theme: str, headcount: int, lat: float, lng: float, radius_km: int = 10) -> List[Dict[str, Any]]:
    """通过REST API调用高德地图搜索场地"""
    # 尝试从环境变量获取高德API密钥
    gaode_key = os.environ.get("GAODE_KEY", "mock_key")
    
    # 如果没有API密钥，使用模拟数据
    if gaode_key == "mock_key":
        ctx.warning("没有配置GAODE_KEY，使用模拟数据")
        return generate_mock_venues(ctx, theme, headcount, lat, lng)
    
    try:
        # 调用高德地图API搜索场地
        # 注意：这里只是示例，实际的高德API调用需要根据官方文档调整
        url = f"https://restapi.amap.com/v3/place/around?key={gaode_key}&location={lng},{lat}&radius={radius_km*1000}&types=150200|150300|150400|170200|170201&sortrule=distance&offset=20"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        # 解析API响应
        venues = []
        if data.get("status") == "1" and data.get("count") != "0":
            for poi in data.get("pois", []):
                venue = {
                    "id": poi.get("id", ""),
                    "name": poi.get("name", ""),
                    "lat": float(poi.get("location", ",").split(",")[1] if "," in poi.get("location", "") else lat),
                    "lng": float(poi.get("location", ",").split(",")[0] if "," in poi.get("location", "") else lng),
                    "capacity": headcount + random.randint(0, 50)  # 模拟容量
                }
                venues.append(venue)
        
        # 过滤出容量足够的场地，确保capacity是整数类型
        filtered_venues = []
        for v in venues:
            try:
                capacity = int(v["capacity"])
                if capacity >= headcount:
                    filtered_venues.append(v)
            except (ValueError, TypeError):
                # 处理capacity无法转换为整数的情况
                ctx.warning(f"场地容量格式错误: {v.get('capacity')}")
        ctx.info(f"成功获取{len(filtered_venues)}个场地信息")
        return filtered_venues
    except Exception as e:
        ctx.error(f"调用高德地图API失败: {e}")
        # 失败时返回模拟数据
        return generate_mock_venues(ctx, theme, headcount, lat, lng, count=3, prefix="fallback_venue")

def generate_mock_venues(ctx: Any, theme: str, headcount: int, lat: float, lng: float, count: int = 5, prefix: str = "venue") -> List[Dict[str, Any]]:
    """生成模拟场地数据"""
    mock_venues = [
        {
            "id": f"{prefix}_{i}",
            "name": f"{theme}活动中心{i}",
            "lat": lat + random.uniform(-0.05, 0.05),
            "lng": lng + random.uniform(-0.05, 0.05),
            "capacity": headcount + random.randint(5, 20)
        } for i in range(1, count + 1)
    ]
    
    # 根据人数过滤，确保capacity是整数
    filtered_venues = []
    for v in mock_venues:
        try:
            capacity = int(v["capacity"])
            if capacity >= headcount:
                filtered_venues.append(v)
        except (ValueError, TypeError):
            # 理论上这里不应该出现异常，因为我们生成的是整数
            pass
    ctx.info(f"生成了{len(filtered_venues)}个模拟场地")
    return filtered_venues

# 创建ASGI应用包装器
app = mcp.http_app()

# 启动服务器
if __name__ == "__main__":
    try:
        print("启动场地搜索服务...")
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8001)
    except Exception as e:
        print(f"启动服务器失败: {e}")
        # 回退到基本的模拟启动
        print("使用模拟模式运行...")