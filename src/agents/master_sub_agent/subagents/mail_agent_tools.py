"""Mail Agent Tools - 邮件子智能体使用的工具函数"""

import re
import time
from typing import Any

from langchain.tools import tool

from src.utils import logger


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """
    发送邮件工具（必须在用户明确确认后才能调用）

    ⚠️ 重要：此工具只能在用户明确确认后调用！在调用此工具之前，必须：
    1. 向用户展示完整的邮件信息（收件人、主题、内容）
    2. 等待用户明确确认（yes/是/好的/确认/同意）
    3. 只有在用户明确同意后才能调用此工具

    Args:
        to: 收件人邮箱地址 (例如: "alice@example.com")
        subject: 邮件主题
        body: 邮件内容

    Returns:
        发送结果信息
    """
    logger.info(f"即将发送邮件 - 收件人: {to}, 主题: {subject}, 内容: {body[:100]}...")

    # 模拟邮件发送
    time.sleep(2)
    logger.info(f"step 1.0.1 ---->邮件已发送 - 收件人: {to}, 主题: {subject}")
    return f"邮件已成功发送至 {to}"
   

@tool
def validate_email(email: str) -> dict[str, Any]:
    """
    验证邮箱地址的合法性和格式

    此工具用于检查邮箱地址是否符合标准格式要求。
    在发送邮件前必须使用此工具验证收件人邮箱地址。

    Args:
        email: 待验证的邮箱地址（例如: "alice@example.com"）

    Returns:
        验证结果，包含：
        - is_valid (bool): 邮箱地址是否合法
        - message (str): 详细的验证结果说明
        - suggestions (list): 如果格式不正确，提供修改建议

    常见邮箱格式问题：
    - 缺少 @ 符号
    - @ 前没有用户名
    - @ 后没有域名
    - 域名缺少顶级域名（如 .com）
    """
    # 检查是否为空
    if not email or not email.strip():
        return {
            "is_valid": False,
            "message": "邮箱地址不能为空",
            "suggestions": ["请输入有效的邮箱地址"]
        }

    email = email.strip()

    # 检查是否包含 @ 符号
    if '@' not in email:
        return {
            "is_valid": False,
            "message": f"邮箱地址 '{email}' 缺少 @ 符号",
            "suggestions": ["邮箱地址必须包含 @ 符号，例如: user@example.com"]
        }

    # 检查是否有多个 @ 符号
    if email.count('@') > 1:
        return {
            "is_valid": False,
            "message": f"邮箱地址 '{email}' 包含多个 @ 符号",
            "suggestions": ["邮箱地址只能包含一个 @ 符号，例如: user@example.com"]
        }

    # 分割用户名和域名
    parts = email.split('@')
    username = parts[0]
    domain = parts[1] if len(parts) > 1 else ""

    # 检查用户名是否为空
    if not username:
        return {
            "is_valid": False,
            "message": "邮箱地址 @ 符号前缺少用户名",
            "suggestions": ["请提供用户名，例如: username@example.com"]
        }

    # 检查域名是否为空
    if not domain:
        return {
            "is_valid": False,
            "message": "邮箱地址 @ 符号后缺少域名",
            "suggestions": ["请提供域名，例如: user@domain.com"]
        }

    # 检查域名是否包含点号
    if '.' not in domain:
        return {
            "is_valid": False,
            "message": f"域名 '{domain}' 缺少顶级域名（如 .com）",
            "suggestions": ["域名必须包含点和顶级域名，例如: user@example.com"]
        }

    # 检查顶级域名是否至少2个字符
    domain_parts = domain.split('.')
    tld = domain_parts[-1]
    if len(tld) < 2:
        return {
            "is_valid": False,
            "message": f"顶级域名 '.{tld}' 太短",
            "suggestions": ["顶级域名至少需要2个字符，例如: .com, .cn, .net"]
        }

    # 完整的邮箱格式验证
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(email_pattern, email))

    if is_valid:
        return {
            "is_valid": True,
            "message": f"邮箱地址 '{email}' 格式正确",
            "suggestions": []
        }
    else:
        return {
            "is_valid": False,
            "message": f"邮箱地址 '{email}' 格式不正确",
            "suggestions": [
                "请检查邮箱地址格式",
                "标准格式: username@domain.com",
                "示例: alice@example.com, bob@company.cn"
            ]
        }


def get_mail_tools() -> list[Any]:
    """获取邮件子智能体的工具列表"""
    return [send_email, validate_email]
