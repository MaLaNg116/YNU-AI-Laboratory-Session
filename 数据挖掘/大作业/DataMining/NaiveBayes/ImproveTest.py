import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
import time

# 读取数据文件
file_path = "../data/abalone.data"  # 替换为实际文件路径
column_names = ["Sex", "Length", "Diameter", "Height", "Whole weight",
                "Shucked weight", "Viscera weight", "Shell weight", "Rings"]
data = pd.read_csv(file_path, header=None, names=column_names)

# 使用LabelEncoder将标签编码为数字
label_encoder = LabelEncoder()
data['Sex'] = label_encoder.fit_transform(data['Sex'])
data_I = data.copy()
data_MF = data[data['Sex'] != label_encoder.transform(['I'])[0]]

# 将标签为'I'的样本编码为1，不为'I'的样本编码为0
data_I['Sex'] = (data['Sex'] == label_encoder.transform(['I'])[0]).astype(int)
print("lable_encoder: (1, I), (0, M/F)")

# 提取特征列和标签列
X = data.drop("Sex", axis=1)
y_true = data["Sex"]
X_I = data_I.drop("Sex", axis=1)
y_I_true = data_I["Sex"]
X_MF = data_MF.drop("Sex", axis=1)
y_MF_true = data_MF["Sex"]

print("lable_encoder: (2, M), (1, I), (0, F)")

# 使用PCA进行降维
pca = PCA(n_components=None)  # 设置为None，表示保留所有主成分
X_pca = pca.fit_transform(X)

# 查看PCA保留的维度
num_components = pca.n_components_
print("Number of PCA Components:", num_components)
explained_variance_ratios = pca.explained_variance_ratio_
print("Explained Variance Ratios:", explained_variance_ratios)

# 划分训练集和测试集，并确保所有标签为'I'的样本都在训练集中
X_train, X_test, y_train, y_test = train_test_split(X_pca, y_true, test_size=0.2, random_state=42, stratify=y_true)
X_train_I, X_test_I, y_train_I, y_test_I = train_test_split(X_I, y_I_true, test_size=0.2, random_state=42,
                                                            stratify=y_I_true)
X_train_MF, X_test_MF, y_train_MF, y_test_MF = train_test_split(X_MF, y_MF_true, test_size=0.2, random_state=42,
                                                                stratify=y_MF_true)

# 设置朴素贝叶斯分类器的参数范围
param_grid = {'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 0.2, 0.5, 0.8, 1]}

# 定义第一个朴素贝叶斯分类器，用于'I' vs. Rest
classifier_I = GaussianNB()
I_grid_search = GridSearchCV(classifier_I, param_grid, cv=5, scoring='accuracy')

# 在标签为'I'的样本上训练第一个分类器
start_time = time.time()
I_grid_search.fit(X_train_I, y_train_I)
training_time = time.time() - start_time

# 输出最佳参数和交叉验证准确率
print("Best Parameters:", I_grid_search.best_params_)
print("Cross-Validation Accuracy:{:.2f}%".format(round((I_grid_search.best_score_ * 100), 2)))
print("Training Time with Cross-Validation: {:.4f} seconds".format(training_time))

# 在测试集上进行预测
start_time = time.time()
y_pred_I = I_grid_search.best_estimator_.predict(X_test_I)
testing_time = time.time() - start_time
print("Testing Time: {:.4f} seconds".format(testing_time))

# 计算准确率
accuracy_I = accuracy_score(y_test_I, y_pred_I)
print("I分类器准确率:{:.2f}%".format(accuracy_I * 100))

# 定义第二个朴素贝叶斯分类器，用于'M' vs. 'F'
classifier_MF = GaussianNB()
MF_grid_search = GridSearchCV(classifier_MF, param_grid, cv=5, scoring='accuracy')

# 在标签为'MF'的样本上训练第二个分类器
start_time = time.time()
MF_grid_search.fit(X_train_MF, y_train_MF)
training_time2 = time.time() - start_time

# 输出最佳参数和交叉验证准确率
print("Best Parameters:", MF_grid_search.best_params_)
print("Cross-Validation Accuracy:{:.2f}%".format(round((MF_grid_search.best_score_ * 100), 2)))
print("Training Time with Cross-Validation: {:.4f} seconds".format(training_time2))

# 在测试集上进行预测
start_time = time.time()
y_pred_MF = MF_grid_search.best_estimator_.predict(X_test_MF)
testing_time1 = time.time() - start_time
print("Testing Time: {:.4f} seconds".format(testing_time1))

# 计算准确率
accuracy_MF = accuracy_score(y_test_MF, y_pred_MF)
print("MF分类器准确率:{:.2f}%".format(accuracy_MF * 100))


