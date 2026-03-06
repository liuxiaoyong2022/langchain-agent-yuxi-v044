"""Master-Sub Agent API 使用示例

展示如何通过 HTTP API 使用主控+子智能体系统
"""

import requests
import json
from typing import Optional


class MasterSubAgentAPI:
    """主控+子智能体系统 API 客户端"""

    def __init__(self, base_url: str = "http://localhost:8000", token: Optional[str] = None):
        """
        初始化 API 客户端

        Args:
            base_url: API 基础URL
            token: 认证令牌（如果需要）
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get_agents(self):
        """获取所有可用的智能体列表"""
        response = requests.get(
            f"{self.base_url}/chat/agents",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_agent_info(self, agent_id: str):
        """获取指定智能体的信息"""
        response = requests.get(
            f"{self.base_url}/chat/agents/{agent_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def chat(self, agent_id: str, message: str, thread_id: Optional[str] = None):
        """
        发送聊天消息

        Args:
            agent_id: 智能体ID（如 "MasterSubAgent"）
            message: 用户消息
            thread_id: 会话线程ID（可选）

        Returns:
            响应结果
        """
        payload = {
            "agent_id": agent_id,
            "message": message,
        }
        if thread_id:
            payload["thread_id"] = thread_id

        response = requests.post(
            f"{self.base_url}/chat/chat",
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_history(self, agent_id: str, user_id: str, thread_id: str):
        """获取对话历史"""
        params = {
            "user_id": user_id,
            "thread_id": thread_id,
        }
        response = requests.get(
            f"{self.base_url}/chat/history/{agent_id}",
            params=params,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()


def example_list_agents():
    """示例1: 列出所有智能体"""
    print("=" * 60)
    print("示例1: 列出所有智能体")
    print("=" * 60)

    client = MasterSubAgentAPI()

    try:
        agents = client.get_agents()
        print("\n可用智能体:")
        for agent in agents:
            print(f"\n  ID: {agent['id']}")
            print(f"  名称: {agent['name']}")
            print(f"  描述: {agent['description'][:80]}...")
            print(f"  能力: {', '.join(agent.get('capabilities', []))}")

        # 找到 MasterSubAgent
        master_sub_agent = next((a for a in agents if a['id'] == 'MasterSubAgent'), None)
        if master_sub_agent:
            print("\n✓ 找到主控子智能体系统！")
        else:
            print("\n✗ 未找到主控子智能体系统")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ API请求失败: {e}")
        print("\n提示: 请确保服务器正在运行（docker compose up）")


def example_get_agent_info():
    """示例2: 获取智能体详细信息"""
    print("\n" + "=" * 60)
    print("示例2: 获取智能体详细信息")
    print("=" * 60)

    client = MasterSubAgentAPI()

    try:
        info = client.get_agent_info("MasterSubAgent")
        print("\n智能体详细信息:")
        print(f"  ID: {info['id']}")
        print(f"  名称: {info['name']}")
        print(f"  描述: {info['description']}")
        print(f"\n  能力列表:")
        for capability in info.get('capabilities', []):
            print(f"    - {capability}")

        print(f"\n  配置项:")
        for item in info.get('configurable_items', []):
            print(f"    - {item.get('name')}: {item.get('description')}")

        print(f"\n  示例:")
        for example in info.get('examples', []):
            print(f"    输入: {example.get('user_input')}")
            print(f"    描述: {example.get('description')}")

        print("\n✓ 获取智能体信息成功")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ API请求失败: {e}")


def example_simple_chat():
    """示例3: 简单对话"""
    print("\n" + "=" * 60)
    print("示例3: 简单对话")
    print("=" * 60)

    client = MasterSubAgentAPI()

    try:
        # 天气查询示例（简单的单轮对话）
        print("\n场景: 查询天气")
        response = client.chat(
            agent_id="MasterSubAgent",
            message="北京今天天气怎么样？",
            thread_id="test_weather_thread"
        )

        print(f"\n用户: 北京今天天气怎么样？")
        print(f"\n助手响应:")
        print(response.get("response", "无响应"))

        print("\n✓ 对话完成")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ API请求失败: {e}")


def example_multi_turn_chat():
    """示例4: 多轮对话（模拟）"""
    print("\n" + "=" * 60)
    print("示例4: 多轮对话（模拟）")
    print("=" * 60)

    client = MasterSubAgentAPI()
    thread_id = "test_email_thread"

    try:
        # 第一轮: 发起邮件请求
        print("\n第一轮对话:")
        response1 = client.chat(
            agent_id="MasterSubAgent",
            message="帮我给 alice@example.com 发一封邮件",
            thread_id=thread_id
        )
        print(f"用户: 帮我给 alice@example.com 发一封邮件")
        print(f"助手: {response1.get('response', '无响应')[:100]}...")

        # 第二轮: 提供主题
        print("\n第二轮对话:")
        response2 = client.chat(
            agent_id="MasterSubAgent",
            message="主题是项目进展汇报",
            thread_id=thread_id
        )
        print(f"用户: 主题是项目进展汇报")
        print(f"助手: {response2.get('response', '无响应')[:100]}...")

        # 第三轮: 提供内容
        print("\n第三轮对话:")
        response3 = client.chat(
            agent_id="MasterSubAgent",
            message="内容是我们已经完成了第一阶段的工作",
            thread_id=thread_id
        )
        print(f"用户: 内容是我们已经完成了第一阶段的工作")
        print(f"助手: {response3.get('response', '无响应')[:100]}...")

        print("\n✓ 多轮对话完成")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ API请求失败: {e}")


def example_get_history():
    """示例5: 获取对话历史"""
    print("\n" + "=" * 60)
    print("示例5: 获取对话历史")
    print("=" * 60)

    client = MasterSubAgentAPI()

    try:
        # 先发送一条消息
        client.chat(
            agent_id="MasterSubAgent",
            message="测试消息",
            thread_id="test_history_thread"
        )

        # 获取历史记录
        history = client.get_history(
            agent_id="MasterSubAgent",
            user_id="test_user",
            thread_id="test_history_thread"
        )

        print(f"\n对话历史（共 {len(history)} 条消息）:")
        for i, msg in enumerate(history[-5:], 1):  # 只显示最后5条
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            print(f"\n  消息 {i}:")
            print(f"    角色: {role}")
            print(f"    内容: {content[:80]}...")

        print("\n✓ 获取历史记录成功")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ API请求失败: {e}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("主控+子智能体系统 API 使用示例")
    print("=" * 60)
    print("\n注意: 请确保服务器正在运行（docker compose up）")
    print("如果需要认证，请设置 ADMIN_NAME 和 ADMIN_PASSWORD 环境变量")

    try:
        # 运行所有示例
        example_list_agents()
        example_get_agent_info()
        example_simple_chat()
        # 以下示例可能需要用户交互，暂时注释
        # example_multi_turn_chat()
        # example_get_history()

        print("\n" + "=" * 60)
        print("所有示例运行完成！")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
