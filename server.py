from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from typing import Dict, Any, List, Optional

from config import settings
from deepseek_client import DeepSeekClient
from echarts_utils import EChartsUtils
from data_processor import DataProcessor

# 创建 FastAPI 应用
app = FastAPI(
    title="DeepSeek-ECharts MCP Server",
    description="DeepSeek 大模型与 ECharts 集成的 MCP Server",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化客户端和工具
deepseek_client = DeepSeekClient()

# 请求和响应模型
class ToolCall(BaseModel):
    name: str
    parameters: Dict[str, Any]

class ToolResponse(BaseModel):
    tool_call_id: str
    result: Dict[str, Any]

class MCPRequest(BaseModel):
    tools: List[ToolCall]
    context: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    tool_responses: List[ToolResponse]
    status: str

# 工具注册
TOOLS = {
    "generate_echarts_config": {
        "description": "使用 DeepSeek 生成 ECharts 配置",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "用户提示，描述需要的图表"
                },
                "data": {
                    "type": "object",
                    "description": "可选的数据集"
                }
            },
            "required": ["prompt"]
        }
    },
    "create_chart": {
        "description": "创建指定类型的图表",
        "parameters": {
            "type": "object",
            "properties": {
                "chart_type": {
                    "type": "string",
                    "description": "图表类型: line, bar, pie, scatter"
                },
                "data": {
                    "type": "object",
                    "description": "数据集"
                },
                "title": {
                    "type": "string",
                    "description": "图表标题"
                },
                "theme": {
                    "type": "string",
                    "description": "主题: light, dark"
                }
            },
            "required": ["chart_type"]
        }
    },
    "process_data": {
        "description": "处理和转换数据",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "description": "原始数据"
                },
                "data_type": {
                    "type": "string",
                    "description": "数据类型: json, csv, excel, dict"
                },
                "chart_type": {
                    "type": "string",
                    "description": "目标图表类型"
                }
            },
            "required": ["data"]
        }
    },
    "optimize_chart": {
        "description": "优化图表配置",
        "parameters": {
            "type": "object",
            "properties": {
                "config": {
                    "type": "object",
                    "description": "原始图表配置"
                }
            },
            "required": ["config"]
        }
    },
    "generate_html": {
        "description": "生成包含图表的 HTML",
        "parameters": {
            "type": "object",
            "properties": {
                "config": {
                    "type": "object",
                    "description": "图表配置"
                },
                "height": {
                    "type": "string",
                    "description": "图表高度"
                }
            },
            "required": ["config"]
        }
    },
    "create_and_open_chart": {
        "description": "创建图表并在浏览器中打开",
        "parameters": {
            "type": "object",
            "properties": {
                "chart_type": {
                    "type": "string",
                    "description": "图表类型: line, bar, pie, scatter"
                },
                "data": {
                    "type": "object",
                    "description": "数据集"
                },
                "title": {
                    "type": "string",
                    "description": "图表标题"
                },
                "theme": {
                    "type": "string",
                    "description": "主题: light, dark"
                },
                "height": {
                    "type": "string",
                    "description": "图表高度"
                }
            },
            "required": ["chart_type"]
        }
    },
    "open_chart": {
        "description": "在浏览器中打开现有图表配置",
        "parameters": {
            "type": "object",
            "properties": {
                "config": {
                    "type": "object",
                    "description": "图表配置"
                },
                "height": {
                    "type": "string",
                    "description": "图表高度"
                }
            },
            "required": ["config"]
        }
    }
}

# 工具实现函数
def generate_echarts_config(prompt: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """使用 DeepSeek 生成 ECharts 配置"""
    try:
        config = deepseek_client.generate_echarts_config(prompt, data)
        return {"config": config, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

def create_chart(chart_type: str, data: Optional[Dict[str, Any]] = None, 
                 title: str = "", theme: str = "light") -> Dict[str, Any]:
    """创建指定类型的图表"""
    try:
        config = EChartsUtils.create_chart_config(chart_type, data, title, theme)
        return {"config": config, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

def process_data(data: Dict[str, Any], data_type: Optional[str] = None, 
                 chart_type: Optional[str] = None) -> Dict[str, Any]:
    """处理和转换数据"""
    try:
        processed_data = DataProcessor.process_data(data, data_type)
        if chart_type:
            processed_data = DataProcessor.format_for_echarts(processed_data, chart_type)
        return {"data": processed_data, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

def optimize_chart(config: Dict[str, Any]) -> Dict[str, Any]:
    """优化图表配置"""
    try:
        optimized_config = EChartsUtils.optimize_config(config)
        return {"config": optimized_config, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

def generate_html(config: Dict[str, Any], height: str = "400px") -> Dict[str, Any]:
    """生成包含图表的 HTML"""
    try:
        html = EChartsUtils.generate_html(config, height)
        return {"html": html, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

def create_and_open_chart(chart_type: str, data: Optional[Dict[str, Any]] = None, 
                         title: str = "", theme: str = "light", height: str = "400px") -> Dict[str, Any]:
    """创建图表并在浏览器中打开"""
    try:
        # 先创建图表配置
        config = EChartsUtils.create_chart_config(chart_type, data, title, theme)
        # 然后打开图表
        result = EChartsUtils.generate_and_open_chart(config, height)
        return result
    except Exception as e:
        return {"error": str(e), "status": "error"}

def open_chart(config: Dict[str, Any], height: str = "400px") -> Dict[str, Any]:
    """在浏览器中打开现有图表配置"""
    try:
        result = EChartsUtils.generate_and_open_chart(config, height)
        return result
    except Exception as e:
        return {"error": str(e), "status": "error"}

# API 路由
@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "DeepSeek-ECharts MCP Server 运行正常"}

@app.get("/tools")
def list_tools():
    """列出可用工具"""
    return {"tools": TOOLS}

@app.post("/call")
def call_tool(request: MCPRequest):
    """调用工具"""
    tool_responses = []
    
    for i, tool_call in enumerate(request.tools):
        tool_name = tool_call.name
        parameters = tool_call.parameters
        
        # 调用相应的工具函数
        if tool_name == "generate_echarts_config":
            result = generate_echarts_config(
                prompt=parameters.get("prompt"),
                data=parameters.get("data")
            )
        elif tool_name == "create_chart":
            result = create_chart(
                chart_type=parameters.get("chart_type"),
                data=parameters.get("data"),
                title=parameters.get("title", ""),
                theme=parameters.get("theme", "light")
            )
        elif tool_name == "process_data":
            result = process_data(
                data=parameters.get("data"),
                data_type=parameters.get("data_type"),
                chart_type=parameters.get("chart_type")
            )
        elif tool_name == "optimize_chart":
            result = optimize_chart(
                config=parameters.get("config")
            )
        elif tool_name == "generate_html":
            result = generate_html(
                config=parameters.get("config"),
                height=parameters.get("height", "400px")
            )
        elif tool_name == "create_and_open_chart":
            result = create_and_open_chart(
                chart_type=parameters.get("chart_type"),
                data=parameters.get("data"),
                title=parameters.get("title", ""),
                theme=parameters.get("theme", "light"),
                height=parameters.get("height", "400px")
            )
        elif tool_name == "open_chart":
            result = open_chart(
                config=parameters.get("config"),
                height=parameters.get("height", "400px")
            )
        else:
            result = {"error": f"未知工具: {tool_name}", "status": "error"}
        
        # 添加到响应
        tool_responses.append(ToolResponse(
            tool_call_id=f"tool_{i}",
            result=result
        ))
    
    return MCPResponse(
        tool_responses=tool_responses,
        status="completed"
    )

# 根路径
@app.get("/")
def root():
    """根路径"""
    return {
        "message": "DeepSeek-ECharts MCP Server",
        "version": "1.0.0",
        "endpoints": {
            "/health": "健康检查",
            "/tools": "列出可用工具",
            "/call": "调用工具"
        }
    }

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
