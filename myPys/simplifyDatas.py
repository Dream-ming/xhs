import pandas as pd

# 加载 JSON 数据
data = [
    {"Name": "Alice", "Age": 25, "City": "New York"},
    {"Name": "Bob", "Age": 30, "City": "Los Angeles"},
    {"Name": "Charlie", "Age": 35, "City": "Chicago"}
]

df = pd.read_json("search_contents_2024-12-24.json")

# 将 JSON 数据转换为 DataFrame
# df = pd.DataFrame(data)

# 写入 CSV 文件
df.to_csv("output.csv", index=False, encoding="utf-8-sig")

print("数据已成功写入 CSV 文件！")
