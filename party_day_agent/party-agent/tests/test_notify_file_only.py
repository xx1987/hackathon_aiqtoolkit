import sys
import os
import json
import datetime
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 尝试导入保存通知到文件的函数
try:
    from tools.notify_mcp import save_notification_to_file
    print("成功导入save_notification_to_file函数")
except ImportError as e:
    print(f"导入函数失败: {e}")
    sys.exit(1)

# 测试数据
test_plan = {
    "id": "test_plan_file_001",
    "theme": "测试本地文件通知功能",
    "date": "2024-12-25",
    "venue": {"name": "测试场地"},
    "headcount": 30
}

def main():
    print("\n===== 开始测试本地文件通知功能 =====")
    print(f"测试数据: {json.dumps(test_plan, ensure_ascii=False)}")
    
    # 创建测试内容
    test_content = f"""主题党日活动通知
活动主题: {test_plan['theme']}
活动日期: {test_plan['date']}
活动地点: {test_plan['venue']['name']}
参与人数: {test_plan['headcount']}人
方案ID: {test_plan['id']}

这是一条测试通知，验证本地文件记录功能。"""
    
    # 执行保存通知到文件函数
    print("\n开始保存通知到文件...")
    try:
        success = save_notification_to_file(test_plan, test_content)
        print(f"保存结果: {'成功' if success else '失败'}")
        
        # 检查是否创建了notifications目录
        notifications_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notifications')
        print(f"\n检查通知目录: {notifications_dir}")
        
        if os.path.exists(notifications_dir):
            # 列出目录中的文件
            files = os.listdir(notifications_dir)
            print(f"目录中的文件数量: {len(files)}")
            
            # 查找包含测试计划ID的文件
            plan_id = test_plan['id']
            found_files = [f for f in files if plan_id in f]
            print(f"找到的相关通知文件数量: {len(found_files)}")
            
            # 显示找到的文件内容预览
            for file in found_files:
                filepath = os.path.join(notifications_dir, file)
                print(f"\n文件: {filepath}")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"文件大小: {len(content)} 字节")
                        # 打印文件内容摘要
                        if len(content) > 500:
                            print(f"内容前500字节:\n{content[:500]}...")
                        else:
                            print(f"完整内容:\n{content}")
                        # 验证关键信息是否存在
                        key_info = [test_plan['theme'], test_plan['date'], test_plan['venue']['name'], str(test_plan['headcount'])]
                        for info in key_info:
                            if isinstance(info, str) and info in content:
                                print(f"✓ 验证通过: '{info}' 存在于文件内容中")
                            else:
                                print(f"✗ 验证失败: '{info}' 不存在于文件内容中")
                except Exception as e:
                    print(f"读取文件失败: {e}")
        else:
            print("通知目录未创建")
    except Exception as e:
        print(f"保存通知时发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n===== 测试完成 =====")

# 运行测试
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"运行测试时发生错误: {e}")
        import traceback
        traceback.print_exc()