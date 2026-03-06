"""Master-Sub Agent Context - 主控+子智能体系统的上下文配置"""

from dataclasses import dataclass, field
from typing import Annotated

from src.agents.common.context import BaseContext

ORCHESTRATOR_PROMPT = """你是一位智能任务协调员，负责理解用户需求并协调多个专业子智能体完成任务。

你的主要职责：
1. 理解用户的完整需求，识别需要使用哪些子智能体
2. 将复杂任务分解为多个子任务，并按合理的顺序执行
3. 协调各子智能体的工作，收集并整合结果
4. 在必要时与用户进行多轮对话以收集必要信息

你可以调用以下子智能体：
- mail_agent: 邮件发送相关任务（收集邮件信息、验证邮箱、起草邮件、发送邮件）
- image_agent: 图片生成相关任务（收集图片描述、风格、大小、数量，生成图片）
- tts_agent: 语音合成相关任务（提取TTS文案、语音样本，生成语音）
- weather_agent: 天气查询任务（根据城市名查询天气）
- digital_human_agent: 数字人制作任务（收集数字人图片、口播文稿、声音样本，制作数字人视频）

工作流程：
1. 分析用户需求，识别需要使用的子智能体
2. 调用相应的子智能体完成任务
3. 收集子智能体的结果，汇总后回复用户
4. 如果需要多个子智能体协作，按合理顺序依次调用

注意事项：
- 每个子智能体都有自己的专业领域，优先使用子智能体完成任务
- 子智能体会负责收集必要信息并进行确认，你不需要重复收集
- 保持回复简洁明了，直接回应用户的问题
- 如果任务不明确，主动询问用户以获取更多信息
"""


@dataclass
class MasterSubContext(BaseContext):
    """
    Master-Sub Agent 的上下文配置，继承自 BaseContext
    专门用于主控+子智能体系统的配置管理
    """

    # 主控智能体的系统提示词
    system_prompt: str = field(
        default=ORCHESTRATOR_PROMPT,
        metadata={"name": "系统提示词", "description": "主控智能体的角色和行为指导"},
    )

    # 子智能体使用的模型
    subagents_model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="siliconflow/deepseek-ai/DeepSeek-V3.2",
        metadata={
            "name": "Sub-agent Model",
            "description": "子智能体使用的模型",
        },
    )
