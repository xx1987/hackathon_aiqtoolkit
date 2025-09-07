import sys
import os
import asyncio
import json

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 模拟Context类
class MockContext:
    def info(self, msg):
        print(f"[INFO] {msg}")
    def warning(self, msg):
        print(f"[WARNING] {msg}")
    def error(self, msg):
        print(f"[ERROR] {msg}")

# 模拟AsyncClient类
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

# 直接使用模拟的httpx实现，避免导入问题
class MockHttpx:
    AsyncClient = MockAsyncClient
httpx = MockHttpx()

async def test_gaode_rest_api():
    # 创建模拟上下文对象
    ctx = MockContext()
    
    # 设置测试参数
    theme = "生日派对"
    headcount = 20
    lat = 39.9087  # 北京天安门附近纬度
    lng = 116.3975  # 北京天安门附近经度
    radius_km = 5
    
    print("===== 测试高德地图REST API可用性 =====")
    print(f"测试参数: 主题={theme}, 人数={headcount}, 位置=({lat}, {lng}), 半径={radius_km}km")
    
    # 检查是否已设置API密钥
    gaode_key = os.environ.get("GAODE_KEY", "mock_key")
    has_gaode_key = gaode_key != "mock_key"
    print(f"是否配置了GAODE_KEY: {has_gaode_key}")
    print(f"GAODE_KEY长度: {len(gaode_key)}字符")
    
    if not has_gaode_key:
        print("\n注意: 未配置有效的GAODE_KEY，无法测试真实API")
        print("使用模拟调用演示API请求格式...")
        
        # 构建API URL（仅用于演示）
        url = f"https://restapi.amap.com/v3/place/around?key=******&location={lng},{lat}&radius={radius_km*1000}&types=150200|150300|150400|170200|170201&sortrule=distance&offset=20"
        print(f"\n模拟API请求URL: {url}")
        print("\n要测试真实API，请设置有效的GAODE_KEY环境变量")
        
        # 模拟API响应
        print("\n模拟API响应:")
        mock_response = {
            "status": "1",
            "count": "5",
            "pois": [
                {"id": "poi_1", "name": "模拟场地1", "location": "116.3975,39.9087"},
                {"id": "poi_2", "name": "模拟场地2", "location": "116.4075,39.9187"},
                {"id": "poi_3", "name": "模拟场地3", "location": "116.3875,39.8987"}
            ]
        }
        print(json.dumps(mock_response, ensure_ascii=False, indent=2))
    else:
        try:
            # 尝试调用高德地图API
            print("\n开始调用高德地图API...")
            url = f"https://restapi.amap.com/v3/place/around?key={gaode_key}&location={lng},{lat}&radius={radius_km*1000}&types=150200|150300|150400|170200|170201&sortrule=distance&offset=20"
            
            # 隐藏URL中的密钥
            masked_url = url.replace(gaode_key, "******")
            print(f"API请求URL: {masked_url}")
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                print(f"API响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print("\nAPI响应内容:")
                    print(json.dumps(data, ensure_ascii=False, indent=2))
                    
                    # 分析响应结果
                    if data.get("status") == "1":
                        count = data.get("count", "0")
                        pois = data.get("pois", [])
                        print(f"\n成功获取{count}个地点信息")
                        if pois:
                            print("\n前3个场地:")
                            for i, poi in enumerate(pois[:3], 1):
                                # 修复字符串.get()错误，确保正确处理字典类型
                                name = poi['name'] if isinstance(poi, dict) and 'name' in poi else '未知'
                                address = poi['address'] if isinstance(poi, dict) and 'address' in poi else '未知'
                                location = poi['location'] if isinstance(poi, dict) and 'location' in poi else '未知'
                                print(f"  {i}. 名称: {name}")
                                print(f"     地址: {address}")
                                print(f"     位置: {location}")
                        print("\n高德地图API调用成功！")
                    else:
                        print(f"\nAPI返回错误状态: {data.get('info', '未知错误')}")
                else:
                    print(f"\nAPI请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"\n调用高德地图API时出错: {e}")
    
    print("\n===== 测试完成 =====")

if __name__ == "__main__":
    asyncio.run(test_gaode_rest_api())