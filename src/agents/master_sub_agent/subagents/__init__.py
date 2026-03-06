"""Subagents - 所有子智能体的配置和工厂函数"""

from .mail_agent import get_mail_subagent
from .image_agent import get_image_subagent
from .tts_agent import get_tts_subagent
from .weather_agent import get_weather_subagent
from .digital_human_agent import get_digital_human_subagent

__all__ = [
    "get_mail_subagent",
    "get_image_subagent",
    "get_tts_subagent",
    "get_weather_subagent",
    "get_digital_human_subagent",
]
