import pandas as pd

# 读取数据文件
file_path = "./data/abalone.data"  # 替换为实际文件路径
column_names = ["Sex", "Length", "Diameter", "Height", "Whole weight",
                "Shucked weight", "Viscera weight", "Shell weight", "Rings"]
data = pd.read_csv(file_path, header=None, names=column_names)

print(f"The number of rows with 'Sex' equal to 'I' is: {data[data['Sex'] == 'I'].shape[0]}")
print(f"The number of rows with 'Sex' equal to 'M' is: {data[data['Sex'] == 'M'].shape[0]}")
print(f"The number of rows with 'Sex' equal to 'F' is: {data[data['Sex'] == 'F'].shape[0]}")


