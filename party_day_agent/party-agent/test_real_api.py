import asyncio
import os
import sys
import planner

async def test_direct_code():
    """直接调用Python代码测试功能"""
    # 检查.env文件是否存在
    if not os.path.exists(".env"):
        print("警告: .env文件不存在，将使用模拟数据")
        print("请按照.env.example创建.env文件配置真实API密钥")
        
    # 设置环境变量，使用模拟模式
    os.environ.setdefault('GAODE_KEY', 'mock_key')
    os.environ.setdefault('WX_ROBOT_URL', 'mock_url')
    os.environ.setdefault('DOCX_TEMPLATE', './template.docx')
    
    # 示例输入数据
    input_data = {
        "theme": "学习党的二十大精神",
        "headcount": 30,
        "lat": 39.9042,
        "lng": 116.4074,
        "radius_km": 5,
        "member_ids": ["党员1", "党员2", "党员3"]
    }
    
    print("正在调用主题党日智能体代码...")
    print(f"输入参数: {input_data}")
    
    try:
        # 直接调用智能体函数
        result = await planner.run_party_day_agent(input_data)
        
        # 打印结果
        print("\n智能体返回结果:")
        print(f"状态: 成功")
        print(f"选择的场地: {result.get('venue', {}).get('name', '未指定')}")
        print(f"方案生成: {result.get('plan_id', '未生成')}")
        print(f"通知发送状态: {'成功' if result.get('notice_sent', False) else '未发送'}")
        print(f"总结文件URL: {result.get('summary_file', '未生成')}")
        print(f"\n完整结果: {result}")
        
        return True
    except Exception as e:
        print(f"\n调用失败: {e}")
        import traceback
        traceback.print_exc()
    
    return False

if __name__ == "__main__":
    print("主题党日智能体代码直接测试")
    print("=" * 50)
    print("注意: 由于Docker权限问题，我们直接调用Python代码")
    print("使用模拟数据进行测试，如需调用真实API请配置.env文件")
    print("=" * 50)
    
    # 运行测试
    success = asyncio.run(test_direct_code())
    
    if success:
        print("\n测试成功! 主题党日智能体代码运行正常。")
        print("\n注意: 如需调用真实API，需要：")
        print("1. 创建.env文件并配置GAODE_KEY等环境变量")
        print("2. 确保所有依赖已安装")
        print("3. 使用正确的Docker命令启动所有服务")
    else:
        print("\n测试失败，请检查代码和配置。")