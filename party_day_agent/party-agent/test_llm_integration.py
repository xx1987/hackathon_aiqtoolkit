#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import asyncio
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入需要的模块
from .planner import llm_client

# Set environment variables to use API implementation
os.environ["USE_MOCK"] = "0"

async def test_llm_client():
    """Test the LLM client directly using API"""
    print("=== Testing LLM Client via API ===")
    try:
        # Import generate_plan_func within the function to avoid import issues
        from .planner import generate_plan as generate_plan_func
        
        # 创建完整的模拟状态对象，包含所有必要字段
        state = {
            "plan_id": "test_llm_client_plan",
            "theme": "学习贯彻二十大精神",
            "venue": {
                "name": "党建活动室",
                "address": "北京市海淀区中关村南大街5号"
            },
            "date": "2024-06-30",
            "headcount": 25
        }
        
        # 调用大模型API生成方案
        print("Generating plan with LLM API...")
        result = await generate_plan_func(state)
        
        # 验证结果
        if result and "plan" in result:
            print("Successfully generated plan with LLM API!")
            print("\nPlan Details:")
            print(f"Time: {result['plan'].get('time', 'N/A')}")
            print("Agenda:")
            for item in result['plan'].get('agenda', []):
                print(f"  - {item}")
            print(f"Requirements: {result['plan'].get('requirements', 'N/A')}")
            print(f"Notes: {result['plan'].get('notes', 'N/A')}")
            return True
        else:
            print("Failed to generate plan with LLM API")
            return False
    except Exception as e:
        import traceback
        print(f"Error during LLM client API test: {e}")
        traceback.print_exc()
        return False

async def test_generate_plan_function():
    """Test the generate_plan function in the workflow"""
    print("\n=== Testing Generate Plan Function ===")
    try:
        # Import generate_plan_func within the function to avoid import issues
        from .planner import generate_plan as generate_plan_func
        
        # 创建模拟状态对象
        state = {
            "plan_id": "test_plan_001",
            "theme": "党史学习教育",
            "date": "2024-07-01",
            "venue": {
                "name": "党史纪念馆",
                "address": "北京市西城区前门西大街141号",
                "type": "党建场所"
            },
            "headcount": 30,
            "member_ids": ["user1", "user2", "user3"]
        }
        
        # 调用生成方案函数
        print("Running generate_plan function...")
        result = await generate_plan_func(state)
        
        # 验证结果
        if result and "plan" in result:
            print("Successfully generated plan in the function!")
            print("\nGenerated Plan:")
            print(json.dumps(result["plan"], ensure_ascii=False, indent=2))
            return True
        else:
            print("Failed to generate plan in the function")
            return False
    except Exception as e:
        import traceback
        print(f"Error during generate_plan function test: {e}")
        traceback.print_exc()
        return False

async def main():
    # 运行测试
    print(f"\n=== Starting LLM Integration Tests ===")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Environment: {'Mock' if os.environ.get('USE_MOCK') == '1' else 'Real'}")
    
    # 显示LLM客户端信息
        try:
            from .planner import llm_client
        print(f"Using LLM client: {llm_client.__class__.__name__}")
    except Exception:
        print("LLM client information unavailable")
    
    # 运行测试并收集结果
    test_results = {
        "test_llm_client": await test_llm_client(),
        "test_generate_plan_function": await test_generate_plan_function()
    }
    
    # 显示测试结果摘要
    print("\n=== Test Results Summary ===")
    all_passed = all(test_results.values())
    
    for test_name, passed in test_results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{test_name}: {status}")
    
    if all_passed:
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed. Please check the logs for details.")

if __name__ == "__main__":
    asyncio.run(main())