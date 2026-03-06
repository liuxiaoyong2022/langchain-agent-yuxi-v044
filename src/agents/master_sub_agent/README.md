# 主控+子智能体系统 (Master-Sub Agent System)

基于 LangGraph 1.x + deepagents 构建的主智能体+多子智能体协作系统。

## 系统架构

### 主控智能体（Orchestrator Agent）
- **职责**：对话入口、意图识别、任务分发、结果汇总、与用户交互
- **功能**：理解用户需求，协调多个专业子智能体完成任务

### 子智能体系统
系统包含5个专业子智能体，各司其职：

| 子智能体 | 功能描述 |
|---------|---------|
| **mail_agent** | 邮件发送 - 收集邮件信息、验证邮箱、起草邮件、发送前确认 |
| **image_agent** | 图片生成 - 收集图片描述、风格、尺寸、数量，生成前确认 |
| **tts_agent** | 语音合成 - 收集TTS文案、语音样本，生成前确认 |
| **weather_agent** | 天气查询 - 根据城市名查询天气信息 |
| **digital_human_agent** | 数字人制作 - 收集形象图片、口播文稿、声音样本，制作前确认 |

## 核心特性

✅ **多轮对话收集信息** - 每个子智能体都能通过多轮对话收集必要信息
✅ **用户确认机制** - 所有关键操作都需要用户明确确认（yes/no）后才执行
✅ **任务协调** - 主控智能体智能分配任务给合适的子智能体
✅ **参数验证** - 对邮箱格式、图片尺寸等进行自动验证
✅ **历史记录** - 支持 SQLite 持久化存储对话历史

## 目录结构

```
src/agents/master_sub_agent/
├── __init__.py           # 模块导出
├── context.py            # 上下文配置
├── graph.py              # 主智能体实现
├── prompts.py            # 所有子智能体的提示词
├── tools.py              # 所有子智能体的工具函数
├── metadata.toml         # 智能体元数据和示例
├── README.md             # 本文档
└── subagents/            # 子智能体配置
    ├── __init__.py
    ├── mail_agent.py
    ├── image_agent.py
    ├── tts_agent.py
    ├── weather_agent.py
    └── digital_human_agent.py
```

## 使用示例

### 1. 邮件发送任务
```
用户: 帮我给 alice@example.com 发一封邮件，主题是项目进展

主控智能体: 识别到邮件任务，调用 mail_agent

mail_agent: 请输入邮件内容
用户: 我们已经完成了第一阶段的工作

mail_agent: 请确认以下信息：
  收件人: alice@example.com
  主题: 项目进展
  内容: 我们已经完成了第一阶段的工作

  是否发送？(yes/no)
用户: yes

mail_agent: ✓ 邮件已成功发送至 alice@example.com
```

### 2. 图片生成任务
```
用户: 生成一张图片，画一只在森林里的狐狸

主控智能体: 识别到图片生成任务，调用 image_agent

image_agent: 请指定图片风格（如：写实、印象派、卡通、油画）
用户: 写实风格

image_agent: 请指定图片尺寸（如：1024*768）
用户: 1024*768

image_agent: 请确认以下信息：
  描述: 一只在森林里的狐狸
  风格: 写实
  尺寸: 1024 x 768
  张数: 1

  是否生成？(yes/no)
用户: yes

image_agent: ✓ 已成功生成 1 张 写实 风格的图片
```

### 3. 天气查询任务
```
用户: 北京今天天气怎么样？

主控智能体: 识别到天气查询任务，调用 weather_agent

weather_agent: 今天北京天气晴朗，温度 15-25°C，微风，空气质量良好
```

## 开发指南

### 添加新的子智能体

1. 在 `subagents/` 目录下创建新的 Python 文件（如 `my_agent.py`）
2. 在 `prompts.py` 中添加对应的提示词
3. 在 `tools.py` 中添加对应的工具函数
4. 在 `subagents/__init__.py` 中导出新的子智能体函数
5. 在 `graph.py` 中注册新的子智能体

示例：
```python
# subagents/my_agent.py
from src.agents.master_sub_agent.prompts import MY_AGENT_PROMPT
from src.agents.master_sub_agent.tools import get_my_tools

def get_my_subagent() -> dict:
    return {
        "name": "my_agent",
        "description": "我的子智能体描述",
        "system_prompt": MY_AGENT_PROMPT,
        "tools": get_my_tools(),
    }
```

### 自定义主控提示词

修改 `context.py` 中的 `ORCHESTRATOR_PROMPT` 来自定义主控智能体的行为。

### 配置模型

智能体使用项目配置的默认模型。子智能体使用 `context.py` 中配置的 `subagents_model`。

可以在配置文件中修改：
```toml
[subagents_model]
default = "siliconflow/deepseek-ai/DeepSeek-V3.2"
```

## 工具说明

### 邮件工具
- `send_email(to, subject, body)` - 发送邮件
- `validate_email(email)` - 验证邮箱格式

### 图片工具
- `generate_image(description, style, width, height, count)` - 生成图片
- `validate_image_size(size_str)` - 验证图片尺寸格式

### TTS工具
- `generate_tts(tts_content, voice_sample_url)` - 生成语音

### 天气工具
- `query_weather(city)` - 查询天气

### 数字人工具
- `create_digital_human(digital_image, digital_content, digital_sample)` - 创建数字人视频

## 测试

运行测试脚本验证功能：
```bash
python test/master_sub_agent_test.py
```

## 技术栈

- **LangGraph 1.x** - 图框架，用于构建状态机
- **LangChain** - LLM 应用框架
- **deepagents** - 智能体中间件库
- **SQLite** - 对话历史持久化

## 注意事项

1. 所有关键操作都会触发 `interrupt()` 等待用户确认
2. 子智能体通过 `SubAgentMiddleware` 集成到主智能体
3. 每个子智能体都有独立的提示词和工具集
4. 对话历史保存在 `saves/agents/master_sub_agent/aio_history.db`

## 版本信息

- **版本**: 1.0.0
- **作者**: Yuxi-Know Team
- **更新日期**: 2026-03-06
