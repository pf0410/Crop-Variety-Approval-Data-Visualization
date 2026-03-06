import requests
import pandas as pd
import math

# 从浏览器的开发者工具中获取
apitoken = "EjJ46nMm3zY02FkmBz0fezyDq08L42uO"  # API专用的令牌，用于接口认证
cookie = "JSESSIONID=BA9B54B73604C36376558CF7B8E6C145"  # 会话cookie，维护登录状态
token = ""   # 另一种认证令牌


# HTTP请求头配置
headers = {
    "apitoken": apitoken,
    "authorization": "",
    "cookie": cookie,
    "token": token,
    "referer": "http://202.127.42.144:60011/controlboard/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
}

base_url = "http://202.127.42.144:60011/v1/data-service/api/getDwdSdVarietyannouncementList" # 大数据平台的网站
page_size = 50 # 一页抓取50条数据

# 先请求第一页
params = {
    "page": 1,
    "pageSize": page_size,
    "cropid": "",
    "judgementyear": "",
    "judgementregion": "",
    "varietyname": "",
    "judgementno": "",
    "applycompany": "",
    "istransgenosis": "",
    "status": "",
    "introductionfilingnoSign": ""
}

resp = requests.get(base_url, params=params, headers=headers)
data = resp.json()

# 检查是否成功
print("第一条响应内容：", data)

if not data.get("data"):
    raise Exception("请求失败：请检查 apitoken / cookie / token 是否过期！")

total = data["data"]["total"]
print("总条数：", total)

num_pages = math.ceil(total / page_size)

all_rows = []

for page in range(1, num_pages + 1):
    params["page"] = page
    resp = requests.get(base_url, params=params, headers=headers)
    d = resp.json()

    if not d.get("data"):
        print(f"第 {page} 页失败，可能 cookie/token 过期")
        break

    rows = d["data"]["rowData"]
    all_rows.extend(rows)
    print(f"完成第 {page}/{num_pages} 页")

df = pd.DataFrame(all_rows)
df.to_excel("variety_announcements.xlsx", index=False)

print("数据已成功导出到 variety_announcements.xlsx")

