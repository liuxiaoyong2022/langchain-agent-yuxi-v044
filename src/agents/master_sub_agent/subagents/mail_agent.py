"""Mail Subagent - 邮件子智能体配置"""

from src.agents.master_sub_agent.prompts import MAIL_AGENT_PROMPT
from src.agents.master_sub_agent.tools import get_mail_tools


def get_mail_subagent() -> dict:
    """
    获取邮件子智能体配置

    Returns:
        子智能体配置字典
    """
    return {
        "name": "mail_agent",
        "description": (
            "邮件发送专家，负责处理所有邮件相关的任务。"
            "包括收集邮件信息（收件人、主题、内容）、验证邮箱地址格式、"
            "起草邮件内容、发送前确认并执行发送。"
        ),
        "system_prompt": MAIL_AGENT_PROMPT,
        "tools": get_mail_tools(),
    }
