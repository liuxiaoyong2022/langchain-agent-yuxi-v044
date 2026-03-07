"""Digital Human Agent Tools - 数字人子智能体使用的工具函数"""

import time
from typing import Any

from langchain.tools import tool

from src.utils import logger


@tool
def create_digital_human(digital_image: str, digital_content: str, digital_sample: str = "") -> str:
    """
    创建数字人视频工具

    Args:
        digital_image: 数字人形象图片URL或路径
        digital_content: 数字人口播文稿
        digital_sample: 数字人声音样本URL或路径（可选，空字符串使用默认）

    Returns:
        生成结果信息
    """
    use_default = not digital_sample
    logger.info(
        f"即将创建数字人 - 图片: {digital_image}, 内容长度: {len(digital_content)}, 使用默认声音: {use_default}"
    )
    # 模拟数字人视频制作
    time.sleep(5)
    logger.info(f"interrupt on tool 数字人视频制作成功 - 内容长度: {len(digital_content)}")
    return f"数字人视频已成功制作（口播文稿长度: {len(digital_content)} 字符）"


def get_digital_human_tools() -> list[Any]:
    """获取数字人子智能体的工具列表"""
    return [create_digital_human]
