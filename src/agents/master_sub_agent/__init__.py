"""Master-Sub Agent - 主控+子智能体系统

基于 LangGraph 1.x 构建的主智能体+多子智能体协作系统。
"""

from .context import MasterSubContext
from .graph import MasterSubAgent

__all__ = [
    "MasterSubAgent",
    "MasterSubContext",
]

# 模块元数据
__version__ = "1.0.0"
__author__ = "Yuxi-Know Team"
__description__ = "基于 LangGraph 1.x 的主控+子智能体系统"
