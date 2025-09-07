#!/usr/bin/env python3
import os
import sys
import subprocess
import asyncio

async def run_test_file(file_path):
    """运行单个测试文件"""
    try:
        print(f"\n=== 开始运行测试文件: {os.path.basename(file_path)} ===")
        
        # 使用Python解释器运行测试文件
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # 获取输出和错误
        stdout, stderr = await process.communicate()
        
        # 打印输出
        if stdout:
            print(f"\n标准输出:\n{stdout.decode('utf-8')}")
        if stderr:
            print(f"\n标准错误:\n{stderr.decode('utf-8')}")
        
        # 检查返回码
        if process.returncode == 0:
            print(f"\n✅ 测试文件 {os.path.basename(file_path)} 运行成功")
            return True
        else:
            print(f"\n❌ 测试文件 {os.path.basename(file_path)} 运行失败，返回码: {process.returncode}")
            return False
    except Exception as e:
        print(f"\n❌ 运行测试文件 {os.path.basename(file_path)} 时出错: {str(e)}")
        return False

async def main():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 获取所有以test_开头的Python文件
    test_files = [
        os.path.join(current_dir, f)
        for f in os.listdir(current_dir)
        if f.startswith('test_') and f.endswith('.py') and f != 'run_all_tests.py'
    ]
    
    if not test_files:
        print("未找到任何测试文件")
        return
    
    print(f"找到 {len(test_files)} 个测试文件，开始运行...")
    
    # 逐个运行测试文件
    success_count = 0
    for file_path in test_files:
        success = await run_test_file(file_path)
        if success:
            success_count += 1
    
    # 打印总结果
    print(f"\n\n=== 测试运行总结 ===")
    print(f"运行测试文件总数: {len(test_files)}")
    print(f"成功运行: {success_count}")
    print(f"运行失败: {len(test_files) - success_count}")
    
    if success_count == len(test_files):
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败！")

if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())