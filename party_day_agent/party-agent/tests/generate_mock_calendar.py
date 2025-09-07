import sys
import os
from datetime import datetime, timedelta

# 直接使用简化方法生成模拟日历文件，避免依赖ics库
try:
    # 创建当前日期
    today = datetime.now()
    
    # 生成ICS格式的内容
    ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
"""
    
    # 添加3个测试事件
    for i in range(1, 4):
        event_date = today + timedelta(days=i)
        event_start = event_date.strftime('%Y%m%dT090000')
        event_end = event_date.strftime('%Y%m%dT100000')
        event_stamp = today.strftime('%Y%m%dT120000Z')
        
        ics_content += f"""
BEGIN:VEVENT
UID:{1234567890 + i}
DTSTAMP:{event_stamp}
DTSTART:{event_start}
DTEND:{event_end}
SUMMARY:测试会议{i}
DESCRIPTION:这是一个测试事件
END:VEVENT
"""
    
    # 结束日历
    ics_content += "END:VCALENDAR"
    
    # 保存到当前目录
    file_path = 'mock_calendar.ics'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(ics_content)
    
    print(f"成功生成模拟日历文件: {os.path.abspath(file_path)}")
except Exception as e:
    print(f"生成模拟日历文件时出错: {e}")
    # 作为最后的备选，使用静态内容创建日历文件
    static_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:1234567890
DTSTAMP:20230907T120000Z
DTSTART:20230908T090000
DTEND:20230908T100000
SUMMARY:测试会议1
DESCRIPTION:这是一个测试事件
END:VEVENT
BEGIN:VEVENT
UID:1234567891
DTSTAMP:20230907T120000Z
DTSTART:20230909T140000
DTEND:20230909T150000
SUMMARY:测试会议2
DESCRIPTION:这是一个测试事件
END:VEVENT
BEGIN:VEVENT
UID:1234567892
DTSTAMP:20230907T120000Z
DTSTART:20230910T110000
DTEND:20230910T120000
SUMMARY:测试会议3
DESCRIPTION:这是一个测试事件
END:VEVENT
END:VCALENDAR"""
    
    file_path = 'mock_calendar.ics'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(static_content)
    
    print(f"成功生成静态模拟日历文件: {os.path.abspath(file_path)}")