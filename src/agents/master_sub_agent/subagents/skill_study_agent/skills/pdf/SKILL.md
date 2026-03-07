---
name: pdf
description: 当用户需要对 PDF 文件进行任何操作时使用此技能。包括从 PDF 提取文本/表格、合并多个 PDF、拆分 PDF、旋转页面、添加水印、创建新 PDF、填写 PDF 表单、加密/解密 PDF、提取图片等。
---

# PDF 处理指南

## 概述

本指南涵盖使用 Python 库进行基本 PDF 处理操作。

## 快速开始

```python
from pypdf import PdfReader, PdfWriter

# 读取 PDF
reader = PdfReader("document.pdf")
print(f"页数: {len(reader.pages)}")

# 提取文本
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## 常见操作

### 提取文本

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### 提取表格

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"第 {i+1} 页，表格 {j+1}:")
            for row in table:
                print(row)
```

### 合并 PDF

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### 拆分 PDF

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### 旋转页面

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # 顺时针旋转 90 度
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### 获取 PDF 元数据

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"标题: {meta.title if meta else 'N/A'}")
print(f"作者: {meta.author if meta else 'N/A'}")
print(f"页数: {len(reader.pages)}")
```

## 工作流程

当用户需要处理 PDF 时：

1. **理解需求**：明确用户要对 PDF 做什么操作
2. **选择合适的库**：
   - `pypdf`：基本操作（合并、拆分、旋转等）
   - `pdfplumber`：文本和表格提取
3. **使用 `python_repl` 工具**：执行 Python 代码完成任务
4. **返回结果**：向用户说明操作结果

## 示例对话

**用户**: 提取 document.pdf 的文本内容

**你的行动**:
```python
# 使用 python_repl 执行
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    print(text)
```

**用户**: 把 file1.pdf 和 file2.pdf 合并成一个

**你的行动**:
```python
# 使用 python_repl 执行
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["file1.pdf", "file2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
print("合并完成！输出文件: merged.pdf")
```

## 注意事项

- 确保文件路径正确
- 处理大文件时注意内存使用
- 某些 PDF 可能需要密码才能读取
- 扫描的 PDF 需要 OCR（光学字符识别）才能提取文本
