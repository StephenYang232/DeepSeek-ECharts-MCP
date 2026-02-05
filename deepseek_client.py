import requests
import json
from typing import List, Dict, Optional, Any
from config import settings


class DeepSeekClient:
    """DeepSeek 大模型客户端"""
    
    def __init__(self):
        """初始化客户端"""
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.model = settings.DEEPSEEK_MODEL
        
    def generate_response(self, messages: List[Dict[str, str]], 
                         temperature: float = 0.7, 
                         max_tokens: int = 1024, 
                         stream: bool = False) -> Dict[str, Any]:
        """
        生成模型响应
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            temperature: 温度参数，控制输出随机性
            max_tokens: 最大令牌数
            stream: 是否流式响应
            
        Returns:
            模型响应结果
        """
        if not self.api_key:
            raise ValueError("DeepSeek API Key 未配置")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                stream=stream,
                timeout=30
            )
            
            response.raise_for_status()
            
            if stream:
                # 处理流式响应
                return self._handle_stream_response(response)
            else:
                # 处理普通响应
                return response.json()
                
        except requests.RequestException as e:
            raise Exception(f"DeepSeek API 调用失败: {str(e)}")
    
    def _handle_stream_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        处理流式响应
        
        Args:
            response: 流式响应对象
            
        Returns:
            聚合后的响应结果
        """
        full_response = {
            "id": None,
            "object": "chat.completion",
            "created": None,
            "model": self.model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": ""},
                "finish_reason": None
            }]
        }
        
        for chunk in response.iter_lines():
            if chunk:
                chunk = chunk.decode('utf-8')
                if chunk.startswith('data: '):
                    chunk = chunk[6:]
                    if chunk == '[DONE]':
                        break
                    try:
                        chunk_data = json.loads(chunk)
                        if 'id' in chunk_data and not full_response['id']:
                            full_response['id'] = chunk_data['id']
                        if 'created' in chunk_data and not full_response['created']:
                            full_response['created'] = chunk_data['created']
                        if 'choices' in chunk_data:
                            for choice in chunk_data['choices']:
                                if 'delta' in choice and 'content' in choice['delta']:
                                    full_response['choices'][0]['message']['content'] += choice['delta']['content']
                                if 'finish_reason' in choice:
                                    full_response['choices'][0]['finish_reason'] = choice['finish_reason']
                    except json.JSONDecodeError:
                        pass
        
        return full_response
    
    def generate_echarts_config(self, user_prompt: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        生成 ECharts 配置
        
        Args:
            user_prompt: 用户提示
            data: 可选的数据集
            
        Returns:
            ECharts 配置对象
        """
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的数据可视化专家，擅长使用 ECharts 创建各种图表。请根据用户的需求和提供的数据，生成完整、有效的 ECharts 配置对象。只返回配置对象，不要包含其他解释性文本。"
            },
            {
                "role": "user",
                "content": f"用户需求: {user_prompt}\n\n数据: {json.dumps(data, ensure_ascii=False) if data else '无'}\n\n请生成 ECharts 配置对象:"
            }
        ]
        
        response = self.generate_response(messages, temperature=0.3, max_tokens=2048)
        
        # 提取配置内容
        content = response['choices'][0]['message']['content']
        
        # 尝试解析 JSON
        try:
            # 清理内容，移除可能的代码块标记
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            
            config = json.loads(content)
            return config
        except json.JSONDecodeError as e:
            raise Exception(f"ECharts 配置生成失败: {str(e)}")
