---
name: send_email
description: 发送电子邮件到指定邮箱地址
license: Proprietary. LICENSE.txt has complete terms
---

# send_email

**描述**: 发送电子邮件到指定的邮箱地址

## 使用方法

当用户要求发送邮件时，按以下步骤操作：

### 步骤1：准备邮件内容

收集以下信息：
- 收件人邮箱地址
- 邮件主题
- 邮件正文内容
- 发件人信息（可选）

### 步骤2：配置SMTP服务器

根据邮箱类型配置SMTP服务器：

**常用邮箱SMTP配置**：

1. **Outlook/Hotmail**:
   - 服务器: smtp-mail.outlook.com
   - 端口: 587
   - 加密: TLS

2. **Gmail**:
   - 服务器: smtp.gmail.com
   - 端口: 587
   - 加密: TLS
   - 注意: 需要开启"应用专用密码"

3. **QQ邮箱**:
   - 服务器: smtp.qq.com
   - 端口: 587
   - 加密: TLS

4. **163邮箱**:
   - 服务器: smtp.163.com
   - 端口: 465
   - 加密: SSL

### 步骤3：使用Python发送邮件

使用 `python_repl` 执行发送代码：

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_email, subject, body, 
               smtp_server, smtp_port, 
               from_email, from_password,
               use_tls=True):
    """
    发送电子邮件
    
    参数:
    - to_email: 收件人邮箱
    - subject: 邮件主题
    - body: 邮件正文
    - smtp_server: SMTP服务器地址
    - smtp_port: SMTP服务器端口
    - from_email: 发件人邮箱
    - from_password: 发件人密码或应用专用密码
    - use_tls: 是否使用TLS加密
    """
    
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加正文
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 连接服务器并发送
        if use_tls:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # 启用TLS加密
        else:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # SSL加密
        
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        
        return True, "邮件发送成功！"
        
    except Exception as e:
        return False, f"邮件发送失败: {str(e)}"

# 示例使用
# result, message = send_email(
#     to_email="recipient@example.com",
#     subject="测试邮件",
#     body="这是一封测试邮件",
#     smtp_server="smtp-mail.outlook.com",
#     smtp_port=587,
#     from_email="your_email@outlook.com",
#     from_password="your_password",
#     use_tls=True
# )
```

### 步骤4：安全注意事项

1. **不要硬编码密码**: 建议从环境变量或配置文件中读取密码
2. **使用环境变量**:
   ```python
   import os
   email_password = os.getenv('EMAIL_PASSWORD')
   ```
3. **应用专用密码**: 对于Gmail等邮箱，建议使用应用专用密码而非账户密码

### 步骤5：发送结果反馈

告诉用户邮件是否发送成功，如果失败则提供错误信息。

## 示例对话

用户: 把天气报告发送到 example@outlook.com

你的行动:

1. 准备天气报告内容
2. 询问用户SMTP配置信息（或使用默认配置）
3. 使用python_repl执行发送代码
4. 告诉用户发送结果

## 备用方案

如果用户没有提供SMTP配置，可以：
1. 将邮件内容保存为文件供用户手动发送
2. 提供邮件内容让用户复制粘贴
3. 建议用户配置环境变量存储邮箱信息
