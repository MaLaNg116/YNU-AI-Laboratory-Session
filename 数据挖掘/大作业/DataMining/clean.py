import pandas as pd

# 读取数据文件
file_path = "./data/abalone.data"  # 替换为实际文件路径
column_names = ["Sex", "Length", "Diameter", "Height", "Whole",
                "Shucked", "Viscera", "Shell", "Rings"]
data = pd.read_csv(file_path, header=None, names=column_names)

# 将数据文件保存成csv格式
data.to_csv("./data/abalone.csv", index=False)
