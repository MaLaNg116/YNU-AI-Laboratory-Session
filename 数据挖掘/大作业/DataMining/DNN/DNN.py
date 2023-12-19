import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, roc_curve, auc
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

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

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_pca, y_true, test_size=0.25, random_state=42)

# 使用PyTorch神经网络进行分类

# 将数据转换为PyTorch张量
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.LongTensor(y_train.values)
X_test_tensor = torch.FloatTensor(X_test)

# 移动数据到GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
X_train_tensor = X_train_tensor.to(device)
y_train_tensor = y_train_tensor.to(device)
X_test_tensor = X_test_tensor.to(device)


# 定义神经网络模型
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, output_size):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, 512)
        self.fc2 = nn.Linear(512, 1024)
        self.fc3 = nn.Linear(1024, 512)
        self.fc4 = nn.Linear(512, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x


# 初始化神经网络模型
input_size = X_train.shape[1]
output_size = len(label_encoder.classes_)
model = NeuralNetwork(input_size, output_size).to(device)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 将数据转换为DataLoader
batch_size = 64
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# 训练神经网络
num_epochs = 60
start_time = time.time()
for epoch in range(num_epochs):
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
training_time = time.time() - start_time
print("Training Time (Neural Network): {:.4f} seconds".format(training_time))

# 在测试集上进行评估
model.eval()
start_time = time.time()
with torch.no_grad():
    outputs = model(X_test_tensor)
    _, predicted = torch.max(outputs, 1)
testing_time = time.time() - start_time
print("Testing Time (Neural Network): {:.4f} seconds".format(testing_time))

# 将预测转换为numpy数组
y_pred_nn = predicted.cpu().numpy()
print(y_pred_nn.tolist())

# 计算准确率
accuracy_nn = accuracy_score(y_test, y_pred_nn)
print("神经网络准确率: {:.2f}%".format(accuracy_nn * 100))

# 计算混淆矩阵
conf_matrix_nn = confusion_matrix(y_test, y_pred_nn)

# 显示混淆矩阵
disp_nn = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_nn, display_labels=label_encoder.classes_)
disp_nn.plot(cmap='viridis', values_format='d')
plt.title('Neural Network Confusion Matrix')
# plt.savefig('NeuralNetworkConfusionMatrix.png')
plt.show()

# 计算训练和测试的计算复杂度（近似值）
training_complexity_nn = input_size * X_train.shape[0]
testing_complexity_nn = input_size * X_test.shape[0]
print("近似训练复杂度（神经网络）: O({})".format(training_complexity_nn))
print("近似测试复杂度（神经网络）: O({})".format(testing_complexity_nn))

# 绘制ROC曲线
y_probs = F.softmax(outputs, dim=1).cpu().numpy()

# 为每个类别计算ROC曲线和AUC值
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(len(label_encoder.classes_)):
    fpr[i], tpr[i], _ = roc_curve(y_test == i, y_probs[:, i])
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
plt.title('Neural Network ROC')
plt.legend(loc="lower right")
# plt.savefig('NeuralNetworkROC.png')
plt.show()
