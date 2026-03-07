"""Master-Sub Agent Graph - 主控+子智能体系统的核心实现"""

from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt

from src.agents.common import BaseAgent, load_chat_model
from src.agents.common.middlewares import context_aware_prompt, context_based_model
from src.agents.master_sub_agent.context import MasterSubContext
from src.agents.master_sub_agent.subagents import (
    get_digital_human_subagent,
    get_image_subagent,
    get_mail_subagent,
    get_tts_subagent,
)
from src.agents.master_sub_agent.subagents.skill_study_agent import get_skill_study_subagent


@dynamic_prompt
def orchestrator_prompt(request: ModelRequest) -> str:
    """从 runtime context 动态生成主控智能体提示词"""
    context = MasterSubContext.from_file(module_name="master_sub_agent")
    return context.system_prompt


class MasterSubAgent(BaseAgent):
    """
    主控+子智能体系统

    这是一个基于 LangGraph 1.x 的主智能体，负责协调多个专业子智能体完成任务。

    架构特点：
    - 主控智能体（Orchestrator）：对话入口、意图识别、任务分发、结果汇总
    - 子智能体系统：4个专业子智能体 + 1个技能学习型子智能体
    - 支持多轮对话收集信息
    - 支持用户确认机制
    - 支持任务规划和执行

    子智能体列表：
    - mail_agent: 邮件发送
    - image_agent: 图片生成
    - tts_agent: 语音合成
    - digital_human_agent: 数字人制作
    - skill_study_agent: 技能学习型子智能体（处理天气查询、PDF 等其他任务）
    """

    name = "主控子智能体系统"
    description = "具备任务协调和多子智能体协作能力的智能体系统，可以处理邮件、图片生成、TTS、数字人制作等多种任务，并通过技能学习型子智能体处理更多通用任务"
    context_schema = MasterSubContext
    capabilities = [
        "email",
        "image_generation",
        "tts",
        "digital_human",
        "skill_learning",
        "weather_query",
        "pdf_processing",
        "multi_agent_coordination",
        "file_upload",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph = None

    async def get_graph(self, **kwargs):
        """构建主控+子智能体系统的图"""
        if self.graph:
            return self.graph

        # 获取上下文配置
        context = self.context_schema.from_file(module_name=self.module_name)

        # 加载模型
        model = load_chat_model(context.model)
        sub_model = load_chat_model(context.subagents_model)

        # 获取所有子智能体配置
        subagents = [
            get_mail_subagent(),
            get_image_subagent(),
            get_tts_subagent(),
            get_digital_human_subagent(),
            get_skill_study_subagent(),
        ]

        # 使用 create_agent 创建主智能体，集成子智能体
        graph = create_agent(
            model=model,
            tools=[],  # 主智能体本身不直接使用工具，通过子智能体完成任务
            system_prompt=context.system_prompt,
            middleware=[
                orchestrator_prompt,  # 动态主控提示词
                context_aware_prompt,  # 上下文感知提示词
                context_based_model,  # 基于上下文的模型选择
                SubAgentMiddleware(
                    default_model=sub_model,
                    default_tools=[],
                    subagents=subagents,
                    default_middleware=[
                        # 子智能体的中间件
                        context_aware_prompt,
                        context_based_model,
                    ],
                    general_purpose_agent=False,  # 不启用通用智能体，只使用定义的子智能体
                ),
            ],
            checkpointer=await self._get_checkpointer(),
        )

        self.graph = graph
        return graph
