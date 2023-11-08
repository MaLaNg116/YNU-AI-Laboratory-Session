import pandas as pd

# 清洗病历类型的数据
df = pd.read_csv("Depression_Unwashed.csv", encoding="utf-8")
mask = df['回答'].str.match('^一、初次面诊')
df = df[~mask]

# 清洗存在空值的数据
print("移除空值前")
print(df[df.isna().any(axis=1)])
df.dropna(axis=0, how='any', inplace=True)
print("移除空值后")
print(df[df.isna().any(axis=1)])
df.to_csv("Depression_Washed.csv", encoding="utf-8-sig", index=False)
