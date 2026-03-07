"""Skill Study Agent - 技能学习子智能体"""

from pathlib import Path

from .core_tools import initialize_core_tools
from .prompt_builder import PromptBuilder


def get_skill_study_subagent() -> dict:
    """
    获取技能学习子智能体配置

    Returns:
        子智能体配置字典
    """
    # 获取当前目录
    current_dir = Path(__file__).parent

    # 初始化 Prompt Builder
    prompt_builder = PromptBuilder(
        workspace_dir=current_dir / "workspace",
        memory_dir=current_dir / "memory",
        skills_dir=current_dir / "skills"
    )

    # 构建系统提示词
    system_prompt = prompt_builder.build_system_prompt()

    # 初始化核心工具
    tools = initialize_core_tools(current_dir)

    return {
        "name": "skill_study_agent",
        "description": (
            "通用技能学习型子智能体，能够通过学习和执行技能来处理多种任务。"
            "当现有专业子智能体（邮件、图片生成、TTS、数字人）无法处理任务时，"
            "主控智能体会将任务路由到此智能体。"
            "支持天气查询、PDF处理等多种技能，并可以通过学习新的技能来扩展能力。"
        ),
        "system_prompt": system_prompt,
        "tools": tools,
    }
