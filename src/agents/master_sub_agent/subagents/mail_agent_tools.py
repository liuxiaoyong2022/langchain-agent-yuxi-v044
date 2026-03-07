"""Mail Agent Tools - 邮件子智能体使用的工具函数"""

import re
import time
from typing import Any

from langchain.tools import tool
from langgraph.types import interrupt

from src.utils import logger


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """
    发送邮件工具

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
    logger.info(f"step 1.0.1 ----> 邮件已发送 - 收件人: {to}, 主题: {subject}")
    return f"邮件已成功发送至 {to}"
   

@tool
def send_email_origin(to: str, subject: str, body: str) -> str:
    """
    发送邮件工具

    Args:
        to: 收件人邮箱地址 (例如: "alice@example.com")
        subject: 邮件主题
        body: 邮件内容

    Returns:
        发送结果信息
    """
    logger.info(f"即将发送邮件 - 收件人: {to}, 主题: {subject}, 内容: {body[:100]}...")

    # 暂停并等待用户确认
    response = interrupt({
        "action": "send_email",
        "to": to,
        "subject": subject,
        "body": body,
        "message": "请确认是否发送此邮件？",
    })

    # 从中断中恢复
    user_action = response["decisions"][0]["type"]
    logger.info(f"step 1.0.2------->用户决策: {user_action}")

    if user_action == "approve":
        final_to = response.get("to", to)
        final_subject = response.get("subject", subject)
        final_body = response.get("body", body)

        # 模拟邮件发送
        time.sleep(2)
        logger.info(f"邮件已发送 - 收件人: {final_to}, 主题: {final_subject}")
        return f"邮件已成功发送至 {final_to}"
    else:
        logger.info(f"用户取消发送邮件")
        return "邮件发送已被用户取消"
    
@tool
def validate_email(email: str) -> dict[str, Any]:
    """
    验证邮箱地址的合法性

    Args:
        email: 待验证的邮箱地址

    Returns:
        验证结果，包含 is_valid (是否合法) 和 message (提示信息)
    """
    # 简单的邮箱格式验证
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(email_pattern, email))

    if is_valid:
        return {"is_valid": True, "message": "邮箱地址格式正确"}
    else:
        return {"is_valid": False, "message": "邮箱地址格式不正确，请检查"}


def get_mail_tools() -> list[Any]:
    """获取邮件子智能体的工具列表"""
    return [send_email, validate_email]
