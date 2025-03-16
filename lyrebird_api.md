
# 获取所有请求记录
## api: 
http: //localhost:9090/api/flow GET
## 描述
接口用于获取所有请求记录，返回一个列表，列表中每个元素是一个请求记录，请求记录是一个字典，字典中包含请求的id、大小、持续时间、请求时间、请求、响应等信息。
## response样例: 
``` JSON
[
    {
        "id": "d429e8f8-f4fc-4c92-81b2-7c9866a0e9c0",
        "size": 1,
        "duration": 0.020318984985351562,
        "start_time": 1742132408.3280718,
        "request": {
            "url": "http://localhost:8000/api/logout",
            "scheme": "http",
            "host": "localhost",
            "path": "/api/logout",
            "params": "",
            "method": "GET",
            "port": 8000
        },
        "response": {
            "code": 200,
            "mock": "proxy",
            "modified": ""
        },
        "action": []
    }
]
```

# 获取指定请求记录
## api: 
http: //localhost:9090/api/flow/{id} GET
## 描述
接口用于获取指定请求记录，返回一个字典，字典中包含请求的id、大小、持续时间、请求时间、请求、响应等信息。相比获取所有请求记录，获取指定请求记录返回中额外包含了请求的 body 和 headers 字段。
## response样例: 
``` JSON
{
    "code": 1000,
    "data": {
        "client_address": "127.0.0.1",
        "duration": 0.030804157257080078,
        "id": "df95807f-3920-42f3-9945-ad2e2d6b604c",
        "request": {
            "data": {
                "address": "北京市朝阳区三里屯SOHO",
                "coupon_id": "coupon1",
                "group_buy_id": "gb101",
                "phone": "13800138000",
                "quantity": 2,
                "remark": "不要辣",
                "restaurant_id": "rest1"
            },
            "headers": {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate",
                "Content-Length": "219",
                "Content-Type": "application/json",
                "Token": "ee119416-e4fc-4065-83f1-077f2b27dc65",
                "User-Agent": "python-requests/2.25.1"
            },
            "host": "localhost",
            "method": "POST",
            "path": "/api/orders",
            "port": 8000,
            "query": {},
            "scheme": "http",
            "timestamp": 1742132405.228,
            "url": "http://localhost:8000/api/orders"
        },
        "response": {
            "code": 200,
            "data": {
                "create_time": "2025-03-16 21:40:05",
                "discount_amount": 20.0,
                "final_amount": 376.0,
                "order_id": "order_1742132405_2010",
                "status": "待使用",
                "total_amount": 396.0
            },
            "headers": {
                "content-length": "158",
                "content-type": "application/json",
                "date": "Sun, 16 Mar 2025 13:40:04 GMT",
                "lyrebird": "proxy",
                "server": "uvicorn"
            },
            "timestamp": 1742132405.257
        },
        "size": 6,
        "start_time": 1742132405.22728
    },
    "message": "success"
}
```

# 获取Mock数据的目录结构(结构为树形结构)
## api: 
http: //localhost:9090/api/group GET
## 描述
接口用于获取Mock数据的目录结构，返回一个字典，字典中包含目录的id、名称、父目录id、类型等信息。
- 目录结构为树形结构
- 其中name为$的节点为根节点
- 其中type为group的节点为目录节点，type为data的节点为数据节点
- 其中parent_id为null的节点为根节点
- 根节点有且仅有一个
- 节点下的 children 字段表示该节点下的子节点
## response样例: 
``` JSON
{
    "code": 1000,
    "data": {
        "abs_parent_path": "/",
        "children": [
            {
                "abs_parent_path": "/main/",
                "children": [
                    {
                        "abs_parent_path": "/main/posts/",
                        "id": "90f73fa1-cb66-499e-a93c-d12e03adf1bc",
                        "name": "/posts",
                        "parent": [
                            {
                                "id": "a5aadd67-0a1a-48b0-ab41-359b51668726",
                                "name": "$",
                                "parent_id": null,
                                "type": "group"
                            },
                            {
                                "id": "baa2dcae-d71b-4ea9-9c09-db4cd6caf41f",
                                "name": "main",
                                "parent_id": "a5aadd67-0a1a-48b0-ab41-359b51668726",
                                "type": "group"
                            },
                            {
                                "id": "90f73fa1-cb66-499e-a93c-d12e03adf1bc",
                                "name": "/posts",
                                "parent_id": "baa2dcae-d71b-4ea9-9c09-db4cd6caf41f",
                                "type": "data"
                            }
                        ],
                        "parent_id": "baa2dcae-d71b-4ea9-9c09-db4cd6caf41f",
                        "type": "data"
                    },
                    {
                        "abs_parent_path": "/main/data/",
                        "id": "ad346c07-f579-4a03-825f-173303942b80",
                        "name": "data",
                        "parent": [
                            {
                                "id": "a5aadd67-0a1a-48b0-ab41-359b51668726",
                                "name": "$",
                                "parent_id": null,
                                "type": "group"
                            },
                            {
                                "id": "baa2dcae-d71b-4ea9-9c09-db4cd6caf41f",
                                "name": "main",
                                "parent_id": "a5aadd67-0a1a-48b0-ab41-359b51668726",
                                "type": "group"
                            },
                            {
                                "id": "ad346c07-f579-4a03-825f-173303942b80",
                                "name": "data",
                                "parent_id": "baa2dcae-d71b-4ea9-9c09-db4cd6caf41f",
                                "type": "data"
                            }
                        ],
                        "parent_id": "baa2dcae-d71b-4ea9-9c09-db4cd6caf41f",
                        "type": "data"
                    }
                ],
                "id": "baa2dcae-d71b-4ea9-9c09-db4cd6caf41f",
                "name": "main",
                "parent": [
                    {
                        "id": "a5aadd67-0a1a-48b0-ab41-359b51668726",
                        "name": "$",
                        "parent_id": null,
                        "type": "group"
                    },
                    {
                        "id": "baa2dcae-d71b-4ea9-9c09-db4cd6caf41f",
                        "name": "main",
                        "parent_id": "a5aadd67-0a1a-48b0-ab41-359b51668726",
                        "type": "group"
                    }
                ],
                "parent_id": "a5aadd67-0a1a-48b0-ab41-359b51668726",
                "type": "group"
            }
        ],
        "id": "a5aadd67-0a1a-48b0-ab41-359b51668726",
        "label": [],
        "name": "$",
        "parent": [
            {
                "id": "a5aadd67-0a1a-48b0-ab41-359b51668726",
                "name": "$",
                "parent_id": null,
                "type": "group"
            }
        ],
        "parent_id": null,
        "type": "group"
    },
    "message": "success"
}
```
# 创建Mock数据目录
## api: 
http: //localhost:9090/api/group POST
## request body样例
``` JSON
{
    "name": "test",
    "parent_id": "a5aadd67-0a1a-48b0-ab41-359b51668726"
}
```
## 描述
接口用于创建Mock数据目录，返回一个字典，字典中包含目录的id、名称、父目录id、类型等信息。
- 请求 body 中需要包含 name 和 parent_id 字段
- name 为目录的名称
- parent_id 为父目录的id
- 根目录一定已存在，不可创建根目录
- 响应体中的group_id表示创建的目录的id
## response样例: 
``` JSON
{
    "code": 1000,
    "data": {
        "group_id": "50b1e9be-1f87-4350-aaac-9ad1261770bb"
    },
    "message": "success"
}
```

## 创建 Mock 数据
## api:
http: //localhost:9090/api/data POST
## request body样例
``` JSON
{
    "data": {
        "type": "data",
        "name": "testapi"
    },
    "parent_id": "50b1e9be-1f87-4350-aaac-9ad1261770bb"
}
```
## 描述
接口用于创建Mock数据，返回一个字典，字典中包含数据id、数据类型、数据名称、父目录id等信息。
- 请求 body 中需要包含 data 和 parent_id 字段
- data 为数据类型和名称
- parent_id 为父目录的id
- 响应体中的data_id表示创建的数据的id
## response样例
``` JSON
{
    "code": 1000,
    "data_id": "229e12a3-70fb-44a3-8c4c-a6d4c09d1bdb",
    "message": "success"
}
```
## 更新 Mock 数据
## api:
http: //localhost:9090/api/data PUT
## request body样例
``` JSON
{
    "id": "9fab0e0b-8aae-4c52-bfbe-653759d09f0c",
    "name": "/api/orders",
    "rule": {
        "request.url": "(?=.*/api/orders$)"
    },
    "request": {
        "url": "http://localhost:8000/api/orders",
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "219",
            "Content-Type": "application/json",
            "Token": "ee119416-e4fc-4065-83f1-077f2b27dc65",
            "User-Agent": "python-requests/2.25.1"
        },
        "method": "POST",
        "data": "{\"key\": \"value\"}"
    },
    "response": {
        "code": 200,
        "headers": {
            "content-length": "158",
            "content-type": "application/json",
            "date": "Sun, 16 Mar 2025 13:40:04 GMT",
            "lyrebird": "proxy",
            "server": "uvicorn"
        },
        "data": "{\"key\": \"value\"}"
    },
    "lyrebirdInternalFlow": "datamanager"
}
```
## 描述
接口用于更新指定 id的 Mock 数据内容，请求体包含当前 Mock 数据更新后的完整内容，响应体包含是否更新成功。
一条 Mock 数据包含以下结构
- id 字段不可更改
- name 字段表示 Mock 数据名称
- rule 字段表示 Mock 数据匹配规则
- request 字段表示 Mock 数据请求内容，包含 headers、body等字段
- response 字段表示 Mock 数据响内容，包含 headers、body等字段
- lyrebirdInternalFlow 字段表示 Mock 数据类型
## response样例
``` JSON
{
    "code": 1000,
    "message": "success"
}
```