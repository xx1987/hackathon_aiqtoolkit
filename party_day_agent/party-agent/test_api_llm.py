#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import asyncio
from datetime import datetime

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_api_llm_client():
    """Test the API-based LLM client"""
    print("=== Testing API-based LLM Client ===")
    try:
        # 尝试直接导入planner模块中的APILLMClient类
        from .planner import APILLMClient, MODEL_NAME, BASE_URL, API_KEY
        
        print(f"Using API configuration:")
        print(f"- Model: {MODEL_NAME}")
        print(f"- Base URL: {BASE_URL}")
        print(f"- API Key: {'******' + API_KEY[-4:] if API_KEY else 'Not set'}")
        
        # 创建客户端实例
        llm_client = APILLMClient()
        
        # 准备测试数据
        test_data = {
            "theme": "学习贯彻二十大精神",
            "venue": {
                "name": "党建活动室",
                "address": "北京市海淀区中关村南大街5号"
            },
            "date": "2024-06-30",
            "headcount": 25
        }
        
        # 调用API生成方案
        print("\nGenerating plan with API LLM...")
        result = await llm_client.generate_plan(
            theme=test_data["theme"],
            venue=test_data["venue"],
            date=test_data["date"],
            headcount=test_data["headcount"]
        )
        
        # 验证结果
        if result:
            print("Successfully generated plan with API LLM!")
            print("\nPlan Details:")
            print(f"Time: {result.get('time', 'N/A')}")
            print("Agenda:")
            for item in result.get('agenda', []):
                print(f"  - {item}")
            print(f"Requirements: {result.get('requirements', 'N/A')}")
            print(f"Notes: {result.get('notes', 'N/A')}")
            return True
        else:
            print("Failed to generate plan with API LLM")
            return False
    except Exception as e:
        import traceback
        print(f"Error during API LLM client test: {e}")
        traceback.print_exc()
        return False

async def main():
    # 运行测试
    print(f"\n=== Starting API LLM Integration Test ===")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行测试并显示结果
    success = await test_api_llm_client()
    
    if success:
        print("\n✅ API LLM test passed successfully!")
    else:
        print("\n❌ API LLM test failed. Please check the logs for details.")

if __name__ == "__main__":
    asyncio.run(main())