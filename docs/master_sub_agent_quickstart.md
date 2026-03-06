# 主控+子智能体系统 - 快速启动指南

## 🚀 快速开始

### 1. 验证安装

运行测试脚本验证系统是否正常工作：

```bash
python test/master_sub_agent_test.py
```

预期输出：
```
✓ 自动发现智能体: MasterSubAgent 来自 master_sub_agent
✓ 所有子智能体配置测试通过
✓ 所有工具函数测试通过
✓ 智能体创建测试通过
✓ 智能体信息获取测试通过
```

### 2. 启动服务器

使用 Docker Compose 启动开发服务器：

```bash
docker compose up -d
```

### 3. 通过 API 使用

查看可用的智能体：

```bash
curl http://localhost:8000/chat/agents
```

使用智能体进行对话：

```bash
curl -X POST http://localhost:8000/chat/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "MasterSubAgent",
    "message": "北京今天天气怎么样？"
  }'
```

## 📖 使用场景示例

### 场景1: 邮件发送

```
用户: 帮我给 alice@example.com 发一封邮件
助手: 请提供邮件主题
用户: 项目进展汇报
助手: 请提供邮件内容
用户: 我们已完成第一阶段工作
助手: 请确认：
  收件人: alice@example.com
  主题: 项目进展汇报
  内容: 我们已完成第一阶段工作
  是否发送？(yes/no)
用户: yes
助手: ✓ 邮件已发送
```

### 场景2: 图片生成

```
用户: 生成一张图片，画一只在森林里的狐狸
助手: 请指定图片风格（写实/印象派/卡通/油画）
用户: 写实风格
助手: 请指定图片尺寸（如 1024*768）
用户: 1024*768
助手: 请确认：
  描述: 一只在森林里的狐狸
  风格: 写实
  尺寸: 1024x768
  张数: 1
  是否生成？(yes/no)
用户: yes
助手: ✓ 已成功生成 1 张写实风格的图片
```

### 场景3: 天气查询

```
用户: 北京今天天气怎么样？
助手: 今天北京天气晴朗，温度 15-25°C，微风，空气质量良好
```

### 场景4: TTS语音合成

```
用户: 把这句话转换成语音：欢迎使用智能语音助手
助手: 请确认：
  文案: 欢迎使用智能语音助手
  语音: 默认语音
  是否生成？(yes/no)
用户: yes
助手: ✓ 语音已成功生成
```

### 场景5: 数字人制作

```
用户: 帮我制作一个数字人视频
助手: 请提供数字人形象图片
用户: /path/to/avatar.png
助手: 请提供口播文稿
用户: 我们的产品非常优秀
助手: 请确认：
  形象图片: /path/to/avatar.png
  口播文稿: 我们的产品非常优秀
  声音: 默认声音
  是否制作？(yes/no)
用户: yes
助手: ✓ 数字人视频已成功制作
```

## 🧪 测试示例

### 运行基础测试

```bash
python test/master_sub_agent_test.py
```

### 运行使用示例

```bash
python examples/master_sub_agent_usage.py
```

### 运行API示例

```bash
# 先启动服务器
docker compose up -d

# 然后运行API示例
python examples/api_usage_example.py
```

## 🔧 配置

### 模型配置

智能体使用项目配置的默认模型。可以在 `saves/config/base.toml` 中修改：

```toml
[model]
default = "deepseek:deepseek-chat"

# 子智能体专用模型
[subagents_model]
default = "siliconflow/deepseek-ai/DeepSeek-V3.2"
```

### 主控提示词

修改 `src/agents/master_sub_agent/context.py` 中的 `ORCHESTRATOR_PROMPT` 来自定义主控智能体的行为。

### 子智能体提示词

修改 `src/agents/master_sub_agent/prompts.py` 中对应的提示词来自定义各个子智能体的行为。

## 📚 文档

- [README](src/agents/master_sub_agent/README.md) - 详细使用文档
- [实现总结](docs/master_sub_agent_implementation.md) - 开发总结和架构说明
- [需求文档](docs/master_and_multi_agent.md) - 原始需求

## 🎯 核心特性

- ✅ **多轮对话** - 智能收集必要信息
- ✅ **用户确认** - 所有关键操作需要明确确认
- ✅ **参数验证** - 自动验证邮箱、尺寸等参数
- ✅ **任务协调** - 主控智能体智能分配任务
- ✅ **历史记录** - SQLite 持久化存储对话历史

## 🛠️ 开发

### 添加新的子智能体

1. 在 `subagents/` 创建新文件
2. 在 `prompts.py` 添加提示词
3. 在 `tools.py` 添加工具函数
4. 在 `subagents/__init__.py` 导出
5. 在 `graph.py` 注册

详见 [README](src/agents/master_sub_agent/README.md) 的开发指南。

## ⚠️ 注意事项

1. 所有关键操作都使用 `interrupt()` 等待用户确认
2. 当前实现为模拟功能，需要接入真实API
3. 前端需要实现用户确认的UI界面
4. 对话历史保存在 `saves/agents/master_sub_agent/aio_history.db`

## 🐛 故障排除

### 智能体未被识别

检查文件结构和导入是否正确：

```bash
python -c "from src.agents.master_sub_agent import MasterSubAgent; print('OK')"
```

### API无法访问

确保服务器正在运行：

```bash
docker ps | grep api-dev
```

### 查看日志

```bash
docker logs api-dev --tail 100
```

## 📞 支持

如有问题，请查看：
1. [README](src/agents/master_sub_agent/README.md)
2. [实现总结](docs/master_sub_agent_implementation.md)
3. 测试脚本 `test/master_sub_agent_test.py`
4. 使用示例 `examples/master_sub_agent_usage.py`

---

**祝使用愉快！** 🎉
