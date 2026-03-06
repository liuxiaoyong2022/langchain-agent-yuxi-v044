# 能力记忆库 - MEMORY.md

## 📸 图像生成能力

### **核心技能：mcp-minimax**
- **功能**：根据文字描述生成图片
- **触发条件**：当用户想要从图片描述生成图像时使用
- **技术实现**：通过调用 Minimax API 进行文生图

### **具体能力**
1. **文字到图像生成**：
   - 输入：文字描述（中英文均可）
   - 输出：生成的图片 URL
   - 模型：`image-01` 模型

2. **可配置参数**：
   - 图片比例：如 16:9、1:1、4:3 等
   - 响应格式：base64 编码
   - 输出格式：JPEG 图片

3. **处理流程**：
   - 接收用户图片描述
   - 调用 Minimax API
   - 将 base64 图片保存到临时文件
   - 返回图片访问 URL

### **技术实现代码**
```python
import base64
import requests
import os
from datetime import datetime

def invoke_text_to_image(image_desc: str) -> str:
    """从文字描述生成图片，返回图片的访问地址 URL"""
    minimax_api_key = os.environ["MINIMAX_API_KEY"]
    headers = {"Authorization": f"Bearer {minimax_api_key}"}
    
    url = "https://api.minimax.io/v1/image_generation"
    payload = {
        "model": "image-01",
        "prompt": image_desc,
        "aspect_ratio": "16:9",
        "response_format": "base64",
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    images = response.json()["data"]["image_base64"]
    image_url = None
    
    for i in range(len(images)):
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        file_path = f"/tmp/nginx/static/image/gen_out_put/{filename}"
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(images[i]))
        image_url = f"http://localhost:8080/static/image/gen_out_put/{filename}"
    
    return image_url
```

### **使用场景**
- 创意设计：根据想法生成视觉内容
- 概念可视化：将抽象概念转化为图像
- 内容创作：为文章、演示文稿生成配图
- 原型设计：快速生成设计概念图

### **限制说明**
1. 需要有效的 Minimax API 密钥
2. 生成质量取决于描述的具体程度
3. 可能需要多次尝试调整描述以获得理想结果

### **最佳实践**
1. **详细描述**：提供具体、详细的描述
2. **风格说明**：指定想要的风格（如卡通、写实、水彩等）
3. **元素明确**：清晰描述画面中的各个元素
4. **比例要求**：如有特殊比例需求请提前说明

### **示例描述**
- "生成一张日落的风景图，有橙红色的天空和剪影的椰子树"
- "创建一张猫在窗台上的卡通图片，风格温馨可爱"
- "制作一个科技感十足的抽象图案，蓝色和紫色渐变"

---

## 🛠️ 其他可用技能

### **天气查询 (get_weather)**
- 功能：获取指定城市的实时天气信息
- 使用方法：调用 `fetch_url("https://wttr.in/{城市名}?format=j1&lang=zh")`

### **PDF处理 (pdf)**
- 功能：PDF文件的读取、合并、拆分、提取等操作
- 支持：文本提取、表格提取、OCR、水印添加等

---

## 📁 文件位置
- 技能文件位于：`src/agents/mini_openclaw_agent/skills/`
- 图像生成技能：`mcp-minimax/SKILL.md`
- 天气查询技能：`get_weather/SKILL.md`
- PDF处理技能：`pdf/SKILL.md`

---

*最后更新：2024年2月13日*
*记忆内容：图像生成能力及相关技能信息*
