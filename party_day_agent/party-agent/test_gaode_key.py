import sys
import os
import asyncio
import json
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

# 模拟Context类
class MockContext:
    def info(self, msg):
        print(f"[INFO] {msg}")
    def warning(self, msg):
        print(f"[WARNING] {msg}")
    def error(self, msg):
        print(f"[ERROR] {msg}")

# 直接使用系统的httpx模块
try:
    import httpx
except ImportError:
    # 如果没有httpx，使用模拟实现
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
                        "info": "OK",
                        "infocode": "10000",
                        "count": "0",
                        "pois": []
                    }
            return MockResponse()
    
    class MockHttpx:
        AsyncClient = MockAsyncClient
    httpx = MockHttpx()
    print("注意: 使用模拟的httpx库")

async def test_gaode_key():
    print("===== 测试.env.example中的GAODE_KEY有效性 =====")
    
    # 获取GAODE_KEY
    gaode_key = os.environ.get("GAODE_KEY", "")
    print(f"GAODE_KEY: {gaode_key}")
    print(f"GAODE_KEY长度: {len(gaode_key)}字符")
    
    if not gaode_key:
        print("错误: 未找到GAODE_KEY环境变量")
        return
    
    # 设置测试参数
    lat = 39.9087  # 北京天安门附近纬度
    lng = 116.3975  # 北京天安门附近经度
    radius_km = 1
    
    # 构建API请求URL
    url = f"https://restapi.amap.com/v3/place/around?key={gaode_key}&location={lng},{lat}&radius={radius_km*1000}&types=150200&sortrule=distance&offset=5"
    
    # 隐藏URL中的密钥
    masked_url = url.replace(gaode_key, "******")
    print(f"\nAPI请求URL: {masked_url}")
    
    try:
        # 发送API请求
        print("\n正在发送API请求...")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            print(f"API响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("\nAPI响应内容:")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
                # 分析响应结果
                status = data.get("status", "0")
                info = data.get("info", "未知错误")
                infocode = data.get("infocode", "")
                
                print(f"\n响应状态: status={status}, infocode={infocode}, info={info}")
                
                if status == "1":
                    count = data.get("count", "0")
                    pois = data.get("pois", [])
                    print(f"成功获取{count}个地点信息")
                    if pois:
                    print("\n前2个地点:")
                    for i, poi in enumerate(pois[:2], 1):
                        # 检查poi是字典类型再使用get方法
                        if isinstance(poi, dict):
                            name = poi.get('name', '未知')
                            address = poi.get('address', '未知')
                        else:
                            # 如果不是字典，尝试字符串格式化
                            name = str(poi) if poi else '未知'
                            address = '未知地址'
                        
                        print(f"  {i}. 名称: {name}")
                        print(f"     地址: {address}")
                    print("\n结论: GAODE_KEY有效！")
                else:
                    print("\n结论: GAODE_KEY无效或API调用失败")
                    print(f"错误信息: {info}")
                    if infocode == "10001":
                        print("提示: 这通常表示API密钥无效或已过期")
                    elif infocode == "10003":
                        print("提示: 这通常表示权限不足")
            else:
                print(f"\n结论: API请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"\n调用API时发生错误: {e}")
        print("结论: 无法确定GAODE_KEY是否有效，请检查网络连接或API配置")
    
    print("\n===== 测试完成 =====")

if __name__ == "__main__":
    asyncio.run(test_gaode_key())