"""Master-Sub Agent Tools - 所有子智能体使用的工具函数"""

import re
import time
from typing import Any

from langchain.tools import tool
from langgraph.types import interrupt

from src.utils import logger


# ========== 邮件相关工具 ==========
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


# ========== 图片生成相关工具 ==========
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
    logger.info(f"即将生成图片 - 描述: {description}, 风格: {style}, 尺寸: {width}x{height}, 数量: {count}")

        # 模拟图片生成
    time.sleep(3)
    logger.info(f"generate_image 图片生成成功 - 风格: {style}, 数量: {count}")
    return f"已成功生成 {count} 张 {style} 风格的图片（尺寸: {width}x{height}）"

    # 暂停并等待用户确认
    # response = interrupt({
    #     "action": "generate_image",
    #     "description": description,
    #     "style": style,
    #     "width": width,
    #     "height": height,
    #     "count": count,
    #     "message": "请确认是否生成图片？",
    # })

    # # 从中断中恢复
    # user_action = response["decisions"][0]["type"]
    # logger.info(f"用户决策: {user_action}")

    # if user_action == "approve":
    #     # 模拟图片生成
    #     time.sleep(3)
    #     logger.info(f"图片生成成功 - 风格: {style}, 数量: {count}")
    #     return f"已成功生成 {count} 张 {style} 风格的图片（尺寸: {width}x{height}）"
    # else:
    #     logger.info(f"用户取消生成图片")
    #     return "图片生成已被用户取消"


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


# ========== TTS相关工具 ==========
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
    logger.info(f"即将生成TTS - 内容: {tts_content[:50]}..., 使用默认声音: {use_default}")

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
    logger.info(f"用户决策: {user_action}")

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
    生成语音（TTS）工具

    Args:
        tts_content: 需要转换为语音的文本内容
        voice_sample_url: 语音样本文件URL（可选，空字符串使用默认）

    Returns:
        生成结果信息
    """
    use_default = not voice_sample_url
    logger.info(f"即将生成TTS - 内容: {tts_content[:50]}..., 使用默认声音: {use_default}")

    # 暂停并等待用户确认
    # response = interrupt({
    #     "action": "generate_tts",
    #     "tts_content": tts_content,
    #     "voice_sample_url": voice_sample_url,
    #     "use_default_voice": use_default,
    #     "message": "请确认是否生成语音？",
    # })

    # 从中断中恢复
    # user_action = response["decisions"][0]["type"]
    # logger.info(f"用户决策: {user_action}")

            # 模拟TTS生成
    time.sleep(2)
    logger.info(f"TTS_2生成成功 - 内容长度: {len(tts_content)}")
    return f"语音已成功生成（内容长度: {len(tts_content)} 字符）"



# ========== 天气查询相关工具 ==========
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


# ========== 数字人相关工具 ==========
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
    logger.info(f"即将创建数字人 - 图片: {digital_image}, 内容长度: {len(digital_content)}, 使用默认声音: {use_default}")
    # 模拟数字人视频制作
    time.sleep(5)
    logger.info(f"interrupt on tool 数字人视频制作成功 - 内容长度: {len(digital_content)}")
    return f"数字人视频已成功制作（口播文稿长度: {len(digital_content)} 字符）"

    # # 暂停并等待用户确认
    # response = interrupt({
    #     "action": "create_digital_human",
    #     "digital_image": digital_image,
    #     "digital_content": digital_content,
    #     "digital_sample": digital_sample,
    #     "use_default_voice": use_default,
    #     "message": "请确认是否制作数字人视频？",
    # })

    # # 从中断中恢复
    # user_action = response["decisions"][0]["type"]
    # logger.info(f"用户决策: {user_action}")

    # if user_action == "approve":
    #     # 模拟数字人视频制作
    #     time.sleep(5)
    #     logger.info(f"数字人视频制作成功 - 内容长度: {len(digital_content)}")
    #     return f"数字人视频已成功制作（口播文稿长度: {len(digital_content)} 字符）"
    # else:
    #     logger.info(f"用户取消制作数字人视频")
    #     return "数字人视频制作已被用户取消"


# ========== 工具分组函数 ==========
def get_mail_tools() -> list[Any]:
    """获取邮件子智能体的工具列表"""
    return [send_email, validate_email]


def get_image_tools() -> list[Any]:
    """获取图片生成子智能体的工具列表"""
    return [generate_image, validate_image_size]


def get_tts_tools() -> list[Any]:
    """获取TTS子智能体的工具列表"""
    return [generate_tts_2]


def get_weather_tools() -> list[Any]:
    """获取天气子智能体的工具列表"""
    return [query_weather]


def get_digital_human_tools() -> list[Any]:
    """获取数字人子智能体的工具列表"""
    return [create_digital_human]


def get_all_subagent_tools() -> dict[str, list[Any]]:
    """获取所有子智能体的工具映射"""
    return {
        "mail_agent": get_mail_tools(),
        "image_agent": get_image_tools(),
        "tts_agent": get_tts_tools(),
        "weather_agent": get_weather_tools(),
        "digital_human_agent": get_digital_human_tools(),
    }
