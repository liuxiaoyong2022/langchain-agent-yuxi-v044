"""Image Subagent - 图片生成子智能体配置"""

from src.agents.master_sub_agent.prompts import IMAGE_AGENT_PROMPT
from src.agents.master_sub_agent.tools import get_image_tools


def get_image_subagent() -> dict:
    """
    获取图片生成子智能体配置

    Returns:
        子智能体配置字典
    """
    return {
        "name": "image_agent",
        "description": (
            "图片生成专家，负责根据用户需求生成图片。"
            "包括收集图片信息（描述、风格、尺寸、数量）、验证尺寸格式、"
            "生成前确认并执行生成。"
        ),
        "system_prompt": IMAGE_AGENT_PROMPT,
        "tools": get_image_tools(),
        "interrupt_on": {
            # Override: require approval for reads in this subagent
            "generate_image": {
                    "allowed_decisions": ["approve", "reject"],
                },
    
        }         
    }
