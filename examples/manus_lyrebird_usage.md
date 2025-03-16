# Manus 中使用 Lyrebird 功能示例

本文档展示了如何在 Manus 代理中使用 Lyrebird 相关功能。Lyrebird 是一个请求代理工具，可以用于捕获和模拟 HTTP 请求，在自动化测试中非常有用。

## 前提条件

1. 确保 Lyrebird 代理服务器已启动并运行在默认地址 `http://localhost:9090`
2. 确保 Manus 代理已正确配置并运行

## 使用示例

以下是一些在 Manus 中使用 Lyrebird 功能的示例对话：

### 示例 1：获取所有请求记录

**用户**：
```
获取当前所有的 Lyrebird 代理记录
```

**Manus 将执行**：
```python
# Manus 将使用 LyrebirdTool 执行以下操作
await lyrebird_tool.execute(action="get_flows")
```

### 示例 2：获取特定请求记录

**用户**：
```
获取 ID 为 "d429e8f8-f4fc-4c92-81b2-7c9866a0e9c0" 的 Lyrebird 请求记录详情
```

**Manus 将执行**：
```python
# Manus 将使用 LyrebirdTool 执行以下操作
await lyrebird_tool.execute(
    action="get_flow", 
    flow_id="d429e8f8-f4fc-4c92-81b2-7c9866a0e9c0"
)
```

### 示例 3：获取 Mock 数据目录结构

**用户**：
```
查看 Lyrebird 中的 Mock 数据目录结构
```

**Manus 将执行**：
```python
# Manus 将使用 LyrebirdTool 执行以下操作
await lyrebird_tool.execute(action="get_groups")
```

### 示例 4：创建 Mock 数据目录

**用户**：
```
在 Lyrebird 根目录下创建一个名为 "test_api" 的 Mock 数据目录
```

**Manus 将执行**：
```python
# 首先获取目录结构，找到根目录 ID
groups_result = await lyrebird_tool.execute(action="get_groups")
root_id = groups_result.output.get("data", {}).get("id")

# 然后创建目录
await lyrebird_tool.execute(
    action="create_group",
    parent_id=root_id,
    name="test_api"
)
```

### 示例 5：将请求记录保存为 Mock 数据

**用户**：
```
将 ID 为 "df95807f-3920-42f3-9945-ad2e2d6b604c" 的请求记录保存为 Mock 数据，保存到 "test_api" 目录下
```

**Manus 将执行**：
```python
# 首先获取目录结构，找到目标目录 ID
groups_result = await lyrebird_tool.execute(action="get_groups")
root_data = groups_result.output.get("data", {})
target_group_id = None

# 遍历查找目标目录
for child in root_data.get("children", []):
    if child.get("name") == "test_api":
        target_group_id = child.get("id")
        break

# 然后创建 Mock 数据
if target_group_id:
    await lyrebird_tool.execute(
        action="create_mock",
        parent_id=target_group_id,
        flow_id="df95807f-3920-42f3-9945-ad2e2d6b604c",
        name="order_api_mock"
    )
```

### 示例 6：复杂场景 - 查找并保存特定 API 的请求记录

**用户**：
```
查找所有 Lyrebird 代理记录中 URL 包含 "/api/orders" 的请求，并将其保存为 Mock 数据
```

**Manus 将执行**：
```python
# 获取所有请求记录
flows_result = await lyrebird_tool.execute(action="get_flows")
flows = flows_result.output

# 查找匹配的请求
target_flow = None
for flow in flows:
    request = flow.get("request", {})
    if "/api/orders" in request.get("url", ""):
        target_flow = flow
        break

if target_flow:
    # 获取目录结构
    groups_result = await lyrebird_tool.execute(action="get_groups")
    root_id = groups_result.output.get("data", {}).get("id")
    
    # 创建目录（如果需要）
    group_result = await lyrebird_tool.execute(
        action="create_group",
        parent_id=root_id,
        name="order_api_mocks"
    )
    group_id = group_result.output.get("data", {}).get("group_id")
    
    # 创建 Mock 数据
    await lyrebird_tool.execute(
        action="create_mock",
        parent_id=group_id,
        flow_id=target_flow.get("id"),
        name="order_api_mock"
    )
```

## 注意事项

1. Manus 会根据用户的自然语言请求自动选择合适的工具和参数，用户不需要知道具体的 API 调用细节
2. 如果 Lyrebird 服务器未运行，Manus 会返回相应的错误信息
3. 对于复杂的操作，Manus 可能会分步执行多个 Lyrebird 相关操作
4. 用户可以使用自然语言描述需求，例如"保存最近的登录请求为 Mock 数据"，Manus 会自动解析并执行相应操作 