# DeepSeek-ECharts MCP 使用文档

## 项目介绍

DeepSeek-ECharts MCP（Model Context Protocol）是一个将 DeepSeek 大模型与 ECharts 数据可视化库集成的协议，支持在多种 IDE 和 VS Code 中使用。

### 核心功能

- **智能图表配置生成**：使用 DeepSeek 大模型根据用户需求生成 ECharts 配置
- **多种图表类型支持**：支持折线图、柱状图、饼图、散点图等多种图表类型
- **数据处理**：支持处理 JSON、CSV 等多种格式的数据
- **图表优化**：自动优化图表配置，提高可视化效果
- **HTML 生成**：生成包含图表的完整 HTML 文件
- **IDE 集成**：提供 VS Code 扩展，方便在 IDE 中使用

## 安装步骤

### 1. 克隆仓库

```bash
# 克隆 DeepSeek-ECharts MCP 仓库
git clone <repository_url>
cd <repository_directory>
```

### 2. 安装依赖

```bash
# 进入 server 目录
cd server

# 安装 Python 依赖
pip install -r requirements.txt
```

### 3. 配置 API 密钥

在 `server` 目录下创建 `.env` 文件，并添加 DeepSeek API 密钥：

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
DEEPSEEK_MODEL=deepseek-chat
```

### 4. 启动服务器

```bash
# 在 server 目录下执行
python server.py
```

服务器默认运行在 `http://0.0.0.0:8000`。

## API 端点说明

### 1. 健康检查端点

**URL**: `/health`
**方法**: GET
**功能**: 检查服务器运行状态

**响应示例**:
```json
{
  "status": "healthy",
  "message": "DeepSeek-ECharts MCP Server 运行正常"
}
```

### 2. 工具列表端点

**URL**: `/tools`
**方法**: GET
**功能**: 列出所有可用工具

**响应示例**:
```json
{
  "tools": {
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
    }
  }
}
```

### 3. 工具调用端点

**URL**: `/call`
**方法**: POST
**功能**: 调用指定工具执行操作

**请求示例**:
```json
{
  "tools": [
    {
      "name": "generate_echarts_config",
      "parameters": {
        "prompt": "生成一个展示2024年1-6月月度销售额的折线图，使用蓝色主题，添加网格线和数据标签"
      }
    }
  ]
}
```

**响应示例**:
```json
{
  "tool_responses": [
    {
      "tool_call_id": "tool_0",
      "result": {
        "config": {
          "title": {
            "text": "2024年1-6月月度销售额",
            "left": "center",
            "textStyle": {
              "color": "#333",
              "fontSize": 18
            }
          },
          "tooltip": {
            "trigger": "axis",
            "axisPointer": {
              "type": "shadow"
            }
          },
          "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": true
          },
          "xAxis": {
            "type": "category",
            "data": ["1月", "2月", "3月", "4月", "5月", "6月"],
            "axisLine": {
              "lineStyle": {
                "color": "#5470c6"
              }
            },
            "axisLabel": {
              "color": "#333"
            }
          },
          "yAxis": {
            "type": "value",
            "name": "销售额（万元）",
            "axisLine": {
              "lineStyle": {
                "color": "#5470c6"
              }
            },
            "axisLabel": {
              "color": "#333",
              "formatter": "{value}"
            },
            "splitLine": {
              "lineStyle": {
                "color": "#e0e6f1",
                "type": "dashed"
              }
            }
          },
          "series": [
            {
              "name": "销售额",
              "type": "line",
              "data": [120, 200, 150, 80, 70, 110],
              "itemStyle": {
                "color": "#5470c6"
              },
              "lineStyle": {
                "color": "#5470c6",
                "width": 3
              },
              "symbol": "circle",
              "symbolSize": 8,
              "label": {
                "show": true,
                "position": "top",
                "color": "#5470c6",
                "fontWeight": "bold"
              },
              "areaStyle": {
                "color": {
                  "type": "linear",
                  "x": 0,
                  "y": 0,
                  "x2": 0,
                  "y2": 1,
                  "colorStops": [
                    {
                      "offset": 0,
                      "color": "rgba(84, 112, 198, 0.5)"
                    },
                    {
                      "offset": 1,
                      "color": "rgba(84, 112, 198, 0.1)"
                    }
                  ]
                }
              }
            }
          ],
          "color": ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc"]
        },
        "status": "success"
      }
    }
  ],
  "status": "completed"
}
```

## 工具使用指南

### 1. generate_echarts_config

**功能**: 使用 DeepSeek 大模型生成 ECharts 配置

**参数**:
- `prompt`: 用户提示，描述需要的图表
- `data`: 可选的数据集

**示例**:
```python
import requests
import json

url = "http://localhost:8000/call"
data = {
  "tools": [{
    "name": "generate_echarts_config",
    "parameters": {
      "prompt": "生成一个展示2024年1-6月月度销售额的折线图，使用蓝色主题，添加网格线和数据标签"
    }
  }]
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
```

### 2. create_chart

**功能**: 创建指定类型的图表

**参数**:
- `chart_type`: 图表类型 (line, bar, pie, scatter)
- `data`: 数据集
- `title`: 图表标题
- `theme`: 主题 (light, dark)

**示例**:
```python
import requests
import json

url = "http://localhost:8000/call"
data = {
  "tools": [{
    "name": "create_chart",
    "parameters": {
      "chart_type": "line",
      "data": {
        "xAxis": ["一月", "二月", "三月"],
        "series": [{
          "data": [100, 200, 150]
        }]
      },
      "title": "月度销售额折线图",
      "theme": "light"
    }
  }]
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
```

### 3. process_data

**功能**: 处理和转换数据

**参数**:
- `data`: 原始数据
- `data_type`: 数据类型 (json, csv, excel, dict)
- `chart_type`: 目标图表类型

**示例**:
```python
import requests
import json

url = "http://localhost:8000/call"
data = {
  "tools": [{
    "name": "process_data",
    "parameters": {
      "data": "month,sales\n1月,100\n2月,200\n3月,150",
      "data_type": "csv",
      "chart_type": "bar"
    }
  }]
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
```

### 4. optimize_chart

**功能**: 优化图表配置

**参数**:
- `config`: 原始图表配置

**示例**:
```python
import requests
import json

url = "http://localhost:8000/call"
data = {
  "tools": [{
    "name": "optimize_chart",
    "parameters": {
      "config": {
        "xAxis": {
          "type": "category",
          "data": ["一月", "二月", "三月"]
        },
        "yAxis": {
          "type": "value"
        },
        "series": [{
          "data": [100, 200, 150],
          "type": "line"
        }]
      }
    }
  }]
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
```

### 5. generate_html

**功能**: 生成包含图表的 HTML

**参数**:
- `config`: 图表配置
- `height`: 图表高度

**示例**:
```python
import requests
import json

url = "http://localhost:8000/call"
data = {
  "tools": [{
    "name": "generate_html",
    "parameters": {
      "config": {
        "title": {
          "text": "测试图表"
        },
        "xAxis": {
          "type": "category",
          "data": ["一月", "二月", "三月"]
        },
        "yAxis": {
          "type": "value"
        },
        "series": [{
          "data": [100, 200, 150],
          "type": "line"
        }]
      },
      "height": "400px"
    }
  }]
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
```

## IDE 集成

### VS Code 扩展

**安装步骤**:
1. 打开 VS Code
2. 点击左侧的扩展图标
3. 点击 "从 VSIX 安装..."
4. 选择 `extensions/vscode` 目录下的扩展文件
5. 安装完成后，重新加载 VS Code

**使用方法**:
1. 打开一个 Python 文件
2. 右键点击编辑器，选择 "DeepSeek-ECharts MCP"
3. 在弹出的对话框中输入图表描述
4. 等待生成图表配置
5. 查看生成的图表

### 其他 IDE 集成

MCP 设计为支持多种 IDE，除了 VS Code 扩展外，其他 IDE 可以通过 HTTP API 调用使用。

**使用方法**:
1. 启动 MCP 服务器
2. 在 IDE 中使用 HTTP 客户端或脚本调用 API 端点
3. 处理返回的图表配置或 HTML

## 示例代码

### 基本用法示例

```python
# examples/basic_usage.py
import requests
import json

# 服务器 URL
url = "http://localhost:8000/call"

# 示例 1: 生成图表配置
print("示例 1: 生成图表配置")
data1 = {
  "tools": [{
    "name": "generate_echarts_config",
    "parameters": {
      "prompt": "生成一个展示2024年1-6月月度销售额的折线图，使用蓝色主题，添加网格线和数据标签"
    }
  }]
}

response1 = requests.post(url, json=data1)
print(json.dumps(response1.json(), ensure_ascii=False, indent=2))
print("\n" + "="*60 + "\n")

# 示例 2: 创建柱状图
print("示例 2: 创建柱状图")
data2 = {
  "tools": [{
    "name": "create_chart",
    "parameters": {
      "chart_type": "bar",
      "data": {
        "xAxis": ["一月", "二月", "三月"],
        "series": [{
          "data": [100, 200, 150]
        }]
      },
      "title": "季度销售额柱状图",
      "theme": "light"
    }
  }]
}

response2 = requests.post(url, json=data2)
print(json.dumps(response2.json(), ensure_ascii=False, indent=2))
print("\n" + "="*60 + "\n")

# 示例 3: 生成 HTML
print("示例 3: 生成 HTML")
config = response2.json()["tool_responses"][0]["result"]["config"]
data3 = {
  "tools": [{
    "name": "generate_html",
    "parameters": {
      "config": config,
      "height": "400px"
    }
  }]
}

response3 = requests.post(url, json=data3)
print(json.dumps(response3.json(), ensure_ascii=False, indent=2))
```

## 故障排除

### 1. API 密钥配置错误

**症状**: 调用 `generate_echarts_config` 工具时返回 `DeepSeek API Key 未配置` 错误

**解决方案**:
- 确保在 `server` 目录下创建了 `.env` 文件
- 确保 `.env` 文件中包含正确的 `DEEPSEEK_API_KEY`
- 确保 API 密钥格式正确，没有多余的空格或换行

### 2. 服务器启动失败

**症状**: 运行 `python server.py` 时出现错误

**解决方案**:
- 检查 Python 版本是否兼容（推荐 Python 3.8+）
- 确保所有依赖都已安装：`pip install -r requirements.txt`
- 检查端口 8000 是否被占用

### 3. 工具调用失败

**症状**: 调用工具时返回错误信息

**解决方案**:
- 检查参数是否正确
- 检查数据格式是否符合要求
- 查看服务器日志，了解详细错误信息

### 4. 图表显示异常

**症状**: 生成的图表配置在 ECharts 中显示异常

**解决方案**:
- 检查图表配置是否完整
- 使用 `optimize_chart` 工具优化配置
- 检查数据格式是否正确

## 常见问题

### 1. MCP 支持哪些 IDE？

MCP 设计为支持多种 IDE，目前提供了 VS Code 扩展，其他 IDE 可以通过 HTTP API 调用使用。

### 2. 如何获取 DeepSeek API 密钥？

可以在 DeepSeek 官方网站注册并获取 API 密钥。

### 3. MCP 支持哪些图表类型？

MCP 支持 ECharts 的所有图表类型，包括折线图、柱状图、饼图、散点图、雷达图等。

### 4. 如何在生产环境中部署 MCP？

可以使用 Docker 容器化部署，或使用 Gunicorn 等 WSGI 服务器运行。

### 5. MCP 的性能如何？

MCP 的性能取决于网络速度和 DeepSeek API 的响应速度，对于复杂图表配置，可能需要几秒钟的时间。

## 结语

DeepSeek-ECharts MCP 是一个强大的工具，它将 DeepSeek 大模型的智能能力与 ECharts 的可视化能力结合起来，为用户提供了一种简单、高效的方式来创建和优化图表。通过本文档的指导，您应该能够轻松地安装、配置和使用 MCP，为您的数据分析和可视化工作提供有力支持。

如果您在使用过程中遇到任何问题，欢迎在 GitHub 仓库中提交 issue，我们会及时响应并提供帮助。