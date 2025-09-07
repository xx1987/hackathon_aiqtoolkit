#!/usr/bin/env python3
"""
修复导入问题的辅助脚本

这个脚本用于解决demo.py中的导入问题，可以作为替代运行方式。
当直接运行demo.py出现相对导入错误时，可以使用这个脚本。
"""
import sys
import os
import importlib.util

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 动态导入planner模块
def import_planner():
    planner_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'planner.py')
    spec = importlib.util.spec_from_file_location("planner", planner_path)
    planner = importlib.util.module_from_spec(spec)
    sys.modules["planner"] = planner
    spec.loader.exec_module(planner)
    return planner

async def main():
    try:
        # 导入planner模块
        planner = import_planner()
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
        
        # 尝试运行智能体
        print("开始运行主题党日智能体...")
        result = await planner.run_party_day_agent(test_input)
        
        print(f"测试结果: {result}")
        print("\n程序运行成功!")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())