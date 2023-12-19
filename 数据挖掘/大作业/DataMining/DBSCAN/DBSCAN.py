import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA

eps = 0.90
min_samples = 490

# 读取数据文件
file_path = "../data/abalone.data"  # 替换为实际文件路径
column_names = ["Sex", "Length", "Diameter", "Height", "Whole weight",
                "Shucked weight", "Viscera weight", "Shell weight", "Rings"]
data = pd.read_csv(file_path, header=None, names=column_names)

# 使用LabelEncoder将标签编码为数字
label_encoder = LabelEncoder()
data['Sex'] = label_encoder.fit_transform(data['Sex'])

# 提取特征列和标签列
X = data.drop("Sex", axis=1)
y_true = data["Sex"]

# 使用PCA进行降维
pca = PCA(n_components=1)  # 设置为None，表示保留所有主成分
X_auto = pca.fit_transform(X)

# 查看PCA保留的维度
num_components = pca.n_components_
print("Number of PCA Components:", num_components)

# 使用DBSCAN进行聚类
dbscan = DBSCAN(eps=eps, min_samples=min_samples)
labels = dbscan.fit_predict(X_auto)

# 计算准确率
accuracy = accuracy_score(y_true, labels)

# 查看类别数
num_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # 排除噪声点的影响

print("Number of Clusters:", num_clusters)
print("Clustering Accuracy:", round((accuracy * 100), 2), "%")
