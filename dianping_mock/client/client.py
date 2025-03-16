import requests
import json
import time
import random
from typing import Dict, Any, List, Optional

class DianpingClient:
    """大众点评客户端，用于模拟调用大众点评API接口"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:9090/mock/http://localhost:8000"):
        """初始化客户端
        
        Args:
            base_url: API服务器的基础URL
        """
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.username = None
        self.headers = {}
    
    def _request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """发送HTTP请求
        
        Args:
            method: HTTP方法（GET, POST等）
            endpoint: API端点
            params: URL参数
            data: 请求体数据
            
        Returns:
            响应数据
        """
        url = f"{self.base_url}{endpoint}"
        
        # 如果已登录，添加token到请求头
        headers = self.headers.copy()
        
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            raise ValueError(f"不支持的HTTP方法: {method}")
        
        # 检查响应状态
        if response.status_code >= 400:
            print(f"请求失败: {response.status_code} - {response.text}")
            return {"error": response.text}
        
        # 尝试解析JSON响应
        try:
            return response.json()
        except:
            return {"text": response.text}
    
    def login(self, username: str, password: str) -> Dict:
        """用户登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            登录响应
        """
        print(f"\n===== 用户登录 =====")
        print(f"用户名: {username}")
        print(f"密码: {'*' * len(password)}")
        
        data = {"username": username, "password": password}
        response = self._request("POST", "/api/login", data=data)
        
        if "token" in response:
            self.token = response["token"]
            self.user_id = response["user_id"]
            self.username = response["username"]
            self.headers = {"token": self.token}
            print(f"登录成功! 欢迎, {self.username}!")
        else:
            print(f"登录失败: {response.get('detail', '未知错误')}")
        
        return response
    
    def get_user_info(self) -> Dict:
        """获取用户信息
        
        Returns:
            用户信息
        """
        print(f"\n===== 获取用户信息 =====")
        
        response = self._request("GET", "/api/user/info")
        
        if "error" not in response:
            print(f"用户ID: {response['id']}")
            print(f"用户名: {response['username']}")
            print(f"手机号: {response['phone']}")
            print(f"积分: {response['points']}")
            print(f"等级: {response['level']}")
        
        return response
    
    def search_restaurants(self, keyword: str, page: int = 1, page_size: int = 10) -> Dict:
        """搜索餐厅
        
        Args:
            keyword: 搜索关键词
            page: 页码
            page_size: 每页数量
            
        Returns:
            搜索结果
        """
        print(f"\n===== 搜索餐厅 =====")
        print(f"关键词: {keyword}")
        
        params = {
            "keyword": keyword,
            "type": "restaurant",
            "page": page,
            "page_size": page_size
        }
        
        response = self._request("GET", "/api/search", params=params)
        
        if "error" not in response and "items" in response:
            print(f"找到 {response['total']} 个结果:")
            for i, restaurant in enumerate(response["items"], 1):
                print(f"{i}. {restaurant['name']} - {restaurant['address']} - 评分: {restaurant['rating']}")
        
        return response
    
    def get_restaurants(self, category: str = None, sort_by: str = "rating", page: int = 1, page_size: int = 10) -> List:
        """获取餐厅列表
        
        Args:
            category: 餐厅分类
            sort_by: 排序方式（rating或price）
            page: 页码
            page_size: 每页数量
            
        Returns:
            餐厅列表
        """
        print(f"\n===== 获取餐厅列表 =====")
        if category:
            print(f"分类: {category}")
        print(f"排序方式: {'评分' if sort_by == 'rating' else '价格'}")
        
        params = {
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by
        }
        
        if category:
            params["category"] = category
        
        response = self._request("GET", "/api/restaurants", params=params)
        
        if isinstance(response, list):
            print(f"找到 {len(response)} 个餐厅:")
            for i, restaurant in enumerate(response, 1):
                print(f"{i}. {restaurant['name']} - {restaurant['address']} - 评分: {restaurant['rating']} - 人均: ¥{restaurant['price_per_person']}")
        
        return response
    
    def get_restaurant_detail(self, restaurant_id: str) -> Dict:
        """获取餐厅详情
        
        Args:
            restaurant_id: 餐厅ID
            
        Returns:
            餐厅详情
        """
        print(f"\n===== 获取餐厅详情 =====")
        print(f"餐厅ID: {restaurant_id}")
        
        response = self._request("GET", f"/api/restaurants/{restaurant_id}")
        
        if "error" not in response:
            print(f"餐厅名称: {response['name']}")
            print(f"地址: {response['address']}")
            print(f"电话: {response['phone']}")
            print(f"分类: {', '.join(response['categories'])}")
            print(f"评分: {response['rating']}")
            print(f"人均: ¥{response['price_per_person']}")
            print(f"营业时间: {response['business_hours']}")
        
        return response
    
    def get_restaurant_dishes(self, restaurant_id: str) -> List:
        """获取餐厅菜品
        
        Args:
            restaurant_id: 餐厅ID
            
        Returns:
            菜品列表
        """
        print(f"\n===== 获取餐厅菜品 =====")
        print(f"餐厅ID: {restaurant_id}")
        
        response = self._request("GET", f"/api/restaurants/{restaurant_id}/dishes")
        
        if isinstance(response, list):
            print(f"找到 {len(response)} 个菜品:")
            for i, dish in enumerate(response, 1):
                print(f"{i}. {dish['name']} - ¥{dish['price']} - {dish['description']} - 月售: {dish['sales']}")
        
        return response
    
    def get_restaurant_reviews(self, restaurant_id: str, page: int = 1, page_size: int = 10) -> List:
        """获取餐厅评论
        
        Args:
            restaurant_id: 餐厅ID
            page: 页码
            page_size: 每页数量
            
        Returns:
            评论列表
        """
        print(f"\n===== 获取餐厅评论 =====")
        print(f"餐厅ID: {restaurant_id}")
        
        params = {
            "page": page,
            "page_size": page_size
        }
        
        response = self._request("GET", f"/api/restaurants/{restaurant_id}/reviews", params=params)
        
        if isinstance(response, list):
            print(f"找到 {len(response)} 条评论:")
            for i, review in enumerate(response, 1):
                print(f"{i}. {review['username']} - 评分: {review['rating']} - {review['content']} - {review['time']}")
        
        return response
    
    def get_user_coupons(self) -> List:
        """获取用户优惠券
        
        Returns:
            优惠券列表
        """
        print(f"\n===== 获取用户优惠券 =====")
        
        response = self._request("GET", "/api/user/coupons")
        
        if isinstance(response, list):
            print(f"找到 {len(response)} 张优惠券:")
            for i, coupon in enumerate(response, 1):
                if coupon["type"] == "discount":
                    print(f"{i}. {coupon['name']} - 满{coupon['min_amount']}减{coupon['value']} - 有效期至: {coupon['expire_date']}")
                else:
                    print(f"{i}. {coupon['name']} - {int(coupon['value'] * 100)}%折扣 - 有效期至: {coupon['expire_date']}")
        
        return response
    
    def get_restaurant_group_buys(self, restaurant_id: str) -> List:
        """获取餐厅团购
        
        Args:
            restaurant_id: 餐厅ID
            
        Returns:
            团购列表
        """
        print(f"\n===== 获取餐厅团购 =====")
        print(f"餐厅ID: {restaurant_id}")
        
        response = self._request("GET", f"/api/restaurants/{restaurant_id}/group_buys")
        
        if isinstance(response, list):
            print(f"找到 {len(response)} 个团购:")
            for i, group_buy in enumerate(response, 1):
                print(f"{i}. {group_buy['name']} - 原价: ¥{group_buy['original_price']} - 现价: ¥{group_buy['current_price']} - 已售: {group_buy['sold']}")
                print(f"   详情: {group_buy['details']}")
        
        return response
    
    def create_order(self, restaurant_id: str, group_buy_id: str, quantity: int, 
                    address: str, phone: str, coupon_id: str = None, remark: str = None) -> Dict:
        """创建订单
        
        Args:
            restaurant_id: 餐厅ID
            group_buy_id: 团购ID
            quantity: 数量
            address: 地址
            phone: 电话
            coupon_id: 优惠券ID
            remark: 备注
            
        Returns:
            订单信息
        """
        print(f"\n===== 创建订单 =====")
        print(f"餐厅ID: {restaurant_id}")
        print(f"团购ID: {group_buy_id}")
        print(f"数量: {quantity}")
        if coupon_id:
            print(f"优惠券ID: {coupon_id}")
        
        data = {
            "restaurant_id": restaurant_id,
            "group_buy_id": group_buy_id,
            "quantity": quantity,
            "address": address,
            "phone": phone
        }
        
        if coupon_id:
            data["coupon_id"] = coupon_id
        
        if remark:
            data["remark"] = remark
        
        response = self._request("POST", "/api/orders", data=data)
        
        if "error" not in response:
            print(f"订单创建成功!")
            print(f"订单ID: {response['order_id']}")
            print(f"状态: {response['status']}")
            print(f"总金额: ¥{response['total_amount']}")
            if response['discount_amount'] > 0:
                print(f"优惠金额: ¥{response['discount_amount']}")
            print(f"实付金额: ¥{response['final_amount']}")
            print(f"创建时间: {response['create_time']}")
        
        return response
    
    def get_order_detail(self, order_id: str) -> Dict:
        """获取订单详情
        
        Args:
            order_id: 订单ID
            
        Returns:
            订单详情
        """
        print(f"\n===== 获取订单详情 =====")
        print(f"订单ID: {order_id}")
        
        response = self._request("GET", f"/api/orders/{order_id}")
        
        if "error" not in response:
            print(f"订单ID: {response['id']}")
            print(f"状态: {response['status']}")
            print(f"总金额: ¥{response['total_amount']}")
            if response['discount_amount'] > 0:
                print(f"优惠金额: ¥{response['discount_amount']}")
            print(f"实付金额: ¥{response['final_amount']}")
            print(f"创建时间: {response['create_time']}")
        
        return response
    
    def get_user_orders(self, status: str = None, page: int = 1, page_size: int = 10) -> List:
        """获取用户订单
        
        Args:
            status: 订单状态
            page: 页码
            page_size: 每页数量
            
        Returns:
            订单列表
        """
        print(f"\n===== 获取用户订单 =====")
        if status:
            print(f"状态: {status}")
        
        params = {
            "page": page,
            "page_size": page_size
        }
        
        if status:
            params["status"] = status
        
        response = self._request("GET", "/api/user/orders", params=params)
        
        if isinstance(response, list):
            print(f"找到 {len(response)} 个订单:")
            for i, order in enumerate(response, 1):
                print(f"{i}. 订单ID: {order['id']} - 状态: {order['status']} - 金额: ¥{order['final_amount']} - 时间: {order['create_time']}")
        
        return response
    
    def logout(self) -> Dict:
        """用户退出登录
        
        Returns:
            退出响应
        """
        print(f"\n===== 用户退出登录 =====")
        
        response = self._request("GET", "/api/logout")
        
        if "error" not in response:
            print(f"退出成功!")
            self.token = None
            self.user_id = None
            self.username = None
            self.headers = {}
        
        return response


def simulate_user_flow():
    """模拟用户从登录到下单团购的完整流程"""
    
    client = DianpingClient()
    
    # 1. 用户登录
    client.login("张三", "password123")
    time.sleep(1)
    
    # 2. 获取用户信息
    client.get_user_info()
    time.sleep(1)
    
    # 3. 搜索餐厅
    client.search_restaurants("火锅")
    time.sleep(1)
    
    # 4. 获取餐厅列表
    restaurants = client.get_restaurants()
    time.sleep(1)
    
    # 选择一个餐厅
    restaurant_id = restaurants[0]["id"]
    
    # 5. 获取餐厅详情
    client.get_restaurant_detail(restaurant_id)
    time.sleep(1)
    
    # 6. 获取餐厅菜品
    client.get_restaurant_dishes(restaurant_id)
    time.sleep(1)
    
    # 7. 获取餐厅评论
    client.get_restaurant_reviews(restaurant_id)
    time.sleep(1)
    
    # 8. 获取用户优惠券
    coupons = client.get_user_coupons()
    coupon_id = coupons[0]["id"] if coupons else None
    time.sleep(1)
    
    # 9. 获取餐厅团购
    group_buys = client.get_restaurant_group_buys(restaurant_id)
    time.sleep(1)
    
    if group_buys:
        # 选择一个团购
        group_buy_id = group_buys[0]["id"]
        
        # 10. 创建订单
        order_response = client.create_order(
            restaurant_id=restaurant_id,
            group_buy_id=group_buy_id,
            quantity=2,
            address="北京市朝阳区三里屯SOHO",
            phone="13800138000",
            coupon_id=coupon_id,
            remark="不要辣"
        )
        time.sleep(1)
        
        if "order_id" in order_response:
            # 11. 获取订单详情
            client.get_order_detail(order_response["order_id"])
            time.sleep(1)
    
    # 12. 获取用户订单
    client.get_user_orders()
    time.sleep(1)
    
    # 13. 退出登录
    client.logout()


if __name__ == "__main__":
    simulate_user_flow() 