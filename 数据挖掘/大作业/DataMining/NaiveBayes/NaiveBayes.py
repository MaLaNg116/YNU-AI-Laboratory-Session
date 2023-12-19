import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_curve, auc
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
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
X_pca = pca.fit_transform(X)

# 查看PCA保留的维度
num_components = pca.n_components_
print("Number of PCA Components:", num_components)
explained_variance_ratios = pca.explained_variance_ratio_
print("Explained Variance Ratios:", explained_variance_ratios)
# 打印各主成分的标签
for i in range(num_components):
    print("PCA Component {} Label: {}".format(i + 1, column_names[i + 1]))


# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_pca, y_true, test_size=0.2, random_state=42)
print("X_test", X_test)
print("y_test", y_test)
# 使用朴素贝叶斯分类器（这里使用高斯朴素贝叶斯）

# 设置朴素贝叶斯分类器的参数范围
param_grid = {'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1]}

# 使用GridSearchCV进行交叉验证和参数选择
nb_classifier = GaussianNB()
grid_search = GridSearchCV(nb_classifier, param_grid, cv=5, scoring='accuracy')

# 计算训练时间
start_time = time.time()
grid_search.fit(X_train, y_train)
training_time = time.time() - start_time

# 输出最佳参数和交叉验证准确率
print("Best Parameters:", grid_search.best_params_)
print("Cross-Validation Accuracy:{:.2f}%".format(round((grid_search.best_score_ * 100), 2)))
print("Training Time with Cross-Validation: {:.4f} seconds".format(training_time))

# 在测试集上进行预测
start_time = time.time()
y_pred = grid_search.best_estimator_.predict(X_test)
testing_time = time.time() - start_time
print("Testing Time: {:.4f} seconds".format(testing_time))

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print("Classifier Accuracy:{:.2f}%".format(accuracy * 100))

# 计算混淆矩阵
conf_matrix = confusion_matrix(y_test, y_pred)
print("confusion_matrix", conf_matrix)

# 显示混淆矩阵
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=label_encoder.classes_)
disp.plot(cmap='viridis', values_format='d')
plt.title('Naive Bayes Confusion Matrix')
# plt.savefig('NaiveBayesConfusionMatrix.png')
plt.show()

# 计算训练和测试的计算复杂度（近似值）
training_complexity = X_train.shape[1] * X_train.shape[0]
testing_complexity = X_test.shape[1] * X_test.shape[0]
print("Approximate Training Complexity: O({})".format(training_complexity))
print("Approximate Testing Complexity: O({})".format(testing_complexity))

# 绘制ROC曲线
y_probs = grid_search.best_estimator_.predict_proba(X_test)

# 为每个类别计算ROC曲线和AUC值
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(len(label_encoder.classes_)):
    fpr[i], tpr[i], _ = roc_curve(y_test == i, y_probs[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
print("roc_auc", roc_auc)
print("fpr", fpr)
print("tpr", tpr)

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
plt.title('Naive Bayes (ROC) Curve')
plt.legend(loc="lower right")
# plt.savefig('NaiveBayesROC.png')
plt.show()