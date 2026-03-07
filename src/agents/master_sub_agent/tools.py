"""Master-Sub Agent Tools - 工具函数统一导出

注意：各个子智能体的工具函数已经拆分到对应的 xxx_agent_tools.py 文件中：
- mail_agent_tools.py: 邮件相关工具
- image_agent_tools.py: 图片生成相关工具
- tts_agent_tools.py: TTS相关工具
- digital_human_agent_tools.py: 数字人相关工具

本文件保留用于向后兼容，提供统一的工具导出接口。
"""

from typing import Any

from src.agents.master_sub_agent.subagents.mail_agent_tools import get_mail_tools
from src.agents.master_sub_agent.subagents.image_agent_tools import get_image_tools
from src.agents.master_sub_agent.subagents.tts_agent_tools import get_tts_tools
from src.agents.master_sub_agent.subagents.digital_human_agent_tools import get_digital_human_tools


def get_all_subagent_tools() -> dict[str, list[Any]]:
    """获取所有子智能体的工具映射"""
    return {
        "mail_agent": get_mail_tools(),
        "image_agent": get_image_tools(),
        "tts_agent": get_tts_tools(),
        "digital_human_agent": get_digital_human_tools(),
    }

