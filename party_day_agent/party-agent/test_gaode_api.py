import sys
import os
import asyncio

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.venue_mcp import search, MockContext

async def test_gaode_api():
    # 创建模拟上下文对象
    ctx = MockContext()
    
    # 设置测试参数
    theme = "生日派对"
    headcount = 20
    lat = 39.9087  # 北京天安门附近纬度
    lng = 116.3975  # 北京天安门附近经度
    radius_km = 5
    
    print("===== 测试高德地图API可用性 =====")
    print(f"测试参数: 主题={theme}, 人数={headcount}, 位置=({lat}, {lng}), 半径={radius_km}km")
    
    # 检查是否已设置API密钥
    has_gaode_key = "GAODE_KEY" in os.environ and os.environ["GAODE_KEY"] != "mock_key"
    print(f"是否配置了GAODE_KEY: {has_gaode_key}")
    
    # 尝试调用API搜索场地
    print("\n开始调用场地搜索功能...")
    venues = await search(ctx, theme, headcount, lat, lng, radius_km)
    
    # 显示结果
    print(f"\n搜索结果: 找到{len(venues)}个场地")
    if venues:
        print("\n场地详情:")
        for i, venue in enumerate(venues[:3], 1):  # 只显示前3个
            print(f"  {i}. 名称: {venue.get('name', '未知')}")
            print(f"     位置: ({venue.get('lat', 0)}, {venue.get('lng', 0)})")
            print(f"     容量: {venue.get('capacity', 0)}")
            print(f"     ID: {venue.get('id', '未知')}")
            print()
    
    # 判断是否使用了模拟数据
    is_mock_data = all(venue.get('id', '').startswith('venue_') or venue.get('id', '').startswith('fallback_venue') or venue.get('id', '').startswith('mcp_venue_') for venue in venues)
    if is_mock_data:
        print("\n===== 结果分析 ======")
        if has_gaode_key:
            print("注意: 尽管配置了GAODE_KEY，但返回的仍然是模拟数据，可能的原因：")
            print("1. API密钥无效或权限不足")
            print("2. 网络连接问题")
            print("3. API调用参数不正确")
        else:
            print("注意: 由于未配置有效的GAODE_KEY，返回的是模拟数据")
            print("要测试真实API，请设置有效的GAODE_KEY环境变量")
    else:
        print("\n===== 结果分析 ======")
        print("成功获取到实际的场地数据，高德地图API可用！")
    
if __name__ == "__main__":
    asyncio.run(test_gaode_api())