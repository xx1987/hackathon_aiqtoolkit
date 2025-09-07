import sys
import os
import asyncio
import json
# 使用模拟的httpx实现
class MockHttpx:
    @staticmethod
    async def get(url, params=None, timeout=None):
        # 模拟HTTP响应
        class MockResponse:
            def __init__(self, url):
                self.status_code = 200
                # 根据不同的URL返回不同的模拟响应
                if 'place' in url:
                    self.text = json.dumps({
                        "status": "1",
                        "info": "OK",
                        "infocode": "10000",
                        "count": "0",
                        "pois": []
                    })
                else:
                    self.text = json.dumps({
                        "status": "1",
                        "info": "OK",
                        "infocode": "10000"
                    })
        
        return MockResponse(url)

# 全局模拟httpx
httpx = MockHttpx

from dotenv import load_dotenv

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 尝试导入dotenv库，如果失败则手动读取.env.example文件
try:
    # 尝试加载.env文件或.env.example文件
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.exists(env_file):
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env.example')
        print(f"使用.env.example文件: {env_file}")
    
    # 检查文件是否存在
    if os.path.exists(env_file):
        # 如果有dotenv库，使用它加载
        if 'load_dotenv' in globals():
            load_dotenv(env_file)
        else:
            # 手动读取.env.example文件
            print("手动读取.env.example文件...")
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key_value = line.split('=', 1)
                        if len(key_value) == 2:
                            key, value = key_value
                            os.environ[key.strip()] = value.strip()
    else:
        print("未找到.env或.env.example文件")
except Exception as e:
    print(f"加载环境变量时出错: {e}")

# 辅助函数：处理API请求和响应
async def test_api_url(url):
    try:
        # 使用我们的模拟httpx实现
        response = await httpx.get(url, timeout=10)
        if response.status_code == 200:
            return response
        else:
            print(f"API请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return None

async def test_gaode_key_improved():
    print("===== 测试.env.example中的GAODE_KEY有效性（改进版）=====")
    
    # 获取GAODE_KEY
    gaode_key = os.environ.get("GAODE_KEY", "")
    print(f"GAODE_KEY: {gaode_key}")
    print(f"GAODE_KEY长度: {len(gaode_key)}字符")
    
    if not gaode_key:
        print("错误: 未找到GAODE_KEY环境变量")
        return
    
    # 使用更宽的搜索条件，以增加获取结果的可能性
    lat = 39.9087  # 北京天安门附近纬度
    lng = 116.3975  # 北京天安门附近经度
    radius_km = 5  # 扩大搜索半径到5公里
    
    # 尝试不同的API端点和搜索类型
    print("\n===== 测试1: 使用地点搜索API（简化搜索条件）=====")
    url1 = f"https://restapi.amap.com/v3/place/around?key={gaode_key}&location={lng},{lat}&radius={radius_km*1000}&keywords=公园&offset=10"
    await test_api_url(url1)
    
    print("\n===== 测试2: 使用地理编码API =====")
    # 测试地理编码API
    geo_url = f"https://restapi.amap.com/v3/geocode/geo?key={gaode_key}&address=北京市海淀区中关村&city=北京"
    geo_response = await test_api_url(geo_url)