"""TTS Subagent - TTS子智能体配置"""

from src.agents.master_sub_agent.prompts import TTS_AGENT_PROMPT
from .tts_agent_tools import get_tts_tools


def get_tts_subagent() -> dict:
    """
    获取TTS子智能体配置

    Returns:
        子智能体配置字典
    """
    return {
        "name": "tts_agent",
        "description": (
            "语音合成专家，负责将文字转换为语音。"
            "包括收集TTS信息（文案内容、语音样本）、"
            "生成前确认并执行TTS生成。"
        ),
        "system_prompt": TTS_AGENT_PROMPT,
        "tools": get_tts_tools(),
        # "interrupt_on": {
        #     # Override: require approval for reads in this subagent
        #     "generate_tts_2": {
        #             "allowed_decisions": ["approve", "reject"],
        #         },
    
        # }    
    }
