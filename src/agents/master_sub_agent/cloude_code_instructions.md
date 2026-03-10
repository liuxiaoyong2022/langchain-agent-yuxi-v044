# 主控+子智能体系统 (Master-Sub Agent)

基于 `deep_agent` 架构，使用 `SubAgentMiddleware` 实现主控智能体和多个子智能体协作。

## 架构设计

```
┌─────────────────────────────────────────────────────┐
│         Master Agent (主控智能体)                     │
│  - 理解用户意图                                       │
│  - 调度子智能体                                       │
│  - 汇总结果                                           │
└─────────────────────────────────────────────────────┘
                          │
                          ├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
                          │              │              │              │              │              │
                          ▼              ▼              ▼              ▼              ▼              ▼
              ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
              │  mail-agent  │  │ image-agent  │  │  tts-agent   │  │weather-agent │  │digital-human │
              │  邮件子智能体  │  │ 图片生成子智能体│  │  TTS子智能体  │  │ 天气查询子智能体│  │    -agent     │
              └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

## 代码优化记录

### 1. 各子智能体工具集拆分
- all_tools 拆分为各子智能体工具集 比如: mail_agent_tools  image_agent_tools,tts_agent_tools 等，
   具体每个子智能体的工具参考 src/agents/master_sub_agent/README.md中的子智能体说明
- 将对应的子智能体工具集 在子智能体初始化时赋值给对应的子智能体
- 代码修改仅限于 src/agents/master_sub_agent目录下，不要修改其它文件

### 2. 各子智能体工具集拆分2
-  将src/agents/master_sub_agent/tools.py 中各个工具 包括 工具分组函数 按功能 拆分到不同的 xxx_agent_tools.py 中去 比如: mail_agent_tools  image_agent_tools,tts_agent_tools 等， 
- 相应重构 graph.py 文件

### 3. 重构master_sub_agent 
- 在src/agents/master_sub_agent下，移出weather_agent 以及相关它的工具和prompt 
- 在master_sub_agent下 新增 skill_study_agent 让它处理现有子智能体以外的任务，即让主控智能体将当前已有子智能体不能完成的任务 路由给它，它可以通过skill学习来处理任务 它的实现可参考 src/agents/mini_openclaw_agent 
- 先让study_agent 实现 get_weather 和 pdf技能 (可参考mini_openclaw_agent)
- 修改仅于master_sub_agent下 不要修改其它目录文件

### 4. 增加pdf附件处理能力
- 分析项目程前端部分 即/web目录下 前端附件上传功能中的文件类型限制,增加pdf上传类型

#### 5. skill 优化 
- 分析 src/agents/master_sub_agent/skill_study_agent/skills/pdf 下的技能 要求在作pdf图片提取时，默认将提取出的图片 保存到 /tmp 目录下  格式为 /tmp/{图片所在文件}/image_extract/{序号}.{格式}  比如
/tmp/2412.09262v2/image_extract/001.jpg

```
用户输入
    ↓
主控智能体理解意图
    ↓
SubAgentMiddleware 路由到对应的子智能体
    ↓
子智能体处理任务
    ↓
子智能体返回结果
    ↓
主控智能体汇总结果
    ↓
返回给用户
```

