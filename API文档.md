# YuzaWaMD 酒店预订API文档

## API概述
YuzaWaMD酒店预订API是一个RESTful接口服务，提供酒店房间查询和预订功能。该API直接连接QloApps数据库，提供实时的房间可用性和价格信息。

**基础URL:** `http://192.168.100.251/yuzawamd/hotel_api.php`

---

## 接口列表

### 1. 获取API帮助信息
获取API的基本信息和可用接口列表。

**请求方式:** `GET`  
**接口地址:** `/hotel_api.php?action=help`

**请求参数:** 无

**返回示例:**
```json
{
    "success": true,
    "message": "YuzaWaMD Hotel Booking API",
    "version": "1.0",
    "endpoints": {
        "GET /yuzawamd/hotel_api.php?action=help": "显示帮助信息",
        "GET /yuzawamd/hotel_api.php?action=check": "查询房间可用性",
        "POST /yuzawamd/hotel_api.php?action=book": "创建预订",
        "GET /yuzawamd/hotel_api.php?action=status": "查询订单状态"
    }
}
```

---

### 2. 查询可用房间
根据入住日期、退房日期、入住人数等条件查询可用房间。

**请求方式:** `GET`  
**接口地址:** `/hotel_api.php?action=check`

**请求参数:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `date_from` | string | 是 | 入住日期，格式：YYYY-MM-DD |
| `date_to` | string | 是 | 退房日期，格式：YYYY-MM-DD |
| `adults` | integer | 否 | 成人数量，默认1人 |
| `children` | integer | 否 | 儿童数量，默认0人 |

**成功返回示例:**
```json
{
    "success": true,
    "search_params": {
        "check_in": "2024-03-20",
        "check_out": "2024-03-22",
        "nights": 2,
        "adults": 2,
        "children": 0
    },
    "results": [
        {
            "hotel_id": 1,
            "hotel_name": "YuzaWaMD Hotel",
            "room_type_id": 1,
            "room_type_name": "海景标准间",
            "available_rooms": [
                {"id_room": 101, "room_num": "101"},
                {"id_room": 102, "room_num": "102"}
            ],
            "total_available": 3,
            "max_adults": 2,
            "max_children": 1,
            "amenities": ["免费WiFi", "空调", "24小时热水", "海景"],
            "price_per_night": 288.00,
            "nights": 2,
            "total_price": 576.00
        }
    ],
    "total_options": 1,
    "data_source": "database"
}
```

**请求示例:**
```bash
curl "http://yourserver.com/yuzawamd/hotel_api.php?action=check&date_from=2024-03-20&date_to=2024-03-22&adults=2"
```

**错误返回:**
- 日期格式错误：返回400状态码，提示"Invalid date format. Use YYYY-MM-DD"
- 退房日期早于入住日期：返回400状态码，提示"Check-out date must be after check-in date"

---

### 3. 创建预订
创建新的酒店预订订单。

**请求方式:** `POST`  
**接口地址:** `/hotel_api.php?action=book`  
**Content-Type:** `application/json`

**请求参数（JSON格式）:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `customer_name` | string | 是 | 客人姓名 |
| `customer_email` | string | 是 | 客人邮箱 |
| `customer_phone` | string | 否 | 客人电话 |
| `room_type_id` | integer | 是 | 房型ID（从查询接口获取） |
| `check_in` | string | 是 | 入住日期，格式：YYYY-MM-DD |
| `check_out` | string | 是 | 退房日期，格式：YYYY-MM-DD |
| `adults` | integer | 否 | 成人数量，默认1人 |
| `children` | integer | 否 | 儿童数量，默认0人 |

**请求体示例:**
```json
{
    "customer_name": "张三",
    "customer_email": "zhangsan@example.com",
    "customer_phone": "13800138000",
    "room_type_id": 1,
    "check_in": "2024-03-20",
    "check_out": "2024-03-22",
    "adults": 2,
    "children": 0
}
```

**成功返回示例:**
```json
{
    "success": true,
    "message": "预订创建成功",
    "order": {
        "order_id": 12345,
        "order_reference": "YMDABC123456789",
        "booking_id": 67890,
        "customer": {
            "name": "张三",
            "email": "zhangsan@example.com",
            "phone": "13800138000"
        },
        "room": {
            "room_type_id": 1,
            "room_type_name": "海景标准间",
            "room_number": "101"
        },
        "hotel": {
            "id": 1,
            "name": "YuzaWaMD海景大酒店",
            "address": "海滨路1号",
            "phone": "0755-12345678",
            "check_in_time": "14:00",
            "check_out_time": "12:00"
        },
        "booking_details": {
            "check_in": "2024-03-20",
            "check_out": "2024-03-22",
            "nights": 2,
            "adults": 2,
            "children": 0,
            "price_per_night": 288.00,
            "total_amount": 576.00,
            "currency": "CNY"
        },
        "status": "Confirmed",
        "payment_status": "Pending",
        "created_at": "2024-01-01 12:00:00"
    }
}
```

**请求示例:**
```bash
curl -X POST "http://yourserver.com/yuzawamd/hotel_api.php?action=book" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "张三",
    "customer_email": "zhangsan@example.com",
    "room_type_id": 1,
    "check_in": "2024-03-20",
    "check_out": "2024-03-22"
  }'
```

**错误返回:**
- 缺少必填字段：返回400状态码，并列出缺失的字段
- 邮箱格式错误：返回400状态码，提示"Invalid email format"
- 房型无效：返回400状态码，提示"Room type not found or inactive"

---

### 4. 查询订单状态
查询已创建订单的状态信息。

**请求方式:** `GET`  
**接口地址:** `/hotel_api.php?action=status`

**请求参数:**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `order_id` | integer | 二选一 | 订单ID |
| `reference` | string | 二选一 | 订单号 |

*注：order_id和reference至少提供一个*

**成功返回示例:**
```json
{
    "success": true,
    "order": {
        "order_id": 12345,
        "reference": "YMDABC123456789",
        "status": "Confirmed",
        "payment_status": "Paid",
        "customer": {
            "name": "张三",
            "email": "zhangsan@example.com",
            "phone": "13800138000"
        },
        "booking_details": {
            "check_in": "2024-03-20",
            "check_out": "2024-03-22",
            "nights": 2,
            "adults": 2,
            "children": 0,
            "total_amount": 576.00
        }
    }
}
```

**请求示例:**
```bash
# 使用订单ID查询
curl "http://yourserver.com/yuzawamd/hotel_api.php?action=status&order_id=12345"

# 使用订单号查询
curl "http://yourserver.com/yuzawamd/hotel_api.php?action=status&reference=YMDABC123456789"
```

---

### 5. 测试接口连通性
测试API是否正常运行。

**请求方式:** `GET`  
**接口地址:** `/hotel_api.php?action=test`

**返回示例:**
```json
{
    "success": true,
    "message": "YuzaWaMD Hotel API is working!",
    "server_time": "2024-01-01 12:00:00"
}
```

---

## 错误码说明

| HTTP状态码 | 说明 |
|------------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |

**错误返回格式:**
```json
{
    "error": "错误类型",
    "message": "详细错误说明"
}
```

---

## 调用示例

### PHP调用示例
```php
<?php
// 查询可用房间
$url = 'http://yourserver.com/yuzawamd/hotel_api.php';
$params = [
    'action' => 'check',
    'date_from' => '2024-03-20',
    'date_to' => '2024-03-22',
    'adults' => 2
];
$response = file_get_contents($url . '?' . http_build_query($params));
$data = json_decode($response, true);

// 创建预订
$booking_data = [
    'customer_name' => '张三',
    'customer_email' => 'zhangsan@example.com',
    'room_type_id' => 1,
    'check_in' => '2024-03-20',
    'check_out' => '2024-03-22'
];

$options = [
    'http' => [
        'method' => 'POST',
        'header' => 'Content-Type: application/json',
        'content' => json_encode($booking_data)
    ]
];
$context = stream_context_create($options);
$response = file_get_contents($url . '?action=book', false, $context);
?>
```

### Python调用示例
```python
import requests
import json

# 查询可用房间
params = {
    'action': 'check',
    'date_from': '2024-03-20',
    'date_to': '2024-03-22',
    'adults': 2
}
response = requests.get('http://yourserver.com/yuzawamd/hotel_api.php', params=params)
data = response.json()

# 创建预订
booking_data = {
    'customer_name': '张三',
    'customer_email': 'zhangsan@example.com',
    'room_type_id': 1,
    'check_in': '2024-03-20',
    'check_out': '2024-03-22'
}
response = requests.post(
    'http://yourserver.com/yuzawamd/hotel_api.php?action=book',
    json=booking_data
)
result = response.json()
```

### JavaScript/jQuery调用示例
```javascript
// 查询可用房间
$.ajax({
    url: 'http://yourserver.com/yuzawamd/hotel_api.php',
    type: 'GET',
    data: {
        action: 'check',
        date_from: '2024-03-20',
        date_to: '2024-03-22',
        adults: 2
    },
    success: function(data) {
        console.log('可用房间:', data);
    }
});

// 创建预订
$.ajax({
    url: 'http://yourserver.com/yuzawamd/hotel_api.php?action=book',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
        customer_name: '张三',
        customer_email: 'zhangsan@example.com',
        room_type_id: 1,
        check_in: '2024-03-20',
        check_out: '2024-03-22'
    }),
    success: function(data) {
        console.log('预订成功:', data);
    }
});
```

---

## 注意事项

1. **日期格式**：所有日期必须使用YYYY-MM-DD格式
2. **编码**：API使用UTF-8编码，请确保请求和响应都使用UTF-8
3. **价格**：所有价格以人民币（CNY）为单位，返回浮点数
4. **时区**：所有时间使用服务器本地时间
5. **邮箱验证**：创建预订时会验证邮箱格式的有效性
6. **房间数量**：每次预订只能预订一间房
7. **支付**：API创建的订单默认为"待支付"状态

---

## 联系方式
如有问题或需要技术支持，请联系技术团队。

**版本:** 1.0  
**最后更新:** 2024年