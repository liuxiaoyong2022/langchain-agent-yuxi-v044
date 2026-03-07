"""Image Agent Tools - 图片生成子智能体使用的工具函数"""

import re
import time
from typing import Any

from langchain.tools import tool

from src.utils import logger


@tool
def generate_image(description: str, style: str, width: int, height: int, count: int) -> str:
    """
    生成图片工具

    Args:
        description: 图片描述
        style: 图片风格（写实、印象派、卡通、油画等）
        width: 图片宽度（像素）
        height: 图片高度（像素）
        count: 生成图片的张数

    Returns:
        生成结果信息
    """
    logger.info(f"step 2.0.1 ---> 即将生成图片 - 描述: {description}, 风格: {style}, 尺寸: {width}x{height}, 数量: {count}")

    # 模拟图片生成
    time.sleep(3)
    logger.info(f"step 2.0.2 ---> generate_image 图片生成成功 - 风格: {style}, 数量: {count}")
    return f"已成功生成 {count} 张 {style} 风格的图片（尺寸: {width}x{height}）"


@tool
def validate_image_size(size_str: str) -> dict[str, Any]:
    """
    验证图片尺寸格式

    Args:
        size_str: 尺寸字符串（格式: "1024*768" 或 "1024x768"）

    Returns:
        验证结果，包含 is_valid, width, height, message
    """
    # 支持 * 或 x 作为分隔符
    pattern = r'^(\d+)[\*x](\d+)$'
    match = re.match(pattern, size_str.strip())

    if match:
        width = int(match.group(1))
        height = int(match.group(2))

        # 合理性检查
        if width < 64 or height < 64:
            return {"is_valid": False, "message": "图片尺寸过小，最小为 64x64"}
        if width > 4096 or height > 4096:
            return {"is_valid": False, "message": "图片尺寸过大，最大为 4096x4096"}

        return {
            "is_valid": True,
            "width": width,
            "height": height,
            "message": f"图片尺寸格式正确: {width}x{height}"
        }
    else:
        return {"is_valid": False, "message": "图片尺寸格式不正确，应为 '宽*高' 或 '宽x高'（如: 1024*768）"}


def get_image_tools() -> list[Any]:
    """获取图片生成子智能体的工具列表"""
    return [generate_image, validate_image_size]
