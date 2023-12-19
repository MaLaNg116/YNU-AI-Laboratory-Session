import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import time

# 读取数据文件
file_path = "./data/abalone.data"  # 替换为实际文件路径
column_names = ["Sex", "Length", "Diameter", "Height", "Whole weight",
                "Shucked weight", "Viscera weight", "Shell weight", "Rings"]
data = pd.read_csv(file_path, header=None, names=column_names)

# 使用LabelEncoder将标签编码为数字
label_encoder = LabelEncoder()
data['Sex'] = label_encoder.fit_transform(data['Sex'])

# 提取特征列和标签列
X = data.drop("Sex", axis=1)
y_true = data["Sex"]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y_true, test_size=0.2, random_state=42)

# 设置kmeans分类器的参数范围
param_grid_kmeans = {'n_clusters': [1, 2, 3, 4, 5, 6, 7, 8]}

# 使用GridSearchCV进行交叉验证和参数选择
kmeans_classifier = KMeans()
grid_search_kmeans = GridSearchCV(kmeans_classifier, param_grid_kmeans, cv=5, scoring='accuracy')

# 计算训练时间
start_time_kmeans = time.time()
grid_search_kmeans.fit(X_train, y_train)
training_time_kmeans = time.time() - start_time_kmeans

# 输出最佳参数和交叉验证准确率
print("最佳参数:", grid_search_kmeans.best_params_)
print("交叉验证准确性:", round((grid_search_kmeans.best_score_ * 100), 2), "%")
print("交叉验证的训练时间: {:.4f} seconds".format(training_time_kmeans))

# 在测试集上进行预测
start_time_kmeans = time.time()
y_pred_kmeans = grid_search_kmeans.best_estimator_.predict(X_test)
testing_time_kmeans = time.time() - start_time_kmeans
print("测试时间: {:.4f} seconds".format(testing_time_kmeans))

# 计算准确率
accuracy_kmeans = accuracy_score(y_test, y_pred_kmeans)
print("分类器精度:", round((accuracy_kmeans * 100), 2), "%")

# 计算混淆矩阵
conf_matrix_kmeans = confusion_matrix(y_test, y_pred_kmeans)

# 显示混淆矩阵
disp_kmeans = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_kmeans, display_labels=label_encoder.classes_)
disp_kmeans.plot(cmap='viridis', values_format='d')
plt.title('Confusion Matrix')
plt.show()