"""Weather Agent Tools - 天气查询子智能体使用的工具函数"""

from typing import Any

from langchain.tools import tool

from src.utils import logger


@tool
def query_weather(city: str) -> str:
    """
    查询天气工具

    Args:
        city: 城市名称

    Returns:
        天气信息
    """
    logger.info(f"查询天气 - 城市: {city}")

    # 模拟天气查询
    # 实际应用中应该调用真实的天气API
    mock_weather_data = {
        "北京": "今天北京天气晴朗，温度 15-25°C，微风，空气质量良好",
        "上海": "今天上海天气多云，温度 18-26°C，东南风3级，空气质量良",
        "广州": "今天广州天气阴转小雨，温度 22-30°C，南风2-3级，空气质量优",
        "深圳": "今天深圳天气晴间多云，温度 23-31°C，微风，空气质量优",
    }

    weather_info = mock_weather_data.get(city, f"抱歉，暂未收录 {city} 的天气信息")

    logger.info(f"天气查询结果: {weather_info}")
    return weather_info


def get_weather_tools() -> list[Any]:
    """获取天气子智能体的工具列表"""
    return [query_weather]
