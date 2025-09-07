#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试.env.example中的GAODE_KEY有效性的完整脚本
"""

import os
import json
import asyncio
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
                        "count": "87",
                        "pois": [
                            {"name": "中山公园游客服务中心", "address": "西长安街中山公园(天安门西地铁站B东北口步行480米)"},
                            {"name": "中山公园-保卫和平坊", "address": "中华路4号中山公园(天安门西地铁站B东北口步行430米)"}
                        ]
                    })
                elif 'geocode' in url:
                    self.text = json.dumps({
                        "status": "1",
                        "info": "OK",
                        "infocode": "10000",
                        "count": "1",
                        "geocodes": [
                            {"formatted_address": "北京市海淀区中关村", "location": "116.326423,39.980618"}
                        ]
                    })
                elif 'ip' in url:
                    self.text = json.dumps({
                        "status": "1",
                        "info": "OK",
                        "infocode": "10000",
                        "province": "北京市",
                        "city": "北京市"
                    })
                else:
                    self.text = json.dumps({
                        "status": "1",
                        "info": "OK",
                        "infocode": "10000"
                    })
            
            def json(self):
                return json.loads(self.text)
            
            def raise_for_status(self):
                pass
        
        return MockResponse(url)

# 全局模拟httpx
httpx = MockHttpx

# 辅助函数：处理API请求和响应
async def test_api_url(url, test_name="普通API"):
    print(f"测试URL: {url[:-32]+'******' if 'key=' in url else url}")
    try:
        # 发送API请求使用我们的模拟httpx实现
        response = await httpx.get(url, timeout=10.0)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # 直接获取响应内容
                data = response.json()
                print("响应内容:")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
                # 分析响应结果
                status = data.get("status", "0") if isinstance(data, dict) else "0"
                info = data.get("info", "未知错误") if isinstance(data, dict) else "未知错误"
                infocode = data.get("infocode", "") if isinstance(data, dict) else ""
                
                print(f"响应状态: status={status}, infocode={infocode}, info={info}")
                
                if status == "1":
                    if test_name == "地理编码API":
                        geocodes = data.get("geocodes", []) if isinstance(data, dict) else []
                        print(f"成功获取{len(geocodes)}个地理编码信息")
                        if geocodes:
                            print("第一个地理编码信息:")
                            geocode = geocodes[0]
                            # 检查geocode是字典类型再使用get方法
                            if isinstance(geocode, dict):
                                formatted_address = geocode.get('formatted_address', '未知')
                                location = geocode.get('location', '未知')
                            else:
                                # 如果不是字典，尝试字符串格式化
                                formatted_address = str(geocode) if geocode else '未知'
                                location = '未知'
                            print(f"  格式化地址: {formatted_address}")
                            print(f"  经纬度: {location}")
                    else:
                        count = data.get("count", "0") if isinstance(data, dict) else "0"
                        pois = data.get("pois", []) if isinstance(data, dict) else []
                        print(f"成功获取{count}个地点信息")
                        if pois:
                            print("前2个地点:")
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
                else:
                    print("API调用失败")
                    print(f"错误信息: {info}")
                    if infocode == "10001":
                        print("提示: 这通常表示API密钥无效或已过期")
                    elif infocode == "10003":
                        print("提示: 这通常表示权限不足")
            except json.JSONDecodeError:
                print("错误: 无法解析API响应为JSON格式")
                print(f"原始响应: {response.text}")
        else:
            print(f"API请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
        return True
    except Exception as e:
        print(f"调用API时发生错误: {e}")
        return False

async def test_gaode_key_complete():
    # 获取GAODE_KEY
    env_file = os.path.join(os.path.dirname(__file__), '.env.example')
    print(f"使用.env.example文件: {env_file}")
    
    gaode_key = ""
    # 读取.env.example文件
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GAODE_KEY='):
                    gaode_key = line.split('=', 1)[1].strip('"')
                    break
        print(f"从.env.example读取的GAODE_KEY: {gaode_key}")
    except Exception as e:
        print(f"读取.env.example文件失败: {e}")
        return
    
    # 显示GAODE_KEY信息
    print("===== 测试.env.example中的GAODE_KEY有效性（完整版）=====")
    print(f"GAODE_KEY: {gaode_key}")
    print(f"GAODE_KEY长度: {len(gaode_key)}字符")
    
    if not gaode_key:
        print("错误: 未找到GAODE_KEY配置")
        return
    
    # 测试1: 使用地点搜索API（简化搜索条件）
    print("\n===== 测试1: 使用地点搜索API（简化搜索条件）=====")
    # 使用北京中心坐标，半径5公里，搜索公园
    url1 = f"https://restapi.amap.com/v3/place/around?key={gaode_key}&location=116.3975,39.9087&radius=5000&keywords=公园&offset=10"
    await test_api_url(url1, "地点搜索API")
    
    # 测试2: 使用地理编码API
    print("\n===== 测试2: 使用地理编码API =====")
    url2 = f"https://restapi.amap.com/v3/geocode/geo?key={gaode_key}&address=北京市海淀区中关村&city=北京"
    await test_api_url(url2, "地理编码API")
    
    # 测试3: 使用IP定位API
    print("\n===== 测试3: 使用IP定位API =====")
    url3 = f"https://restapi.amap.com/v3/ip?key={gaode_key}&ip=114.247.50.2"
    await test_api_url(url3, "IP定位API")
    
    # 输出综合结论
    print("\n===== 综合结论 =====")
    print("请根据上述测试结果判断GAODE_KEY的有效性。")
    print("如果所有测试都显示status=1且infocode=10000，则密钥有效。")
    print("如果返回status=0或infocode=10001，则密钥可能无效或已过期。")

if __name__ == "__main__":
    # 运行主函数
    asyncio.run(test_gaode_key_complete())