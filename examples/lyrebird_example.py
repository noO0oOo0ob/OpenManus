#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Lyrebird工具使用示例

此示例展示了如何使用Lyrebird工具获取代理记录并将特定记录保存为Mock数据
"""

import asyncio
import json
from pprint import pprint

from app.tool import LyrebirdTool


async def main():
    """主函数"""
    # 创建Lyrebird工具实例
    lyrebird_tool = LyrebirdTool()
    
    print("=== 获取所有请求记录 ===")
    result = await lyrebird_tool.execute(action="get_flows")
    if result.error:
        print(f"错误: {result.error}")
    else:
        flows = result.output
        print(f"共获取到 {len(flows)} 条请求记录")
        
        # 打印前3条记录的基本信息
        for i, flow in enumerate(flows[:3]):
            print(f"\n记录 {i+1}:")
            print(f"ID: {flow.get('id')}")
            print(f"URL: {flow.get('request', {}).get('url')}")
            print(f"方法: {flow.get('request', {}).get('method')}")
            print(f"状态码: {flow.get('response', {}).get('code')}")
    
    # 如果有记录，获取第一条记录的详细信息
    if not result.error and flows:
        flow_id = flows[0].get('id')
        print(f"\n=== 获取特定请求记录 (ID: {flow_id}) ===")
        flow_result = await lyrebird_tool.execute(action="get_flow", flow_id=flow_id)
        if flow_result.error:
            print(f"错误: {flow_result.error}")
        else:
            print("成功获取特定请求记录")
            # 打印请求和响应的基本信息
            flow_data = flow_result.output.get("data", {})
            request = flow_data.get("request", {})
            response = flow_data.get("response", {})
            
            print("\n请求信息:")
            print(f"URL: {request.get('url')}")
            print(f"方法: {request.get('method')}")
            print(f"路径: {request.get('path')}")
            
            print("\n响应信息:")
            print(f"状态码: {response.get('code')}")
            
            # 获取目录结构
            print("\n=== 获取Mock数据目录结构 ===")
            groups_result = await lyrebird_tool.execute(action="get_groups")
            if groups_result.error:
                print(f"错误: {groups_result.error}")
            else:
                # 获取根目录ID
                root_data = groups_result.output.get("data", {})
                root_id = root_data.get("id")
                if root_id:
                    print(f"根目录ID: {root_id}")
                    
                    # 创建一个新的目录
                    group_name = "example_group"
                    print(f"\n=== 创建Mock数据目录 ({group_name}) ===")
                    group_result = await lyrebird_tool.execute(
                        action="create_group", 
                        parent_id=root_id, 
                        name=group_name
                    )
                    
                    if group_result.error:
                        print(f"错误: {group_result.error}")
                    else:
                        group_id = group_result.output.get("data", {}).get("group_id")
                        if group_id:
                            print(f"成功创建目录，ID: {group_id}")
                            
                            # 从请求记录创建Mock数据
                            print(f"\n=== 从请求记录创建Mock数据 ===")
                            mock_result = await lyrebird_tool.execute(
                                action="create_mock",
                                parent_id=group_id,
                                flow_id=flow_id,
                                name=f"mock_{request.get('path', 'unknown')}"
                            )
                            
                            if mock_result.error:
                                print(f"错误: {mock_result.error}")
                            else:
                                print("成功创建Mock数据:")
                                pprint(mock_result.output)


if __name__ == "__main__":
    asyncio.run(main()) 