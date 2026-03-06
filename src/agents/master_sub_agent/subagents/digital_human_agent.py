"""Digital Human Subagent - 数字人子智能体配置"""

from src.agents.master_sub_agent.prompts import DIGITAL_HUMAN_AGENT_PROMPT
from src.agents.master_sub_agent.tools import get_digital_human_tools


def get_digital_human_subagent() -> dict:
    """
    获取数字人子智能体配置

    Returns:
        子智能体配置字典
    """
    return {
        "name": "digital_human_agent",
        "description": (
            "数字人制作专家，负责制作数字人视频。"
            "包括收集数字人信息（形象图片、口播文稿、声音样本）"
            "制作前确认并执行数字人视频制作。"
        ),
        "system_prompt": DIGITAL_HUMAN_AGENT_PROMPT,
        "tools": get_digital_human_tools(),
        "interrupt_on": {
            # Override: require approval for reads in this subagent
            "create_digital_human": {
                    "allowed_decisions": ["approve", "reject"],
                },
    
        } 
    }
