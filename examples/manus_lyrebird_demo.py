#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manus 代理使用 Lyrebird 功能的演示脚本

此脚本展示了如何通过 Manus 代理使用 Lyrebird 功能
"""

import asyncio
from app.agent.manus import Manus
from app.logger import logger


async def demo_lyrebird_with_manus():
    """演示通过 Manus 使用 Lyrebird 功能"""
    agent = Manus()
    
    # 示例 1: 获取所有请求记录
    logger.info("=== 示例 1: 获取所有请求记录 ===")
    await agent.run("获取当前所有的 Lyrebird 代理记录，并显示前 3 条记录的基本信息")
    
    # 等待用户确认继续
    input("\n按回车键继续下一个示例...")
    
    # 示例 2: 获取 Mock 数据目录结构
    logger.info("\n=== 示例 2: 获取 Mock 数据目录结构 ===")
    await agent.run("查看 Lyrebird 中的 Mock 数据目录结构，并找出根目录 ID")
    
    # 等待用户确认继续
    input("\n按回车键继续下一个示例...")
    
    # 示例 3: 创建 Mock 数据目录
    logger.info("\n=== 示例 3: 创建 Mock 数据目录 ===")
    await agent.run("在 Lyrebird 根目录下创建一个名为 'api_test' 的 Mock 数据目录")
    
    # 等待用户确认继续
    input("\n按回车键继续下一个示例...")
    
    # 示例 4: 复杂场景 - 查找并保存特定 API 的请求记录
    logger.info("\n=== 示例 4: 查找并保存特定 API 的请求记录 ===")
    await agent.run("""
    请执行以下操作：
    1. 获取所有 Lyrebird 代理记录
    2. 查找其中 URL 包含 '/api/' 的第一条记录
    3. 将该记录保存为 Mock 数据，保存到 'api_test' 目录下
    4. 将操作结果以易于理解的方式展示出来
    """)


if __name__ == "__main__":
    # 提示用户确保 Lyrebird 代理服务器已启动
    print("请确保 Lyrebird 代理服务器已启动并运行在默认地址 http://localhost:9090")
    print("如果 Lyrebird 服务器未运行，演示将无法正常进行")
    input("准备好后，按回车键开始演示...")
    
    # 运行演示
    asyncio.run(demo_lyrebird_with_manus()) 