"""
简单测试API连通性
"""

import requests

# 测试房间搜索API
url = "http://160.16.67.238:5000/api/rooms/search"
params = {
    "checkin": "2025-12-01",
    "checkout": "2025-12-03",
    "adults": 2,
    "rooms": 1,
    "children": 0,
}

print("正在测试API...")
print(f"URL: {url}")
print(f"参数: {params}")

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"\n状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(data)
        print(f"成功: {data.get('success')}")
        print(f"房型数量: {data.get('count')}")
        print("\n✅ API连接成功!")
    else:
        print("\n❌ API返回错误")

except Exception as e:
    print(f"\n❌ 连接失败: {e}")
