from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """项目配置类"""
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # DeepSeek API 配置
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_API_URL: str = "https://api.deepseek.com/v1/chat/completions"
    DEEPSEEK_MODEL: str = "deepseek-chat"  # can be changed to deepseek-reasoner
    
    # ECharts 配置
    ECHARTS_VERSION: str = "5.4.3"
    
    # 数据处理配置
    MAX_DATA_SIZE: int = 10000
    
    class Config:
        # 从项目根目录读取 .env 文件
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        env_file_encoding = "utf-8"


# 创建全局配置实例
settings = Settings()
