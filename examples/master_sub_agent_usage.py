"""主控+子智能体系统使用示例

展示如何在实际应用中使用 MasterSubAgent
"""

import asyncio
from src.agents import agent_manager
from src.utils import logger


async def example_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("示例1: 基本使用")
    print("=" * 60)

    # 获取智能体实例
    agent = agent_manager.get_agent("MasterSubAgent")

    # 获取智能体信息
    info = await agent.get_info()
    print(f"\n智能体名称: {info['name']}")
    print(f"智能体描述: {info['description']}")

    # 准备消息
    messages = [
        {"role": "user", "content": "帮我查询一下北京的天气"}
    ]

    # 准备上下文（包含用户ID、线程ID等）
    input_context = {
        "user_id": "test_user",
        "thread_id": "test_thread_001",
    }

    # 流式输出消息
    print("\n开始对话:")
    async for message, metadata in agent.stream_messages(messages, input_context):
        if hasattr(message, 'content'):
            print(f"{message.role}: {message.content}")

    print("\n✓ 对话完成")


async def example_email_task():
    """邮件发送任务示例"""
    print("\n" + "=" * 60)
    print("示例2: 邮件发送任务")
    print("=" * 60)

    agent = agent_manager.get_agent("MasterSubAgent")

    messages = [
        {"role": "user", "content": "帮我给 alice@example.com 发一封邮件，主题是项目进展"}
    ]

    input_context = {
        "user_id": "test_user",
        "thread_id": "test_thread_002",
    }

    print("\n开始对话（邮件发送会触发用户确认）:")
    print("注意: 实际使用中，send_email 会触发 interrupt() 等待用户确认")

    async for message, metadata in agent.stream_messages(messages, input_context):
        if hasattr(message, 'content'):
            print(f"{message.role}: {message.content}")

    print("\n✓ 邮件任务示例完成")


async def example_multi_turn_conversation():
    """多轮对话示例"""
    print("\n" + "=" * 60)
    print("示例3: 多轮对话")
    print("=" * 60)

    agent = agent_manager.get_agent("MasterSubAgent")

    # 第一轮对话
    print("\n第一轮对话:")
    messages = [
        {"role": "user", "content": "我想生成一张图片"}
    ]

    input_context = {
        "user_id": "test_user",
        "thread_id": "test_thread_003",
    }

    async for message, metadata in agent.stream_messages(messages, input_context):
        if hasattr(message, 'content'):
            print(f"{message.role}: {message.content}")

    # 第二轮对话（补充信息）
    print("\n第二轮对话（补充图片描述）:")
    # 注意：实际使用中，需要从上一轮的响应中提取消息
    messages.append({
        "role": "assistant",
        "content": "请提供图片的详细描述"
    })
    messages.append({
        "role": "user",
        "content": "一只在森林里的狐狸，写实风格"
    })

    async for message, metadata in agent.stream_messages(messages, input_context):
        if hasattr(message, 'content'):
            print(f"{message.role}: {message.content}")

    print("\n✓ 多轮对话示例完成")


async def example_get_history():
    """获取历史记录示例"""
    print("\n" + "=" * 60)
    print("示例4: 获取历史记录")
    print("=" * 60)

    agent = agent_manager.get_agent("MasterSubAgent")

    # 获取历史消息
    user_id = "test_user"
    thread_id = "test_thread_001"

    history = await agent.get_history(user_id, thread_id)

    print(f"\n历史消息数量: {len(history)}")
    for i, msg in enumerate(history[-3:], 1):  # 只显示最后3条
        if isinstance(msg, dict):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            print(f"\n消息 {i}:")
            print(f"  角色: {role}")
            print(f"  内容: {content[:100]}...")

    print("\n✓ 历史记录获取完成")


async def example_list_all_capabilities():
    """列出所有能力示例"""
    print("\n" + "=" * 60)
    print("示例5: 列出所有能力")
    print("=" * 60)

    agent = agent_manager.get_agent("MasterSubAgent")
    info = await agent.get_info()

    print("\n智能体能力:")
    for capability in info['capabilities']:
        print(f"  - {capability}")

    print("\n可用功能:")
    print("  1. 邮件发送")
    print("  2. 图片生成")
    print("  3. 语音合成（TTS）")
    print("  4. 天气查询")
    print("  5. 数字人制作")

    print("\n✓ 能力列表获取完成")


async def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("主控+子智能体系统使用示例")
    print("=" * 60)

    try:
        # 运行所有示例
        await example_list_all_capabilities()
        await example_basic_usage()
        # 注意：以下示例需要实际配置 LLM 并可能触发用户确认
        # 在生产环境中使用
        # await example_email_task()
        # await example_multi_turn_conversation()
        # await example_get_history()

        print("\n" + "=" * 60)
        print("所有示例运行完成！")
        print("=" * 60)
        print("\n提示: 完整功能需要在实际应用中配置 LLM 和用户确认机制")

    except Exception as e:
        logger.error(f"示例运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
