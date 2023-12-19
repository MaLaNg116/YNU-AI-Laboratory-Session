import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_curve, auc, confusion_matrix, ConfusionMatrixDisplay
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import time

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
pca = PCA(n_components=None)  # 设置为None，表示保留所有主成分
X_auto = pca.fit_transform(X)

# 查看PCA保留的维度
num_components = pca.n_components_
print("Number of PCA Components:", num_components)
explained_variance_ratios = pca.explained_variance_ratio_
print("Explained Variance Ratios:", explained_variance_ratios)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_auto, y_true, test_size=0.2, random_state=42)

# 初始化SVM分类器
svm_classifier = SVC(decision_function_shape='ovr')  # 'ovr' for one-vs-rest

# 设置参数网格
param_grid = {
    'C': [0.1, 1, 10],  # 正则化参数
    'kernel': ['rbf'],  # 核函数的选择
    'gamma': ['scale', 'auto', 0.1, 1],  # 'rbf'和'poly'核的系数
}

# 初始化GridSearchCV
grid_search = GridSearchCV(estimator=svm_classifier, param_grid=param_grid, cv=5)

# 执行网格搜索和拟合
grid_search.fit(X_auto, y_true)

# 计算训练时间
start_time = time.time()
grid_search.fit(X_train, y_train)
training_time = time.time() - start_time

# 输出最佳参数和交叉验证准确率
print("Best Parameters:", grid_search.best_params_)
print("Cross-Validation Accuracy:", round((grid_search.best_score_ * 100), 2), "%")
print("Training Time with Cross-Validation: {:.4f} seconds".format(training_time))

# 在测试集上进行预测
start_time = time.time()
y_pred = grid_search.best_estimator_.predict(X_test)
testing_time = time.time() - start_time
print("Testing Time: {:.4f} seconds".format(testing_time))

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print("Classifier Accuracy:", round((accuracy * 100), 2), "%")

# 计算混淆矩阵
conf_matrix = confusion_matrix(y_test, y_pred)

# 显示混淆矩阵
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=label_encoder.classes_)
disp.plot(cmap='viridis', values_format='d')
plt.title('Confusion Matrix')
plt.show()

# 计算训练和测试的计算复杂度（近似值）
training_complexity = X_train.shape[1] * X_train.shape[0]
testing_complexity = X_test.shape[1] * X_test.shape[0]
print("Approximate Training Complexity: O({})".format(training_complexity))
print("Approximate Testing Complexity: O({})".format(testing_complexity))

# 使用决策函数计算类别概率
y_scores = grid_search.best_estimator_.decision_function(X_test)

# 为每个类别计算ROC曲线和AUC值
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(len(label_encoder.classes_)):
    fpr[i], tpr[i], _ = roc_curve(y_test == i, y_scores[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# 绘制所有类别的ROC曲线
plt.figure(figsize=(10, 6))
for i in range(len(label_encoder.classes_)):
    plt.plot(fpr[i], tpr[i], label=f'Class {label_encoder.classes_[i]} (AUC = {roc_auc[i]:.2f})')

# 绘制对角线
plt.plot([0, 1], [0, 1], 'k--', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])

# 设置图例
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()

