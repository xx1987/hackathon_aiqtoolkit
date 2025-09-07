import asyncio
import sys
import os
import asyncio

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 尝试导入并运行planner.py中的主要功能
async def main():
    try:
        # 导入planner模块
        import planner
        
        print("成功导入planner模块")
        
        # 创建测试输入数据
        test_input = {
            "theme": "学习党的二十大精神",
            "headcount": 30,
            "lat": 39.9042,
            "lng": 116.4074,
            "radius_km": 5,
            "member_ids": [f"member_{i}" for i in range(10)]
        }
        
        print(f"测试输入数据: {test_input}")
        
        # 尝试运行智能体（如果有模拟实现，这里应该能返回模拟结果）
        print("开始运行主题党日智能体...")
        result = await planner.run_party_day_agent(test_input)
        
        print(f"测试结果: {result}")
        print("\n修复后的代码测试成功!")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())