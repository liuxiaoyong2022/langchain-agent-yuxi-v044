"""Master-Sub Agent 测试脚本

测试主控+子智能体系统的基本功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.master_sub_agent import MasterSubAgent
from src.agents.master_sub_agent.subagents import (
    get_digital_human_subagent,
    get_image_subagent,
    get_mail_subagent,
    get_tts_subagent,
    get_weather_subagent,
)
from src.agents.master_sub_agent.tools import get_all_subagent_tools


async def test_subagent_configs():
    """测试子智能体配置"""
    print("=" * 60)
    print("测试子智能体配置...")
    print("=" * 60)

    subagents = [
        ("邮件子智能体", get_mail_subagent()),
        ("图片生成子智能体", get_image_subagent()),
        ("TTS子智能体", get_tts_subagent()),
        ("天气子智能体", get_weather_subagent()),
        ("数字人子智能体", get_digital_human_subagent()),
    ]

    for name, config in subagents:
        print(f"\n{name}:")
        print(f"  - 名称: {config['name']}")
        print(f"  - 描述: {config['description'][:80]}...")
        print(f"  - 工具数量: {len(config['tools'])}")
        print(f"  - 提示词长度: {len(config['system_prompt'])} 字符")

    print("\n✓ 所有子智能体配置测试通过")


async def test_tools():
    """测试工具函数"""
    print("\n" + "=" * 60)
    print("测试工具函数...")
    print("=" * 60)

    all_tools = get_all_subagent_tools()
    for agent_name, tools in all_tools.items():
        print(f"\n{agent_name}:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description[:60]}...")

    print("\n✓ 所有工具函数测试通过")


async def test_agent_creation():
    """测试智能体创建"""
    print("\n" + "=" * 60)
    print("测试智能体创建...")
    print("=" * 60)

    try:
        agent = MasterSubAgent()
        print(f"\n智能体创建成功:")
        print(f"  - 名称: {agent.name}")
        print(f"  - 描述: {agent.description[:80]}...")
        print(f"  - 能力: {', '.join(agent.capabilities)}")
        print(f"  - 工作目录: {agent.workdir}")

        print("\n✓ 智能体创建测试通过")
        return agent
    except Exception as e:
        print(f"\n✗ 智能体创建失败: {e}")
        import traceback

        traceback.print_exc()
        return None


async def test_agent_info():
    """测试智能体信息获取"""
    print("\n" + "=" * 60)
    print("测试智能体信息获取...")
    print("=" * 60)

    try:
        agent = MasterSubAgent()
        info = await agent.get_info()

        print(f"\n智能体信息:")
        print(f"  - ID: {info['id']}")
        print(f"  - 名称: {info['name']}")
        print(f"  - 描述: {info['description'][:80]}...")
        print(f"  - 示例数量: {len(info['examples'])}")
        print(f"  - 能力: {', '.join(info['capabilities'])}")
        print(f"  - 有检查点: {info['has_checkpointer']}")

        print("\n✓ 智能体信息获取测试通过")
    except Exception as e:
        print(f"\n✗ 智能体信息获取失败: {e}")
        import traceback

        traceback.print_exc()


async def test_graph_creation():
    """测试图创建（注意：这可能会调用 LLM）"""
    print("\n" + "=" * 60)
    print("测试图创建...")
    print("=" * 60)

    try:
        agent = MasterSubAgent()
        print("\n正在构建图...")
        graph = await agent.get_graph()
        print(f"✓ 图创建成功: {type(graph)}")

        # 测试图的基本信息
        print(f"  - 图类型: {type(graph).__name__}")
        print(f"  - 有检查点: {graph.checkpointer is not None}")

        print("\n✓ 图创建测试通过")
    except Exception as e:
        print(f"\n✗ 图创建失败: {e}")
        import traceback

        traceback.print_exc()


async def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("开始测试主控+子智能体系统")
    print("=" * 60)

    # 运行所有测试
    await test_subagent_configs()
    await test_tools()
    await test_agent_creation()
    await test_agent_info()

    # 图创建测试（可选，需要 LLM 连接）
    print("\n" + "=" * 60)
    print("是否测试图创建？（需要 LLM 连接）")
    print("如果只想测试基本功能，可以跳过此步骤")
    print("=" * 60)
    # 注释掉图创建测试，避免需要 LLM 连接
    # await test_graph_creation()

    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
