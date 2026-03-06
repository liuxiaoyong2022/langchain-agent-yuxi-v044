"""Weather Subagent - 天气子智能体配置"""

from src.agents.master_sub_agent.prompts import WEATHER_AGENT_PROMPT
from src.agents.master_sub_agent.tools import get_weather_tools


def get_weather_subagent() -> dict:
    """
    获取天气子智能体配置

    Returns:
        子智能体配置字典
    """
    return {
        "name": "weather_agent",
        "description": (
            "天气查询专家，负责查询指定城市的天气信息。"
            "包括识别城市名称、查询天气、展示结果。"
        ),
        "system_prompt": WEATHER_AGENT_PROMPT,
        "tools": get_weather_tools(),
    }
