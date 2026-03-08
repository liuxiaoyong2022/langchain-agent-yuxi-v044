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
from src.utils.logging_config import logger
from langchain_core.runnables import RunnableConfig
from server.utils.auth_middleware import get_db_session

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

@tool
async def list_conversation_attachments(config: RunnableConfig) -> str:
    """
    List all attachment files in the current conversation session.

    Use this to get information about files uploaded to the current conversation session.
    Returns a list of attachment files with their names, types, and status.

    Automatically retrieves the thread_id and user_id from the current conversation context.
    References the same logic as list_thread_attachments in chat_router.py.

    Returns:
        A formatted list of attachments with file information
    """
    # 从 RunnableConfig 中获取 thread_id 和 user_id
    configurable = config.get("configurable", {})
    thread_id = configurable.get("thread_id")
    user_id = configurable.get("user_id")

    if not thread_id:
        return "Error: No thread_id found in current conversation context."

    print(f"step 5.1.0--------------> list_conversation_attachments thread_id:{thread_id}, user_id:{user_id}")

    try:
        # from src.storage.postgres.manager import pg_manager
        from src.repositories.conversation_repository import ConversationRepository

    
        db = await get_db_session()
        logger.info(f"** step 5.1.1--------------> Database session acquired for listing attachments db:{db}")
        try:
            conv_repo = ConversationRepository(db)
            logger.info(f"step 5.1.2--------------> ConversationRepository initialized for listing attachments conv_repo:{conv_repo}")
            # 参考 chat_router.py 中 list_thread_attachments 的逻辑
            # 1. 通过 thread_id 获取会话
            conversation = await conv_repo.get_conversation_by_thread_id(thread_id)

            # 2. 验证会话存在且用户有权限（类似 _require_user_conversation）
            if not conversation:
                return f"Error: Conversation not found for thread_id: {thread_id}"
            if conversation.status == "deleted":
                return f"Error: Conversation has been deleted"
            if user_id and conversation.user_id != str(user_id):
                return f"Error: Access denied. You do not have permission to view attachments in this conversation."

            # 3. 获取附件列表（使用 conversation.id，参考 list_thread_attachments）
            attachments = await conv_repo.get_attachments(conversation.id)

            if not attachments:
                return "No attachments found in this conversation session."

            # Format the attachment list
            result = f"Found {len(attachments)} attachment(s):\n\n"
            for i, attachment in enumerate(attachments, 1):
                file_name = attachment.get("file_name", "Unknown")
                file_type = attachment.get("file_type", "Unknown")
                status = attachment.get("status", "Unknown")
                file_path = attachment.get("file_path", "N/A")
                uploaded_at = attachment.get("uploaded_at", "N/A")

                result += f"{i}. {file_name}\n"
                result += f"   Type: {file_type}\n"
                result += f"   Status: {status}\n"
                result += f"   Path: {file_path}\n"
                result += f"   Uploaded: {uploaded_at}\n\n"

            return result
        finally:
            await db.close()

    except Exception as e:
        print(f"step 5.error--------------> Error listing attachments: {e}")
        return f"Error listing attachments: {str(e)}"


@tool
async def fetch_attachment_file(file_name: str, config: RunnableConfig) -> str:
    """
    Fetch the original file from MinIO by filename.

    Use this to retrieve the original uploaded file content from storage.
    The file type is automatically determined from the filename extension.

    Args:
        file_name: The name of the file to fetch (e.g., 'document.pdf', 'report.docx')

    Returns:
        The file content or a download link/summary for binary files
    """
    logger.info(f"step 6.0--------------> fetch_attachment_file file_name:{file_name}")

    # 从 RunnableConfig 中获取 thread_id 和 user_id
    configurable = config.get("configurable", {})
    thread_id = configurable.get("thread_id")
    user_id = configurable.get("user_id")

    if not thread_id:
        return "Error: No thread_id found in current conversation context."

    logger.info(f"step 6.0.1--------------> thread_id:{thread_id}, user_id:{user_id}, file_name: {file_name}")

    # 标准化文件名（去除路径，只保留文件名）
    actual_file_name = file_name.split("/")[-1].split("\\")[-1].strip()

    # 根据文件名后缀推断 MIME 类型
    file_type = _get_mime_type(actual_file_name)
    logger.info(f"step 6.0.2--------------> actual_file_name: {actual_file_name}, file_type: {file_type}")

    try:
        from src.storage.postgres.manager import pg_manager
        from src.repositories.conversation_repository import ConversationRepository
        from src.storage.minio.client import get_minio_client

        # db = await pg_manager.get_async_session()
        try:
            # conv_repo = ConversationRepository(db)

            # # 参考 chat_router.py 中 list_thread_attachments 的逻辑
            # # 1. 通过 thread_id 获取会话
            # conversation = await conv_repo.get_conversation_by_thread_id(thread_id)

            # # 2. 验证会话存在且用户有权限
            # if not conversation:
            #     return f"Error: Conversation not found for thread_id: {thread_id}"
            # if conversation.status == "deleted":
            #     return f"Error: Conversation has been deleted"
            # if user_id and conversation.user_id != str(user_id):
            #     return f"Error: Access denied. You do not have permission to access attachments in this conversation."

            # # 3. 获取附件列表验证文件存在
            # attachments = await conv_repo.get_attachments(conversation.id)
            # attachment_file_names = [a.get("file_name", "") for a in attachments]

            # # 验证文件是否在附件列表中
            # if actual_file_name not in attachment_file_names:
            #     return f"Error: File '{actual_file_name}' not found in attachments. Available files:\n" + "\n".join(f"  - {f}" for f in attachment_file_names)

            # 构建 MinIO 访问路径
            # 格式: http://{minio_host}:9000/chat-attachments/attachments/{thread_id}/{文件名}
            minio_client = get_minio_client()
            minio_host = minio_client.public_endpoint  # 格式: "{host_ip}:9000"

            bucket_name = "chat-attachments"
            object_name = f"attachments/{thread_id}/{actual_file_name}"
            minio_url = f"http://{minio_host}/{bucket_name}/{object_name}"

            logger.info(f"step 6.1--------------> object_name: {object_name}, MinIO URL: {minio_url}")

            # 从 MinIO 下载文件
            file_data = await minio_client.adownload_file(bucket_name, object_name)
            logger.info(f"step 6.1.1--------------> file_data length: {len(file_data)}")

            # 根据文件类型处理返回内容
            if file_type.startswith("text/") or actual_file_name.endswith((".txt", ".md", ".html", ".htm", ".json", ".xml", ".pdf")):
                # 文本文件直接返回内容
                content = file_data.decode("utf-8", errors="replace")
                # 限制返回内容长度
                if len(content) > 50000:
                    content = content[:50000] + "\n\n...[Content truncated due to size]..."
                return f"File: {actual_file_name}\nSize: {len(file_data)} bytes\n\nContent:\n{content}"
            elif file_type.startswith("image/"):
                # 图片文件返回信息
                return f"Image file: {actual_file_name}\nSize: {len(file_data)} bytes\nFormat: {file_type}\n\nDownload URL: {minio_url}"
            else:
                # 二进制文件返回摘要信息
                return f"Binary file: {actual_file_name}\nSize: {len(file_data)} bytes\nType: {file_type}\n\nNote: This is a binary file. You can access it at: {minio_url}"
        finally:
            logger.info(f"step 6.2--------------> Finished processing fetch_attachment_file for {actual_file_name}")
            # await db.close()

    except Exception as e:
        logger.error(f"step 6.error--------------> Error fetching attachment file: {e}")
        import traceback
        traceback.print_exc()
        return f"Error fetching attachment file: {str(e)}"


def _get_mime_type(file_name: str) -> str:
    """
    根据文件名后缀推断 MIME 类型

    Args:
        file_name: 文件名

    Returns:
        MIME 类型字符串
    """
    # 转换为小写以进行匹配
    name_lower = file_name.lower()

    # 文本类型
    if name_lower.endswith(".txt"):
        return "text/plain"
    elif name_lower.endswith(".md"):
        return "text/markdown"
    elif name_lower.endswith((".html", ".htm")):
        return "text/html"
    elif name_lower.endswith(".json"):
        return ".json"
    elif name_lower.endswith(".xml"):
        return ".xml"

    # PDF 类型
    elif name_lower.endswith(".pdf"):
        return ".pdf"

    # Word 文档
    elif name_lower.endswith(".docx"):
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif name_lower.endswith(".doc"):
        return "application/msword"

    # 图片类型
    elif name_lower.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    elif name_lower.endswith(".png"):
        return "image/png"
    elif name_lower.endswith(".gif"):
        return "image/gif"
    elif name_lower.endswith((".bmp", ".webp")):
        return "image/bmp"

    # 其他类型默认返回二进制
    else:
        return "application/octet-stream"

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

    # 5. List Attachments - 列出当前会话的附件
    tools.append(list_conversation_attachments)

    # 6. Fetch Attachment - 获取附件文件内容
    tools.append(fetch_attachment_file)

    return tools
