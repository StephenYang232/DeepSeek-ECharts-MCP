import json
from typing import Dict, Any, Optional, List
from config import settings


class EChartsUtils:
    """ECharts 工具类"""
    
    # 预定义的图表类型配置模板
    CHART_TEMPLATES = {
        "line": {
            "xAxis": {
                "type": "category",
                "data": []
            },
            "yAxis": {
                "type": "value"
            },
            "series": [{
                "data": [],
                "type": "line"
            }]
        },
        "bar": {
            "xAxis": {
                "type": "category",
                "data": []
            },
            "yAxis": {
                "type": "value"
            },
            "series": [{
                "data": [],
                "type": "bar"
            }]
        },
        "pie": {
            "series": [{
                "type": "pie",
                "data": []
            }]
        },
        "scatter": {
            "xAxis": {
                "type": "value"
            },
            "yAxis": {
                "type": "value"
            },
            "series": [{
                "data": [],
                "type": "scatter"
            }]
        }
    }
    
    # 预定义主题
    THEMES = {
        "light": {
            "color": ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc"],
            "backgroundColor": "#fff"
        },
        "dark": {
            "color": ["#5470c6", "#91cc75", "#fac858", "#ee6666", "#73c0de", "#3ba272", "#fc8452", "#9a60b4", "#ea7ccc"],
            "backgroundColor": "#1a1a1a"
        }
    }
    
    @classmethod
    def create_chart_config(cls, chart_type: str, data: Optional[Dict[str, Any]] = None, 
                          title: str = "", theme: str = "light") -> Dict[str, Any]:
        """
        创建图表配置
        
        Args:
            chart_type: 图表类型 (line, bar, pie, scatter)
            data: 数据集
            title: 图表标题
            theme: 主题 (light, dark)
            
        Returns:
            ECharts 配置对象
        """
        # 获取基础模板
        if chart_type not in cls.CHART_TEMPLATES:
            raise ValueError(f"不支持的图表类型: {chart_type}")
        
        config = cls.CHART_TEMPLATES[chart_type].copy()
        
        # 设置标题
        if title:
            config["title"] = {"text": title}
        
        # 应用主题
        if theme in cls.THEMES:
            config.update(cls.THEMES[theme])
        
        # 填充数据
        if data:
            config = cls._fill_data(config, chart_type, data)
        
        return config
    
    @classmethod
    def _fill_data(cls, config: Dict[str, Any], chart_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        填充数据到配置中
        
        Args:
            config: 基础配置
            chart_type: 图表类型
            data: 数据集
            
        Returns:
            填充数据后的配置
        """
        if chart_type == "pie":
            # 饼图数据格式: [{"value": 10, "name": "类别1"}]
            if "data" in data:
                config["series"][0]["data"] = data["data"]
        else:
            # 其他图表类型
            if "xAxis" in data:
                config["xAxis"]["data"] = data["xAxis"]
            if "series" in data:
                if isinstance(data["series"], list):
                    # 确保每个 series 对象都有 type 字段
                    for i, series_data in enumerate(data["series"]):
                        if i < len(config["series"]):
                            # 保留原有的 type 字段
                            series_data["type"] = config["series"][i]["type"]
                    config["series"] = data["series"]
                elif isinstance(data["series"], dict) and "data" in data["series"]:
                    config["series"][0]["data"] = data["series"]["data"]
        
        return config
    
    @classmethod
    def optimize_config(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        优化图表配置
        
        Args:
            config: 原始配置
            
        Returns:
            优化后的配置
        """
        # 添加响应式配置
        config.setdefault("responsive", True)
        config.setdefault("animation", True)
        
        # 优化 tooltip
        if "tooltip" not in config:
            config["tooltip"] = {
                "trigger": "axis" if "xAxis" in config else "item",
                "axisPointer": {
                    "type": "cross"
                }
            }
        
        # 优化 legend
        if "series" in config and len(config["series"]) > 1:
            if "legend" not in config:
                config["legend"] = {
                    "data": [series.get("name", f"系列{i+1}") for i, series in enumerate(config["series"])]
                }
        
        return config
    
    @classmethod
    def generate_html(cls, config: Dict[str, Any], height: str = "400px") -> str:
        """
        生成包含图表的 HTML
        
        Args:
            config: 图表配置
            height: 图表高度
            
        Returns:
            包含图表的 HTML 字符串
        """
        # 生成 HTML 字符串
        html_template = '''
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ECharts 图表</title>
            <script src="https://cdn.jsdelivr.net/npm/echarts@{echarts_version}/dist/echarts.min.js"></script>
        </head>
        <body>
            <div id="chart" style="width: 100%; height: {height}; "></div>
            <script>
                var chart = echarts.init(document.getElementById('chart'));
                var option = {config};
                chart.setOption(option);
                window.addEventListener('resize', function() {{
                    chart.resize();
                }});
            </script>
        </body>
        </html>
        '''
        
        # 使用字符串格式化替换变量
        config_str = json.dumps(config, ensure_ascii=False)
        html = html_template.format(
            echarts_version=settings.ECHARTS_VERSION,
            height=height,
            config=config_str
        )
        
        return html

    @classmethod
    def generate_and_open_chart(cls, config: Dict[str, Any], height: str = "400px") -> Dict[str, Any]:
        """
        生成图表并在浏览器中打开
        
        Args:
            config: 图表配置
            height: 图表高度
            
        Returns:
            操作结果
        """
        import tempfile
        import webbrowser
        import os
        
        try:
            # 生成 HTML
            html = cls.generate_html(config, height)
            
            # 创建临时 HTML 文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html)
                temp_file_path = f.name
            
            # 构建文件 URL
            file_url = f"file://{os.path.abspath(temp_file_path)}"
            
            # 打开默认浏览器
            webbrowser.open(file_url)
            
            return {
                "status": "success",
                "message": "图表已在浏览器中打开",
                "file_path": temp_file_path,
                "file_url": file_url
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"打开图表失败: {str(e)}"
            }
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> bool:
        """
        验证 ECharts 配置
        
        Args:
            config: 配置对象
            
        Returns:
            是否有效
        """
        try:
            # 基本验证
            if not isinstance(config, dict):
                return False
            
            # 验证 series
            if "series" in config:
                if not isinstance(config["series"], list):
                    return False
                for series in config["series"]:
                    if not isinstance(series, dict) or "type" not in series:
                        return False
            
            return True
        except Exception:
            return False
