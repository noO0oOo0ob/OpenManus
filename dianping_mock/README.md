# 大众点评Mock服务

这是一个模拟大众点评的Mock服务器和客户端，用于模拟从用户登录到下单团购的完整流程。

## 项目结构

```
dianping_mock/
├── server/
│   └── app.py         # 服务器代码
└── client/
    └── client.py      # 客户端代码
```

## 功能特点

### 服务器端

Mock服务器使用FastAPI实现，提供以下API接口：

1. 用户登录 - `/api/login`
2. 获取用户信息 - `/api/user/info`
3. 获取餐厅列表 - `/api/restaurants`
4. 获取餐厅详情 - `/api/restaurants/{restaurant_id}`
5. 获取餐厅菜品 - `/api/restaurants/{restaurant_id}/dishes`
6. 获取餐厅评论 - `/api/restaurants/{restaurant_id}/reviews`
7. 获取用户优惠券 - `/api/user/coupons`
8. 获取餐厅团购 - `/api/restaurants/{restaurant_id}/group_buys`
9. 创建订单 - `/api/orders`
10. 获取订单详情 - `/api/orders/{order_id}`
11. 获取用户订单 - `/api/user/orders`
12. 搜索餐厅或菜品 - `/api/search`
13. 用户退出登录 - `/api/logout`

### 客户端

客户端使用Python requests库实现，提供以下功能：

1. 用户登录
2. 获取用户信息
3. 搜索餐厅
4. 获取餐厅列表
5. 获取餐厅详情
6. 获取餐厅菜品
7. 获取餐厅评论
8. 获取用户优惠券
9. 获取餐厅团购
10. 创建订单
11. 获取订单详情
12. 获取用户订单
13. 用户退出登录

## 运行说明

### 安装依赖

确保已安装以下依赖：

```bash
pip install fastapi uvicorn requests
```

### 运行服务器

在项目根目录下执行：

```bash
cd dianping_mock/server
uvicorn app:app --reload
```

服务器将在 http://localhost:8000 上运行。

你可以通过访问 http://localhost:8000/docs 查看API文档。

### 运行客户端

在另一个终端中执行：

```bash
cd dianping_mock/client
python client.py
```

客户端将模拟一个用户从登录到下单团购的完整流程。

## 模拟数据

服务器中包含以下模拟数据：

- 用户：张三、李四
- 餐厅：海底捞火锅、外婆家、必胜客
- 菜品：每个餐厅有3个菜品
- 评论：每个餐厅有2条评论
- 优惠券：满100减20、满200减50、8折优惠
- 团购：每个餐厅有2个团购套餐

## 自定义

你可以通过修改 `server/app.py` 中的 `MockDB` 类来自定义模拟数据。

## 注意事项

- 这是一个模拟服务，不包含真实的数据库，所有数据都存储在内存中。
- 服务器重启后，所有创建的订单等数据都会丢失。 