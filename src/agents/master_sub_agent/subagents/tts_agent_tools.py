"""TTS Agent Tools - TTS子智能体使用的工具函数"""

import time
from typing import Any

from langchain.tools import tool
from langgraph.types import interrupt

from src.utils import logger


@tool
def generate_tts(tts_content: str, voice_sample_url: str = "") -> str:
    """
    生成语音（TTS）工具

    Args:
        tts_content: 需要转换为语音的文本内容
        voice_sample_url: 语音样本文件URL（可选，空字符串使用默认）

    Returns:
        生成结果信息
    """
    use_default = not voice_sample_url
    logger.info(f"step 3.0.0 ---> 即将进入human_in_loop中断 生成TTS - 内容: {tts_content[:50]}..., 使用默认声音: {use_default}")

    # 暂停并等待用户确认
    response = interrupt({
        "action": "generate_tts",
        "tts_content": tts_content,
        "voice_sample_url": voice_sample_url,
        "use_default_voice": use_default,
        "message": "请确认是否生成语音？",
    })

    # 从中断中恢复
    user_action = response["decisions"][0]["type"]
    logger.info(f"step 3.0.1 --->即将进入human_in_loop中断恢复 用户决策: {user_action}")

    if user_action == "approve":
        # 模拟TTS生成
        time.sleep(2)
        logger.info(f"TTS生成成功 - 内容长度: {len(tts_content)}")
        return f"语音已成功生成（内容长度: {len(tts_content)} 字符）"
    else:
        logger.info(f"用户取消生成TTS")
        return "TTS生成已被用户取消"


@tool
def generate_tts_2(tts_content: str, voice_sample_url: str = "") -> str:
    """
    生成语音（TTS）工具 v2

    Args:
        tts_content: 需要转换为语音的文本内容
        voice_sample_url: 语音样本文件URL（可选，空字符串使用默认）

    Returns:
        生成结果信息
    """
    use_default = not voice_sample_url
    logger.info(f"即将生成TTS - 内容: {tts_content[:50]}..., 使用默认声音: {use_default}")

    # 模拟TTS生成
    time.sleep(2)
    logger.info(f"TTS_2生成成功 - 内容长度: {len(tts_content)}")
    return f"语音已成功生成（内容长度: {len(tts_content)} 字符）"


def get_tts_tools() -> list[Any]:
    """获取TTS子智能体的工具列表"""
    return [generate_tts]
