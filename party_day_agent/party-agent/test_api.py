import urllib.request
import json
import os

# 使用正确的文件下载端点
url = 'http://localhost:8000/files/123_summary.docx'
print(f'正在调用API: {url}')
try:
    response = urllib.request.urlopen(url)
    data = response.read()
    print(f'API调用成功，响应状态码: {response.status}')
    print(f'响应内容长度: {len(data)} 字节')
    
    # 检查响应头中的文件名
    content_disposition = response.getheader('content-disposition')
    if content_disposition:
        print(f'响应头Content-Disposition: {content_disposition}')
    
    # 尝试解析JSON内容
    try:
        json_data = json.loads(data)
        print('JSON解析成功，内容如下:')
        print(json.dumps(json_data, ensure_ascii=False, indent=2))
        print(f'报告包含的字段: {list(json_data.keys())}')
        
        # 验证event_id是否正确
        if 'event_id' in json_data and json_data['event_id'] == '123':
            print('✓ event_id验证成功，与请求匹配')
        else:
            print('⚠ event_id不匹配或不存在')
            
    except json.JSONDecodeError:
        print('警告: 响应内容不是有效的JSON格式')
        print(f'响应内容: {data.decode()[:500]}...')
except Exception as e:
    print(f'API调用失败: {e}')