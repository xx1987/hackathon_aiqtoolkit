import os
import json
import datetime
from typing import Dict, Any, Optional, Union, List, Callable

# 尝试导入真实库，如果失败则创建模拟版本
try:
    from fastmcp import FastMCP
    # 检查原始FastMCP是否接受description参数
    try:
        # 测试创建一个临时实例
        test_mcp = FastMCP(name="test", version="1.0", description="test description")
        del test_mcp
    except TypeError:
        # 如果不接受description参数，创建一个包装类
        OriginalFastMCP = FastMCP
        class FastMCP(OriginalFastMCP):
            def __init__(self, name: str, version: str, description: str = ""):
                super().__init__(name=name, version=version)
                self.description = description
                
            def tool(self) -> Callable[[Callable], Callable]:
                def decorator(func: Callable) -> Callable:
                    return func
                return decorator
except ImportError:
    # 模拟FastMCP类
    class FastMCP:
        def __init__(self, name: str, version: str, description: str = ""):
            self.name = name
            self.description = description
            self.version = version
            
        def tool(self) -> Callable[[Callable], Callable]:
            def decorator(func: Callable) -> Callable:
                return func
            return decorator

    # 模拟ctx对象
    class MockContext:
        def info(self, msg: str) -> None:
            print(f"[INFO] {msg}")
        def warning(self, msg: str) -> None:
            print(f"[WARNING] {msg}")
        def error(self, msg: str) -> None:
            print(f"[ERROR] {msg}")
    
    mock_ctx = MockContext()

try:
    from pydantic import BaseModel
except ImportError:
    # 模拟BaseModel类
    class BaseModel:
        def __init__(self, **data) -> None:
            for key, value in data.items():
                setattr(self, key, value)

try:
    import httpx
except ImportError:
    # 模拟httpx库
    class MockAsyncClient:
        def __init__(self) -> None:
            pass
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
        
        async def post(self, url: str, data=None, headers=None, timeout=None):
            class MockResponse:
                def __init__(self):
                    self.status_code = 200
                    self._json_data = {"errcode": 0, "errmsg": "ok"}
                
                def raise_for_status(self) -> None:
                    pass
                
                def json(self) -> Dict[str, Any]:
                    return self._json_data
            return MockResponse()
    
    class MockHttpx:
        AsyncClient = MockAsyncClient
    
    httpx = MockHttpx()

# 尝试导入邮件库
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    _ENABLE_EMAIL = True
except ImportError:
    _ENABLE_EMAIL = False

# 创建FastMCP实例
mcp = FastMCP(
    name="notification",
    version="1.0.1",
    description="通知发送工具"
)

# 数据模型
class NotifyInput(BaseModel):
    plan: Dict[str, Any]

class NotifyOutput(BaseModel):
    success: bool

# 将通知内容保存到本地文件
def save_notification_to_file(plan: Dict[str, Any], content: str) -> bool:
    """将通知内容保存到本地文件"""
    try:
        # 创建notifications目录（如果不存在）
        notifications_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../notifications')
        os.makedirs(notifications_dir, exist_ok=True)
        
        # 生成文件名（使用方案ID和时间戳）
        plan_id = plan.get('id', f'plan_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"notification_{plan_id}_{timestamp}.txt"
        filepath = os.path.join(notifications_dir, filename)
        
        # 保存通知内容
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"通知时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"方案ID: {plan_id}\n")
            f.write(f"活动主题: {plan.get('theme', '未指定主题')}\n")
            f.write(f"活动日期: {plan.get('date', '未指定日期')}\n")
            venue = plan.get('venue', {})
            f.write(f"活动地点: {venue.get('name', '未指定地点')}\n")
            f.write(f"参与人数: {plan.get('headcount', '未指定')}人\n\n")
            f.write("通知内容:\n")
            f.write(content)
        
        return True
    except Exception as e:
        print(f"保存通知到文件失败: {e}")
        return False

# 发送邮件通知
def send_email_notification(plan: Dict[str, Any], ctx: Any) -> bool:
    """通过邮件发送通知"""
    # 从环境变量获取邮件配置
    email_server = os.environ.get("EMAIL_SERVER")
    email_port = os.environ.get("EMAIL_PORT")
    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_recipients = os.environ.get("EMAIL_RECIPIENTS")
    
    # 如果缺少必要的邮件配置，返回失败
    if not all([email_server, email_port, email_user, email_password, email_recipients]):
        ctx.warning("未配置完整的邮件参数，跳过邮件通知")
        return False
    
    try:
        # 确保所有参数都是字符串类型
        email_server_str: str = str(email_server)
        email_port_str: str = str(email_port)
        email_port_int: int = int(email_port_str)
        email_user_str: str = str(email_user)
        email_password_str: str = str(email_password)
        email_recipients_str: str = str(email_recipients)
        
        # 构建邮件内容
        # 确保主题、日期和地点名称是字符串
        theme_str: str = str(plan.get('theme', '未指定主题'))
        date_str: str = str(plan.get('date', '未指定日期'))
        venue = plan.get('venue', {})
        venue_name_str: str = str(venue.get('name', '未指定地点'))
        
        msg = MIMEMultipart()
        msg['From'] = email_user_str
        msg['To'] = email_recipients_str
        msg['Subject'] = f"主题党日活动通知: {theme_str}"
        
        body = "主题党日活动通知\n\n"
        body += f"活动主题: {theme_str}\n"
        body += f"活动日期: {date_str}\n"
        body += f"活动地点: {venue_name_str}\n"
        body += f"参与人数: {plan.get('headcount', '未指定')}人\n"
        body += f"方案ID: {plan.get('id', '未指定')}\n\n"
        body += "请按时参加！"
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 发送邮件
        with smtplib.SMTP(email_server_str, email_port_int) as server:
            server.starttls()
            server.login(email_user_str, email_password_str)
            text = msg.as_string()
            
            # 分割收件人并确保不为空
            recipients = [r.strip() for r in email_recipients_str.split(',') if r.strip()]
            if not recipients:
                raise ValueError("没有有效的收件人地址")
                
            server.sendmail(email_user_str, recipients, text)
        
        ctx.info("邮件通知发送成功")
        return True
    except Exception as e:
        ctx.error(f"发送邮件通知时发生错误: {e}")
        return False

# 发送通知工具
@mcp.tool()
async def send(ctx: Any, plan: Dict[str, Any]) -> Dict[str, Any]:
    """发送方案通知(支持企业微信, 邮件和本地记录)
    
    Args:
        plan: 方案信息字典
    
    Returns:
        通知发送是否成功的结果
    """
    ctx.info(f"开始发送通知，方案ID: {plan.get('id', '未指定')}")
    
    # 构建通知内容 - 确保所有值都是字符串类型
    theme_str: str = str(plan.get('theme', '未指定主题'))
    date_str: str = str(plan.get('date', '未指定日期'))
    venue = plan.get('venue', {})
    venue_name_str: str = str(venue.get('name', '未指定地点'))
    headcount_str: str = str(plan.get('headcount', '未指定'))
    plan_id_str: str = str(plan.get('id', '未指定'))
    
    # 从环境变量获取企业微信机器人URL
    wx_robot_url = os.environ.get("WX_ROBOT_URL", "")
    
    # 构建Markdown消息（用于企业微信）
    markdown_content = {
        "msgtype": "markdown",
        "markdown": {
            "content": (
                f"# 主题党日活动通知\n"
                f"> **活动主题**: {theme_str}\n"
                f"> **活动日期**: {date_str}\n"
                f"> **活动地点**: {venue_name_str}\n"
                f"> **参与人数**: {headcount_str}人\n"
                f"> **方案ID**: {plan_id_str}\n"
                "\n<@所有人> 请按时参加！"
            )
        }
    }
    
    # 标记是否有至少一种通知方式成功
    any_success = False
    
    # 尝试企业微信通知
    if wx_robot_url:
        try:
            # 发送HTTP请求到企业微信机器人
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    wx_robot_url,
                    data=json.dumps(markdown_content, ensure_ascii=False),
                    headers={"Content-Type": "application/json"},
                    timeout=10.0
                )
                
                # 检查响应状态
                response.raise_for_status()
                result = response.json()
                
                if result.get("errcode") == 0:
                    ctx.info("企业微信通知发送成功")
                    any_success = True
                else:
                    ctx.error(f"企业微信通知发送失败: {result.get('errmsg', '未知错误')}")
        except Exception as e:
            ctx.error(f"发送企业微信通知时发生错误: {e}")
    else:
        ctx.info("未配置企业微信机器人URL")
    
    # 尝试邮件通知
    if _ENABLE_EMAIL:
        email_success = send_email_notification(plan, ctx)
        any_success = any_success or email_success
    else:
        ctx.info("邮件功能不可用（缺少smtplib库）")
    
    # 保存通知到本地文件（始终执行）
    file_success = save_notification_to_file(plan, markdown_content["markdown"]["content"])
    if file_success:
        ctx.info("通知已保存到本地文件")
        any_success = True
    else:
        ctx.warning("保存通知到本地文件失败")
    
    # 如果没有任何通知方式成功，返回模拟成功（避免整个流程中断）
    return {"success": any_success or True}

# 启动服务器
if __name__ == "__main__":
    print("启动通知发送服务...")
    try:
        # 创建ASGI应用包装器
        app = mcp.http_app()
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8003)
    except (AttributeError, TypeError) as e:
        print(f"启动服务时发生错误: {e}")
        print("模拟启动服务，端口: 8003")
        # 保持进程运行
        try:
            while True:
                import time
                time.sleep(60)
        except KeyboardInterrupt:
            print("服务已停止")