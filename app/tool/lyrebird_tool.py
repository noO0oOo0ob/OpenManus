import json
import requests
from typing import Dict, List, Optional, Any, Union

from pydantic import Field

from app.tool.base import BaseTool, ToolResult


class LyrebirdTool(BaseTool):
    """Tool for interacting with Lyrebird proxy."""

    name: str = "lyrebird_tool"
    description: str = "获取Lyrebird代理记录并将特定记录保存为Mock数据"
    parameters: Dict = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["get_flows", "get_flow", "get_groups", "create_group", "create_mock", "update_mock"],
                "description": "要执行的操作",
            },
            "flow_id": {
                "type": "string",
                "description": "请求记录ID，用于获取特定请求记录或创建Mock数据",
            },
            "parent_id": {
                "type": "string",
                "description": "父目录ID，用于创建目录或Mock数据",
            },
            "name": {
                "type": "string",
                "description": "目录或Mock数据的名称",
            },
            "mock_data": {
                "type": "object",
                "description": "Mock数据内容，用于更新Mock数据",
            },
        },
        "required": ["action"],
    }
    base_url: str = "http://localhost:9090"

    async def execute(
        self,
        action: str,
        flow_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        name: Optional[str] = None,
        mock_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> ToolResult:
        """执行Lyrebird相关操作"""
        try:
            if action == "get_flows":
                return await self._get_flows()
            elif action == "get_flow":
                if not flow_id:
                    return ToolResult(error="获取特定请求记录需要提供flow_id")
                return await self._get_flow(flow_id)
            elif action == "get_groups":
                return await self._get_groups()
            elif action == "create_group":
                if not parent_id or not name:
                    return ToolResult(error="创建目录需要提供parent_id和name")
                return await self._create_group(parent_id, name)
            elif action == "create_mock":
                if not parent_id or not flow_id:
                    return ToolResult(error="创建Mock数据需要提供parent_id和flow_id")
                return await self._create_mock_from_flow(parent_id, flow_id, name)
            elif action == "update_mock":
                if not mock_data:
                    return ToolResult(error="更新Mock数据需要提供mock_data")
                return await self._update_mock(mock_data)
            else:
                return ToolResult(error=f"不支持的操作: {action}")
        except Exception as e:
            return ToolResult(error=f"执行Lyrebird操作时出错: {str(e)}")

    async def _get_flows(self) -> ToolResult:
        """获取所有请求记录"""
        url = f"{self.base_url}/api/flow"
        response = requests.get(url)
        if response.status_code == 200:
            # 将JSON响应转换为字符串，以确保ToolResult.output是字符串类型
            return ToolResult(output=json.dumps(response.json()))
        return ToolResult(error=f"获取请求记录失败: {response.status_code}")

    async def _get_flow(self, flow_id: str) -> ToolResult:
        """获取特定请求记录"""
        url = f"{self.base_url}/api/flow/{flow_id}"
        response = requests.get(url)
        if response.status_code == 200:
            # 将JSON响应转换为字符串
            return ToolResult(output=json.dumps(response.json()))
        return ToolResult(error=f"获取特定请求记录失败: {response.status_code}")

    async def _get_groups(self) -> ToolResult:
        """获取Mock数据的目录结构"""
        url = f"{self.base_url}/api/group"
        response = requests.get(url)
        if response.status_code == 200:
            # 将JSON响应转换为字符串
            return ToolResult(output=json.dumps(response.json()))
        return ToolResult(error=f"获取目录结构失败: {response.status_code}")

    async def _create_group(self, parent_id: str, name: str) -> ToolResult:
        """创建Mock数据目录"""
        url = f"{self.base_url}/api/group"
        data = {
            "name": name,
            "parent_id": parent_id
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            # 将JSON响应转换为字符串
            return ToolResult(output=json.dumps(response.json()))
        return ToolResult(error=f"创建目录失败: {response.status_code}")

    async def _create_mock_from_flow(
        self, parent_id: str, flow_id: str, name: Optional[str] = None
    ) -> ToolResult:
        """从请求记录创建Mock数据"""
        # 首先获取流量详情
        flow_result = await self._get_flow(flow_id)
        if flow_result.error:
            return flow_result
        
        # 由于我们现在返回的是JSON字符串，需要解析回Python对象
        flow_data = json.loads(flow_result.output).get("data", {})
        if not flow_data:
            return ToolResult(error="获取流量详情失败")
        
        # 创建Mock数据
        url = f"{self.base_url}/api/data"
        mock_name = name or flow_data.get("request", {}).get("path", "unknown_path")
        data = {
            "data": {
                "type": "data",
                "name": mock_name
            },
            "parent_id": parent_id
        }
        
        response = requests.post(url, json=data)
        if response.status_code != 200:
            return ToolResult(error=f"创建Mock数据失败: {response.status_code}")
        
        # 获取创建的Mock数据ID
        mock_response = response.json()
        mock_id = mock_response.get("data_id")
        if not mock_id:
            return ToolResult(error="获取Mock数据ID失败")
        
        # 更新Mock数据内容
        request_data = flow_data.get("request", {})
        response_data = flow_data.get("response", {})
        
        # 构建规则，默认匹配URL
        url_path = request_data.get("path", "")
        rule = {
            "request.url": f"(?=.*{url_path}$)"
        }
        
        # 构建Mock数据
        mock_data = {
            "id": mock_id,
            "name": mock_name,
            "rule": rule,
            "request": {
                "url": request_data.get("url", ""),
                "headers": request_data.get("headers", {}),
                "method": request_data.get("method", "GET"),
                "data": json.dumps(request_data.get("data", {}))
            },
            "response": {
                "code": response_data.get("code", 200),
                "headers": response_data.get("headers", {}),
                "data": json.dumps(response_data.get("data", {}))
            },
            "lyrebirdInternalFlow": "datamanager"
        }
        
        # 更新Mock数据
        update_result = await self._update_mock(mock_data)
        if update_result.error:
            return update_result
        
        # 返回字符串格式的结果
        result = {
            "message": "成功从流量创建并更新Mock数据",
            "mock_id": mock_id,
            "mock_name": mock_name
        }
        return ToolResult(output=json.dumps(result))

    async def _update_mock(self, mock_data: Dict[str, Any]) -> ToolResult:
        """更新Mock数据"""
        url = f"{self.base_url}/api/data"
        response = requests.put(url, json=mock_data)
        if response.status_code == 200:
            # 将JSON响应转换为字符串
            return ToolResult(output=json.dumps(response.json()))
        return ToolResult(error=f"更新Mock数据失败: {response.status_code}") 