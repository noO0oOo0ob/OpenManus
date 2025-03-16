from fastapi import FastAPI, HTTPException, Depends, Header, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import random
import uuid
import time
from datetime import datetime, timedelta
import json
import uvicorn

# 创建FastAPI应用
app = FastAPI(
    title="大众点评Mock服务器", 
    description="模拟大众点评的API接口",
    root_path="",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟数据库
class MockDB:
    def __init__(self):
        self.users = {
            "user123": {
                "id": "user123",
                "username": "张三",
                "phone": "13800138000",
                "avatar": "https://example.com/avatar1.jpg",
                "password": "password123",
                "token": None,
                "points": 500,
                "level": 3,
                "orders": []
            },
            "user456": {
                "id": "user456",
                "username": "李四",
                "phone": "13900139000",
                "avatar": "https://example.com/avatar2.jpg",
                "password": "password456",
                "token": None,
                "points": 800,
                "level": 4,
                "orders": []
            }
        }
        
        self.restaurants = {
            "rest1": {
                "id": "rest1",
                "name": "海底捞火锅",
                "address": "北京市朝阳区三里屯SOHO 1号楼2层",
                "phone": "010-12345678",
                "categories": ["火锅", "川菜"],
                "rating": 4.8,
                "price_per_person": 138,
                "business_hours": "10:00-22:00",
                "images": [
                    "https://example.com/haidilao1.jpg",
                    "https://example.com/haidilao2.jpg"
                ],
                "location": {
                    "latitude": 39.932,
                    "longitude": 116.454
                }
            },
            "rest2": {
                "id": "rest2",
                "name": "外婆家",
                "address": "北京市海淀区中关村大街1号",
                "phone": "010-87654321",
                "categories": ["浙菜", "家常菜"],
                "rating": 4.5,
                "price_per_person": 88,
                "business_hours": "10:30-21:30",
                "images": [
                    "https://example.com/waipojia1.jpg",
                    "https://example.com/waipojia2.jpg"
                ],
                "location": {
                    "latitude": 39.984,
                    "longitude": 116.307
                }
            },
            "rest3": {
                "id": "rest3",
                "name": "必胜客",
                "address": "北京市西城区西单北大街1号",
                "phone": "010-66668888",
                "categories": ["披萨", "西餐"],
                "rating": 4.2,
                "price_per_person": 75,
                "business_hours": "10:00-22:00",
                "images": [
                    "https://example.com/pizzahut1.jpg",
                    "https://example.com/pizzahut2.jpg"
                ],
                "location": {
                    "latitude": 39.913,
                    "longitude": 116.373
                }
            }
        }
        
        self.dishes = {
            "rest1": [
                {"id": "dish101", "name": "鸳鸯火锅", "price": 98, "image": "https://example.com/yuanyang.jpg", "description": "一半麻辣，一半清汤", "sales": 1500},
                {"id": "dish102", "name": "毛肚", "price": 58, "image": "https://example.com/maodu.jpg", "description": "新鲜毛肚，脆嫩爽口", "sales": 2000},
                {"id": "dish103", "name": "虾滑", "price": 68, "image": "https://example.com/xiahua.jpg", "description": "鲜虾制作，口感Q弹", "sales": 1800}
            ],
            "rest2": [
                {"id": "dish201", "name": "东坡肉", "price": 68, "image": "https://example.com/dongporou.jpg", "description": "肥而不腻，入口即化", "sales": 1200},
                {"id": "dish202", "name": "西湖醋鱼", "price": 88, "image": "https://example.com/xihuyu.jpg", "description": "鲜嫩可口，酸甜适中", "sales": 1000},
                {"id": "dish203", "name": "龙井虾仁", "price": 78, "image": "https://example.com/longjingxiaren.jpg", "description": "茶香四溢，虾仁鲜嫩", "sales": 1300}
            ],
            "rest3": [
                {"id": "dish301", "name": "超级至尊披萨", "price": 99, "image": "https://example.com/pizza1.jpg", "description": "多种配料，口感丰富", "sales": 2200},
                {"id": "dish302", "name": "意式肉酱面", "price": 59, "image": "https://example.com/pasta.jpg", "description": "正宗意式风味", "sales": 1600},
                {"id": "dish303", "name": "香烤鸡翅", "price": 49, "image": "https://example.com/wings.jpg", "description": "外酥里嫩，香辣可口", "sales": 2500}
            ]
        }
        
        self.reviews = {
            "rest1": [
                {"id": "rev101", "user_id": "user123", "username": "张三", "rating": 5, "content": "服务很好，菜品新鲜", "images": ["https://example.com/review1.jpg"], "time": "2023-05-10 18:30:00"},
                {"id": "rev102", "user_id": "user456", "username": "李四", "rating": 4, "content": "环境不错，就是有点贵", "images": [], "time": "2023-06-15 19:45:00"}
            ],
            "rest2": [
                {"id": "rev201", "user_id": "user123", "username": "张三", "rating": 4, "content": "菜品地道，价格实惠", "images": ["https://example.com/review2.jpg"], "time": "2023-04-20 12:30:00"},
                {"id": "rev202", "user_id": "user456", "username": "李四", "rating": 5, "content": "很喜欢这里的东坡肉", "images": ["https://example.com/review3.jpg"], "time": "2023-07-05 13:15:00"}
            ],
            "rest3": [
                {"id": "rev301", "user_id": "user123", "username": "张三", "rating": 3, "content": "披萨有点咸", "images": [], "time": "2023-03-10 18:00:00"},
                {"id": "rev302", "user_id": "user456", "username": "李四", "rating": 4, "content": "鸡翅很好吃，推荐", "images": ["https://example.com/review4.jpg"], "time": "2023-08-01 19:00:00"}
            ]
        }
        
        self.coupons = [
            {"id": "coupon1", "name": "满100减20", "type": "discount", "value": 20, "min_amount": 100, "expire_date": "2023-12-31"},
            {"id": "coupon2", "name": "满200减50", "type": "discount", "value": 50, "min_amount": 200, "expire_date": "2023-12-31"},
            {"id": "coupon3", "name": "8折优惠", "type": "percent", "value": 0.8, "min_amount": 0, "expire_date": "2023-12-31"}
        ]
        
        self.group_buys = {
            "rest1": [
                {"id": "gb101", "name": "双人火锅套餐", "original_price": 298, "current_price": 198, "sold": 356, "limit": 500, "expire_date": "2023-12-31", "details": "含鸳鸯锅底+6荤6素+2饮料"},
                {"id": "gb102", "name": "4人豪华套餐", "original_price": 598, "current_price": 398, "sold": 210, "limit": 300, "expire_date": "2023-12-31", "details": "含鸳鸯锅底+12荤12素+4饮料"}
            ],
            "rest2": [
                {"id": "gb201", "name": "双人浙菜套餐", "original_price": 198, "current_price": 138, "sold": 245, "limit": 400, "expire_date": "2023-12-31", "details": "含4道招牌菜+2份米饭+2饮料"},
                {"id": "gb202", "name": "家庭聚餐套餐", "original_price": 398, "current_price": 298, "sold": 178, "limit": 250, "expire_date": "2023-12-31", "details": "含8道招牌菜+4份米饭+4饮料"}
            ],
            "rest3": [
                {"id": "gb301", "name": "双人披萨套餐", "original_price": 178, "current_price": 118, "sold": 320, "limit": 450, "expire_date": "2023-12-31", "details": "含1个9寸披萨+2份小吃+2饮料"},
                {"id": "gb302", "name": "家庭欢乐套餐", "original_price": 298, "current_price": 218, "sold": 265, "limit": 350, "expire_date": "2023-12-31", "details": "含1个12寸披萨+4份小吃+4饮料"}
            ]
        }
        
        self.orders = {}
        self.tokens = {}

# 初始化模拟数据库
db = MockDB()

# 模型定义
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user_id: str
    username: str
    avatar: str

class UserInfoResponse(BaseModel):
    id: str
    username: str
    phone: str
    avatar: str
    points: int
    level: int

class RestaurantBrief(BaseModel):
    id: str
    name: str
    address: str
    categories: List[str]
    rating: float
    price_per_person: int
    image: str

class RestaurantDetail(BaseModel):
    id: str
    name: str
    address: str
    phone: str
    categories: List[str]
    rating: float
    price_per_person: int
    business_hours: str
    images: List[str]
    location: Dict[str, float]

class Dish(BaseModel):
    id: str
    name: str
    price: float
    image: str
    description: str
    sales: int

class Review(BaseModel):
    id: str
    user_id: str
    username: str
    rating: int
    content: str
    images: List[str]
    time: str

class Coupon(BaseModel):
    id: str
    name: str
    type: str
    value: float
    min_amount: float
    expire_date: str

class GroupBuy(BaseModel):
    id: str
    name: str
    original_price: float
    current_price: float
    sold: int
    limit: int
    expire_date: str
    details: str

class OrderRequest(BaseModel):
    restaurant_id: str
    group_buy_id: str
    quantity: int
    coupon_id: Optional[str] = None
    address: str
    phone: str
    remark: Optional[str] = None

class OrderResponse(BaseModel):
    order_id: str
    status: str
    total_amount: float
    discount_amount: float
    final_amount: float
    create_time: str

# 工具函数
def get_current_user(token: str = Header(...)):
    if token not in db.tokens:
        raise HTTPException(status_code=401, detail="无效的令牌")
    return db.tokens[token]

# 路由定义
@app.post("/api/login", response_model=LoginResponse)
def login(request: LoginRequest):
    for user_id, user in db.users.items():
        if user["username"] == request.username and user["password"] == request.password:
            token = str(uuid.uuid4())
            db.users[user_id]["token"] = token
            db.tokens[token] = user_id
            return {
                "token": token,
                "user_id": user_id,
                "username": user["username"],
                "avatar": user["avatar"]
            }
    raise HTTPException(status_code=401, detail="用户名或密码错误")

@app.get("/api/user/info", response_model=UserInfoResponse)
def get_user_info(user_id: str = Depends(get_current_user)):
    user = db.users[user_id]
    return {
        "id": user["id"],
        "username": user["username"],
        "phone": user["phone"],
        "avatar": user["avatar"],
        "points": user["points"],
        "level": user["level"]
    }

@app.get("/api/restaurants", response_model=List[RestaurantBrief])
def get_restaurants(
    category: Optional[str] = None,
    sort_by: Optional[str] = "rating",
    page: int = 1,
    page_size: int = 10,
    user_id: Optional[str] = Depends(get_current_user)
):
    restaurants = list(db.restaurants.values())
    
    # 按分类筛选
    if category:
        restaurants = [r for r in restaurants if category in r["categories"]]
    
    # 排序
    if sort_by == "rating":
        restaurants.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "price":
        restaurants.sort(key=lambda x: x["price_per_person"])
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    paginated = restaurants[start:end]
    
    # 转换为简要信息
    result = []
    for r in paginated:
        result.append({
            "id": r["id"],
            "name": r["name"],
            "address": r["address"],
            "categories": r["categories"],
            "rating": r["rating"],
            "price_per_person": r["price_per_person"],
            "image": r["images"][0] if r["images"] else ""
        })
    
    return result

@app.get("/api/restaurants/{restaurant_id}", response_model=RestaurantDetail)
def get_restaurant_detail(
    restaurant_id: str,
    user_id: Optional[str] = Depends(get_current_user)
):
    if restaurant_id not in db.restaurants:
        raise HTTPException(status_code=404, detail="餐厅不存在")
    
    return db.restaurants[restaurant_id]

@app.get("/api/restaurants/{restaurant_id}/dishes", response_model=List[Dish])
def get_restaurant_dishes(
    restaurant_id: str,
    user_id: Optional[str] = Depends(get_current_user)
):
    if restaurant_id not in db.restaurants:
        raise HTTPException(status_code=404, detail="餐厅不存在")
    
    if restaurant_id not in db.dishes:
        return []
    
    return db.dishes[restaurant_id]

@app.get("/api/restaurants/{restaurant_id}/reviews", response_model=List[Review])
def get_restaurant_reviews(
    restaurant_id: str,
    page: int = 1,
    page_size: int = 10,
    user_id: Optional[str] = Depends(get_current_user)
):
    if restaurant_id not in db.restaurants:
        raise HTTPException(status_code=404, detail="餐厅不存在")
    
    if restaurant_id not in db.reviews:
        return []
    
    reviews = db.reviews[restaurant_id]
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    paginated = reviews[start:end]
    
    return paginated

@app.get("/api/user/coupons", response_model=List[Coupon])
def get_user_coupons(user_id: str = Depends(get_current_user)):
    # 简化处理，所有用户都有相同的优惠券
    return db.coupons

@app.get("/api/restaurants/{restaurant_id}/group_buys", response_model=List[GroupBuy])
def get_restaurant_group_buys(
    restaurant_id: str,
    user_id: Optional[str] = Depends(get_current_user)
):
    if restaurant_id not in db.restaurants:
        raise HTTPException(status_code=404, detail="餐厅不存在")
    
    if restaurant_id not in db.group_buys:
        return []
    
    return db.group_buys[restaurant_id]

@app.post("/api/orders", response_model=OrderResponse)
def create_order(
    order_request: OrderRequest,
    user_id: str = Depends(get_current_user)
):
    # 验证餐厅是否存在
    if order_request.restaurant_id not in db.restaurants:
        raise HTTPException(status_code=404, detail="餐厅不存在")
    
    # 验证团购是否存在
    group_buy = None
    for gb in db.group_buys.get(order_request.restaurant_id, []):
        if gb["id"] == order_request.group_buy_id:
            group_buy = gb
            break
    
    if not group_buy:
        raise HTTPException(status_code=404, detail="团购不存在")
    
    # 计算订单金额
    total_amount = group_buy["current_price"] * order_request.quantity
    discount_amount = 0
    
    # 应用优惠券
    if order_request.coupon_id:
        coupon = None
        for c in db.coupons:
            if c["id"] == order_request.coupon_id:
                coupon = c
                break
        
        if coupon and total_amount >= coupon["min_amount"]:
            if coupon["type"] == "discount":
                discount_amount = coupon["value"]
            elif coupon["type"] == "percent":
                discount_amount = total_amount * (1 - coupon["value"])
    
    final_amount = total_amount - discount_amount
    
    # 创建订单
    order_id = f"order_{int(time.time())}_{random.randint(1000, 9999)}"
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    order = {
        "id": order_id,
        "user_id": user_id,
        "restaurant_id": order_request.restaurant_id,
        "group_buy_id": order_request.group_buy_id,
        "quantity": order_request.quantity,
        "coupon_id": order_request.coupon_id,
        "address": order_request.address,
        "phone": order_request.phone,
        "remark": order_request.remark,
        "total_amount": total_amount,
        "discount_amount": discount_amount,
        "final_amount": final_amount,
        "status": "待使用",
        "create_time": create_time
    }
    
    db.orders[order_id] = order
    db.users[user_id]["orders"].append(order_id)
    
    return {
        "order_id": order_id,
        "status": "待使用",
        "total_amount": total_amount,
        "discount_amount": discount_amount,
        "final_amount": final_amount,
        "create_time": create_time
    }

@app.get("/api/orders/{order_id}")
def get_order_detail(
    order_id: str,
    user_id: str = Depends(get_current_user)
):
    if order_id not in db.orders:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    order = db.orders[order_id]
    
    if order["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="无权访问此订单")
    
    return order

@app.get("/api/user/orders")
def get_user_orders(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    user_id: str = Depends(get_current_user)
):
    user = db.users[user_id]
    orders = [db.orders[order_id] for order_id in user["orders"]]
    
    # 按状态筛选
    if status:
        orders = [o for o in orders if o["status"] == status]
    
    # 按时间排序
    orders.sort(key=lambda x: x["create_time"], reverse=True)
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    paginated = orders[start:end]
    
    return paginated

@app.get("/api/search")
def search(
    keyword: str,
    type: str = "restaurant",  # restaurant, dish
    page: int = 1,
    page_size: int = 10,
    user_id: Optional[str] = Depends(get_current_user)
):
    results = []
    
    if type == "restaurant":
        for r in db.restaurants.values():
            if keyword.lower() in r["name"].lower() or any(keyword.lower() in cat.lower() for cat in r["categories"]):
                results.append({
                    "id": r["id"],
                    "name": r["name"],
                    "address": r["address"],
                    "categories": r["categories"],
                    "rating": r["rating"],
                    "price_per_person": r["price_per_person"],
                    "image": r["images"][0] if r["images"] else ""
                })
    elif type == "dish":
        for rest_id, dishes in db.dishes.items():
            for dish in dishes:
                if keyword.lower() in dish["name"].lower() or keyword.lower() in dish["description"].lower():
                    dish_copy = dish.copy()
                    dish_copy["restaurant_id"] = rest_id
                    dish_copy["restaurant_name"] = db.restaurants[rest_id]["name"]
                    results.append(dish_copy)
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    paginated = results[start:end]
    
    return {
        "total": len(results),
        "items": paginated
    }

@app.get("/api/logout")
def logout(user_id: str = Depends(get_current_user)):
    # 找到用户的token并删除
    for uid, user in db.users.items():
        if uid == user_id and user["token"]:
            token = user["token"]
            if token in db.tokens:
                del db.tokens[token]
            user["token"] = None
            return {"message": "退出成功"}
    
    return {"message": "退出成功"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        forwarded_allow_ips="*",
        proxy_headers=True
    ) 