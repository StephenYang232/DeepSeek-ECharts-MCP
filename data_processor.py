import json
import pandas as pd
from typing import Dict, Any, Optional, List
from config import settings


class DataProcessor:
    """数据处理模块"""
    
    @classmethod
    def process_data(cls, data: Any, data_type: Optional[str] = None) -> Dict[str, Any]:
        """
        处理数据
        
        Args:
            data: 原始数据
            data_type: 数据类型 (json, csv, excel, dict)
            
        Returns:
            处理后的数据
        """
        if data_type is None:
            # 自动检测数据类型
            data_type = cls._detect_data_type(data)
        
        if data_type == "json":
            return cls._process_json(data)
        elif data_type == "csv":
            return cls._process_csv(data)
        elif data_type == "excel":
            return cls._process_excel(data)
        elif data_type == "dict":
            return cls._process_dict(data)
        else:
            raise ValueError(f"不支持的数据类型: {data_type}")
    
    @classmethod
    def _detect_data_type(cls, data: Any) -> str:
        """
        自动检测数据类型
        
        Args:
            data: 原始数据
            
        Returns:
            数据类型
        """
        if isinstance(data, dict):
            return "dict"
        elif isinstance(data, str):
            # 尝试解析为 JSON
            try:
                json.loads(data)
                return "json"
            except json.JSONDecodeError:
                # 检查是否为 CSV 格式
                if data.strip().startswith("{"):
                    return "json"
                return "csv"
        return "dict"
    
    @classmethod
    def _process_json(cls, data: Any) -> Dict[str, Any]:
        """
        处理 JSON 数据
        
        Args:
            data: JSON 字符串或对象
            
        Returns:
            处理后的数据
        """
        if isinstance(data, str):
            data = json.loads(data)
        return data
    
    @classmethod
    def _process_csv(cls, data: str) -> Dict[str, Any]:
        """
        处理 CSV 数据
        
        Args:
            data: CSV 字符串
            
        Returns:
            处理后的数据，格式为 {"xAxis": [...], "series": [{"data": [...]}]}
        """
        import io
        
        # 读取 CSV 数据
        df = pd.read_csv(io.StringIO(data))
        
        # 限制数据大小
        if len(df) > settings.MAX_DATA_SIZE:
            df = df.head(settings.MAX_DATA_SIZE)
        
        # 转换为 ECharts 数据格式
        result = {
            "xAxis": [],
            "series": []
        }
        
        # 使用第一列为 xAxis
        if not df.empty:
            x_col = df.columns[0]
            result["xAxis"] = df[x_col].astype(str).tolist()
            
            # 其他列作为 series
            for col in df.columns[1:]:
                series = {
                    "name": col,
                    "data": df[col].tolist(),
                    "type": "line"
                }
                result["series"].append(series)
        
        return result
    
    @classmethod
    def _process_excel(cls, data: Any) -> Dict[str, Any]:
        """
        处理 Excel 数据
        
        Args:
            data: Excel 文件路径或字节流
            
        Returns:
            处理后的数据
        """
        # 读取 Excel 数据
        df = pd.read_excel(data)
        
        # 限制数据大小
        if len(df) > settings.MAX_DATA_SIZE:
            df = df.head(settings.MAX_DATA_SIZE)
        
        # 转换为 ECharts 数据格式
        result = {
            "xAxis": [],
            "series": []
        }
        
        # 使用第一列为 xAxis
        if not df.empty:
            x_col = df.columns[0]
            result["xAxis"] = df[x_col].astype(str).tolist()
            
            # 其他列作为 series
            for col in df.columns[1:]:
                series = {
                    "name": col,
                    "data": df[col].tolist(),
                    "type": "line"
                }
                result["series"].append(series)
        
        return result
    
    @classmethod
    def _process_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理字典数据
        
        Args:
            data: 字典数据
            
        Returns:
            处理后的数据
        """
        # 简单验证和清理
        if "data" in data and isinstance(data["data"], list):
            # 限制数据大小
            if len(data["data"]) > settings.MAX_DATA_SIZE:
                data["data"] = data["data"][:settings.MAX_DATA_SIZE]
        
        return data
    
    @classmethod
    def aggregate_data(cls, data: Dict[str, Any], aggregation: str = "sum") -> Dict[str, Any]:
        """
        聚合数据
        
        Args:
            data: 原始数据
            aggregation: 聚合方式 (sum, avg, max, min)
            
        Returns:
            聚合后的数据
        """
        if "series" not in data:
            return data
        
        # 对每个 series 进行聚合
        aggregated_series = []
        for series in data["series"]:
            if "data" in series and isinstance(series["data"], list):
                aggregated_data = cls._aggregate_list(series["data"], aggregation)
                aggregated_series.append({
                    "name": series["name"],
                    "data": aggregated_data,
                    "type": series["type"]
                })
        
        data["series"] = aggregated_series
        return data
    
    @classmethod
    def _aggregate_list(cls, data: List[Any], aggregation: str) -> float:
        """
        聚合列表数据
        
        Args:
            data: 数据列表
            aggregation: 聚合方式
            
        Returns:
            聚合结果
        """
        # 过滤非数值数据
        numeric_data = [x for x in data if isinstance(x, (int, float))]
        
        if not numeric_data:
            return 0
        
        if aggregation == "sum":
            return sum(numeric_data)
        elif aggregation == "avg":
            return sum(numeric_data) / len(numeric_data)
        elif aggregation == "max":
            return max(numeric_data)
        elif aggregation == "min":
            return min(numeric_data)
        else:
            return sum(numeric_data)
    
    @classmethod
    def format_for_echarts(cls, data: Dict[str, Any], chart_type: str) -> Dict[str, Any]:
        """
        格式化数据为 ECharts 所需格式
        
        Args:
            data: 原始数据
            chart_type: 图表类型
            
        Returns:
            格式化后的数据
        """
        if chart_type == "pie":
            # 转换为饼图数据格式
            return cls._format_for_pie(data)
        else:
            # 其他图表类型
            return data
    
    @classmethod
    def _format_for_pie(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化为饼图数据格式
        
        Args:
            data: 原始数据
            
        Returns:
            饼图数据格式
        """
        pie_data = []
        
        if "series" in data:
            for series in data["series"]:
                if "data" in series and "name" in series:
                    for i, value in enumerate(series["data"]):
                        if "xAxis" in data and i < len(data["xAxis"]):
                            name = data["xAxis"][i]
                        else:
                            name = f"{series['name']}_{i}"
                        pie_data.append({
                            "name": name,
                            "value": value
                        })
        elif "data" in data:
            # 直接处理 data 字段
            if isinstance(data["data"], list):
                for item in data["data"]:
                    if isinstance(item, dict) and "name" in item and "value" in item:
                        pie_data.append(item)
        
        return {"data": pie_data}
