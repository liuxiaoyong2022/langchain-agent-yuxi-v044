"""Skill Study Agent 核心工具实现

提供基础工具：Python REPL, Fetch URL, Read File
"""

from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup
import html2text
import subprocess
from langchain_core.tools import tool
from langchain_experimental.tools import PythonREPLTool
from pydantic import BaseModel, Field
from typing import Type
from langchain_core.tools import BaseTool


class CustomPythonREPLTool(PythonREPLTool):
    """Custom Python REPL tool"""
    name: str = "python_repl"
    description: str = """
    Execute Python code in a REPL environment.
    Use this for calculations, data processing, and script execution.
    Input should be valid Python code.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


_repl_instance = CustomPythonREPLTool()


@tool
def fetch_url(url: str) -> str:
    """
    Fetch content from a URL and return it as clean Markdown text.
    Use this to retrieve information from websites, APIs, or online resources.
    The HTML is automatically cleaned and converted to readable format.

    Args:
        url: The URL to fetch

    Returns:
        Cleaned Markdown content
    """
    print(f"step skill.1.0 -> Fetching {url}")
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; SkillStudyAgent/1.0)'}
        )
        response.raise_for_status()

        # 清洗HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()

        # 转换为Markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        markdown_content = h.handle(str(soup))

        # 限制长度（防止Token爆炸）
        if len(markdown_content) > 20000:
            markdown_content = markdown_content[:20000] + "\n\n...[truncated]"

        print(f"step skill.1.1 -> Fetched {len(markdown_content)} chars")
        return markdown_content

    except Exception as e:
        return f"Error fetching URL: {str(e)}"


@tool
def python_repl(code: str, timeout: Optional[int] = None) -> str:
    """
    Execute Python code in an isolated REPL environment.

    Use this for calculations, data processing, or running Python scripts.
    The environment persists across calls in the same session.

    Args:
        code: Python code to execute
        timeout: Optional execution timeout in seconds (default: 30)

    Returns:
        Output from execution or error messages
    """
    print(f"step skill.2.0 -> Executing Python code")
    return _repl_instance.run(code)


@tool
def read_file(project_root: str, file_path: str) -> str:
    """
    Read the content of a file from the local filesystem.

    **CRITICAL for Skills**: Always use this to read SKILL.md before executing any skill.
    Path should be relative to project root (e.g., 'src/agents/master_sub_agent/subagents/skill_study_agent/skills/get_weather/SKILL.md').

    Args:
        project_root: Project root path
        file_path: Relative path from project root

    Returns:
        The content of the file or error message
    """
    print(f"step skill.3.0 -> Reading file: {file_path}")

    # 构建完整路径并解析为绝对路径
    full_path = Path(project_root + "/" + file_path).resolve()

    # 检查文件是否存在
    if not full_path.exists():
        return f"Error: File not found at {file_path}"

    # 检查是否为文件
    if not full_path.is_file():
        return f"Error: Path is not a file: {file_path}"

    # 读取文件内容
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content:
            return f"File is empty: {file_path}"

        print(f"step skill.3.1 -> Read {len(content)} chars")
        return content

    except PermissionError:
        return f"Error: Permission denied reading file: {file_path}"
    except UnicodeDecodeError:
        return f"Error: Cannot decode file {file_path} (may be binary file)"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for relevant information.

    Use this when the user asks about specific knowledge or documentation.

    Args:
        query: Search query for the knowledge base

    Returns:
        Relevant documents or error message
    """
    print(f"step skill.4.0 -> Searching knowledge base: {query}")

    try:
        from src import knowledge_base
        import inspect

        # Get available knowledge bases
        retrievers = knowledge_base.get_retrievers()

        if not retrievers:
            return "No knowledge bases available. Please create a knowledge base first."

        # Use the first available knowledge base
        target_db_id = next(iter(retrievers))
        retriever_info = retrievers[target_db_id]
        retriever = retriever_info["retriever"]

        # Query the knowledge base
        if inspect.iscoroutinefunction(retriever):
            import asyncio
            result = asyncio.run(retriever(query))
        else:
            result = retriever(query)

        # Format the result
        if isinstance(result, list) and result:
            formatted_result = f"Knowledge Base: {retriever_info['name']}\n"
            formatted_result += f"Query: {query}\n\n"
            formatted_result += f"Found {len(result)} relevant documents:\n\n"
            for i, item in enumerate(result[:10], 1):
                if isinstance(item, dict):
                    content = item.get("content", "")
                    source = item.get("metadata", {}).get("file_name", "Unknown")
                    formatted_result += f"{i}. [{source}]\n{content[:500]}...\n\n"
                else:
                    formatted_result += f"{i}. {str(item)[:500]}...\n\n"
            return formatted_result
        elif isinstance(result, str):
            return result
        else:
            return f"Query completed. Result type: {type(result).__name__}"

    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"


def initialize_core_tools(project_root: Path) -> list:
    """
    初始化所有核心工具

    Args:
        project_root: 项目根目录路径

    Returns:
        工具列表
    """
    tools = []

    # 1. Python REPL - Python代码解释器
    tools.append(python_repl)

    # 2. Fetch URL - 网络信息获取
    tools.append(fetch_url)

    # 3. Read File - 文件读取工具
    tools.append(read_file)

    # 4. RAG Search - 知识库检索
    tools.append(search_knowledge_base)

    return tools
