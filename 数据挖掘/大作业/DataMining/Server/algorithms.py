import numpy as np
import pandas as pd
import pickle

import torch
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, roc_curve, auc
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import pymysql
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


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


class Algorithms:
    def __init__(self, pca_dim=None):
        # MySQL数据库连接参数
        db_params = {
            'host': 'localhost',
            'user': 'root',
            'password': 'password',
            'database': 'datamining',
            'charset': 'utf8mb4',
        }

        # 连接到MySQL数据库
        connection = pymysql.connect(**db_params)
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT * FROM abalone")
                sql_data = list(cursor.fetchall())
                columns = ['id', 'Sex', 'Length', 'Diameter', 'Height', 'Whole', 'Shucked', 'Viscera', 'Shell', 'Rings']
                self.data = pd.DataFrame(sql_data, columns=columns).drop(['id'], axis=1)

                # 使用LabelEncoder将标签编码为数字
                self.label_encoder = LabelEncoder()
                self.data['Sex'] = self.label_encoder.fit_transform(self.data['Sex'])

                # 提取特征列和标签列
                X = self.data.drop("Sex", axis=1)
                self.y_true = self.data["Sex"]

                # 使用PCA进行降维
                self.pca = PCA(n_components=pca_dim)  # 默认设置为None，表示保留所有主成分
                self.X_pca = self.pca.fit_transform(X)

                # 查看PCA保留的维度
                self.num_components = self.pca.n_components_
                self.explained_variance_ratios = self.pca.explained_variance_ratio_

                # 划分训练集和测试集
                self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X_pca, self.y_true,
                                                                                        test_size=0.25, random_state=42)
            except:
                print("Error: unable to fetch data")
            finally:
                connection.close()

    def naive_bayes(self, from_user=None):
        # 使用朴素贝叶斯分类器（这里使用高斯朴素贝叶斯）
        # 设置预测模式和展示模式
        if from_user is not None:
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))
            # 读取模型参数
            with open('./models/naive_bayes.pkl', 'rb') as f:
                naive_bayes_model = pickle.load(f)
            from_user = self.pca.transform(np.array(from_user).reshape(1, -1))
            user_predict = label[int(naive_bayes_model.best_estimator_.predict(from_user)[0])]
            result = {
                'predict': user_predict
            }

            return result
        else:
            # 设置朴素贝叶斯分类器的参数范围
            param_grid = {'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6,
                                            1e-5, 1e-4, 1e-3, 1e-2, 0.1]}

            # 使用GridSearchCV进行交叉验证和参数选择
            nb_classifier = GaussianNB()
            grid_search = GridSearchCV(nb_classifier, param_grid, cv=5, scoring='accuracy')

            # 计算训练时间
            start_time = time.time()
            grid_search.fit(self.X_train, self.y_train)
            training_time = time.time() - start_time

            # 使用pickle保存模型
            with open('./models/naive_bayes.pkl', 'wb') as f:
                pickle.dump(grid_search, f)

            # 输出最佳参数和交叉验证准确率
            best_params = grid_search.best_params_
            best_score = round((grid_search.best_score_ * 100), 2)

            # 在测试集上进行预测
            start_time = time.time()
            y_pred = grid_search.best_estimator_.predict(self.X_test)
            test_time = time.time() - start_time

            # 计算准确率和混淆矩阵
            accuracy = accuracy_score(self.y_test, y_pred)
            conf_matrix = confusion_matrix(self.y_test, y_pred).tolist()
            conf_matrix = conf_matrix[::-1]
            tmp = []
            for i, sublist in enumerate(conf_matrix):
                # 遍历子列表，获取索引和值
                for j, value in enumerate(sublist):
                    # 将索引和值添加到结果列表中
                    tmp.append([i, j, value])
            conf_matrix = tmp
            conf_matrix_label = [["M", "I", "F"], ["F", "I", "M"]]
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))

            # 绘制ROC曲线
            y_probs = grid_search.best_estimator_.predict_proba(self.X_test)

            # 为每个类别计算ROC曲线和AUC值
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            roc_data = []
            for i in range(len(self.label_encoder.classes_)):
                aoc_tmp = []
                fpr_tmp, tpr_tmp, _ = roc_curve(self.y_test == i, y_probs[:, i])
                fpr[i], tpr[i] = fpr_tmp.tolist(), tpr_tmp.tolist()
                for f, j in zip(fpr[i], tpr[i]):
                    aoc_tmp.append([f, j])
                roc_data.append(aoc_tmp)
                roc_auc[i] = auc(fpr_tmp, tpr_tmp)
            result = {
                'params': param_grid,
                'best_params': best_params,
                'best_score': best_score,
                'num_components': self.num_components,
                'explained_variance_ratios': self.explained_variance_ratios.tolist(),
                'training_time': training_time,
                'test_time': test_time,
                'accuracy': accuracy,
                'label': label,
                'conf_matrix': conf_matrix,
                'conf_matrix_label': conf_matrix_label,
                'roc_data': roc_data,
                'roc_auc': roc_auc
            }

            return result

    def decision_tree(self, from_user=None):
        # 使用决策树分类器
        # 设置预测模式和展示模式
        if from_user is not None:
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))
            # 读取模型参数
            with open('./models/decision_tree.pkl', 'rb') as f:
                decision_tree_model = pickle.load(f)
            from_user = self.pca.transform(np.array(from_user).reshape(1, -1))
            user_predict = label[int(decision_tree_model.best_estimator_.predict(from_user)[0])]
            result = {
                'predict': user_predict
            }

            return result
        else:
            # 设置朴素贝叶斯分类器的参数范围
            param_grid = {'max_depth': [None, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]}

            # 使用GridSearchCV进行交叉验证和参数选择
            dt_classifier = DecisionTreeClassifier()
            grid_search = GridSearchCV(dt_classifier, param_grid, cv=5, scoring='accuracy')

            # 计算训练时间
            start_time = time.time()
            grid_search.fit(self.X_train, self.y_train)
            training_time = time.time() - start_time

            # 使用pickle保存模型
            with open('./models/decision_tree.pkl', 'wb') as f:
                pickle.dump(grid_search, f)

            # 输出最佳参数和交叉验证准确率
            best_params = grid_search.best_params_
            best_score = round((grid_search.best_score_ * 100), 2)

            # 在测试集上进行预测
            start_time = time.time()
            y_pred = grid_search.best_estimator_.predict(self.X_test)
            test_time = time.time() - start_time

            # 计算准确率和混淆矩阵
            accuracy = accuracy_score(self.y_test, y_pred)
            conf_matrix = confusion_matrix(self.y_test, y_pred).tolist()
            conf_matrix = conf_matrix[::-1]
            tmp = []
            for i, sublist in enumerate(conf_matrix):
                # 遍历子列表，获取索引和值
                for j, value in enumerate(sublist):
                    # 将索引和值添加到结果列表中
                    tmp.append([i, j, value])
            conf_matrix = tmp
            conf_matrix_label = [["M", "I", "F"], ["F", "I", "M"]]
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))

            # 绘制ROC曲线
            y_probs = grid_search.best_estimator_.predict_proba(self.X_test)

            # 为每个类别计算ROC曲线和AUC值
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            roc_data = []
            for i in range(len(self.label_encoder.classes_)):
                aoc_tmp = []
                fpr_tmp, tpr_tmp, _ = roc_curve(self.y_test == i, y_probs[:, i])
                fpr[i], tpr[i] = fpr_tmp.tolist(), tpr_tmp.tolist()
                for f, j in zip(fpr[i], tpr[i]):
                    aoc_tmp.append([f, j])
                roc_data.append(aoc_tmp)
                roc_auc[i] = auc(fpr_tmp, tpr_tmp)
            result = {
                'params': param_grid,
                'best_params': best_params,
                'best_score': best_score,
                'num_components': self.num_components,
                'explained_variance_ratios': self.explained_variance_ratios.tolist(),
                'training_time': training_time,
                'test_time': test_time,
                'accuracy': accuracy,
                'label': label,
                'conf_matrix': conf_matrix,
                'conf_matrix_label': conf_matrix_label,
                'roc_data': roc_data,
                'roc_auc': roc_auc
            }

            return result

    def random_forest(self, from_user=None):
        # 使用随机森林分类器
        # 设置预测模式和展示模式
        if from_user is not None:
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))
            # 读取模型参数
            with open('./models/random_forest.pkl', 'rb') as f:
                random_forest_model = pickle.load(f)
            from_user = self.pca.transform(np.array(from_user).reshape(1, -1))
            user_predict = label[int(random_forest_model.best_estimator_.predict(from_user)[0])]
            result = {
                'predict': user_predict
            }
            print(result)
            return result
        else:
            # 设置随机森林分类器的参数范围
            param_grid = {
                'n_estimators': [50, 100, 200, 300],  # 选择不同数量的决策树
                'max_depth': [None, 5, 10, 15]  # 选择不同的最大深度或使用 None 表示不限制深度
            }

            # 使用GridSearchCV进行交叉验证和参数选择
            random_forest = RandomForestClassifier()
            grid_search = GridSearchCV(random_forest, param_grid, cv=5, scoring='accuracy')

            # 计算训练时间
            start_time = time.time()
            grid_search.fit(self.X_train, self.y_train)
            training_time = time.time() - start_time

            # 使用pickle保存模型
            with open('./models/random_forest.pkl', 'wb') as f:
                pickle.dump(grid_search, f)

            # 输出最佳参数和交叉验证准确率
            best_params = grid_search.best_params_
            best_score = round((grid_search.best_score_ * 100), 2)

            # 在测试集上进行预测
            start_time = time.time()
            y_pred = grid_search.best_estimator_.predict(self.X_test)
            test_time = time.time() - start_time

            # 计算准确率和混淆矩阵
            accuracy = accuracy_score(self.y_test, y_pred)
            conf_matrix = confusion_matrix(self.y_test, y_pred).tolist()
            conf_matrix = conf_matrix[::-1]
            tmp = []
            for i, sublist in enumerate(conf_matrix):
                # 遍历子列表，获取索引和值
                for j, value in enumerate(sublist):
                    # 将索引和值添加到结果列表中
                    tmp.append([i, j, value])
            conf_matrix = tmp
            conf_matrix_label = [["M", "I", "F"], ["F", "I", "M"]]
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))

            # 绘制ROC曲线
            y_probs = grid_search.best_estimator_.predict_proba(self.X_test)

            # 为每个类别计算ROC曲线和AUC值
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            roc_data = []
            for i in range(len(self.label_encoder.classes_)):
                aoc_tmp = []
                fpr_tmp, tpr_tmp, _ = roc_curve(self.y_test == i, y_probs[:, i])
                fpr[i], tpr[i] = fpr_tmp.tolist(), tpr_tmp.tolist()
                for f, j in zip(fpr[i], tpr[i]):
                    aoc_tmp.append([f, j])
                roc_data.append(aoc_tmp)
                roc_auc[i] = auc(fpr_tmp, tpr_tmp)
            result = {
                'params': param_grid,
                'best_params': best_params,
                'best_score': best_score,
                'num_components': self.num_components,
                'explained_variance_ratios': self.explained_variance_ratios.tolist(),
                'training_time': training_time,
                'test_time': test_time,
                'accuracy': accuracy,
                'label': label,
                'conf_matrix': conf_matrix,
                'conf_matrix_label': conf_matrix_label,
                'roc_data': roc_data,
                'roc_auc': roc_auc
            }

            return result

    def svm_model(self, from_user=None):
        # 使用SVM分类器(这里采用 OvR 策略)
        # 设置预测模式和展示模式
        if from_user is not None:
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))
            # 读取模型参数
            with open('./models/svm.pkl', 'rb') as f:
                svm_model = pickle.load(f)
            from_user = self.pca.transform(np.array(from_user).reshape(1, -1))
            user_predict = label[int(svm_model.best_estimator_.predict(from_user)[0])]
            result = {
                'predict': user_predict
            }

            return result
        else:
            # 设置SVM分类器的参数范围
            param_grid = {
                'C': [0.1, 1, 10],  # 正则化参数
                'kernel': ['rbf'],  # 核函数的选择
                'gamma': ['scale', 'auto', 0.1, 1],  # 'rbf'和'poly'核的系数
            }

            # 使用GridSearchCV进行交叉验证和参数选择
            svm_classifier = SVC(decision_function_shape='ovr')
            grid_search = GridSearchCV(svm_classifier, param_grid, cv=5, scoring='accuracy')

            # 计算训练时间
            start_time = time.time()
            grid_search.fit(self.X_train, self.y_train)
            training_time = time.time() - start_time

            # 使用pickle保存模型
            with open('./models/svm.pkl', 'wb') as f:
                pickle.dump(grid_search, f)

            # 输出最佳参数和交叉验证准确率
            best_params = grid_search.best_params_
            best_score = round((grid_search.best_score_ * 100), 2)

            # 在测试集上进行预测
            start_time = time.time()
            y_pred = grid_search.best_estimator_.predict(self.X_test)
            test_time = time.time() - start_time

            # 计算准确率和混淆矩阵
            accuracy = accuracy_score(self.y_test, y_pred)
            conf_matrix = confusion_matrix(self.y_test, y_pred).tolist()
            conf_matrix = conf_matrix[::-1]
            tmp = []
            for i, sublist in enumerate(conf_matrix):
                # 遍历子列表，获取索引和值
                for j, value in enumerate(sublist):
                    # 将索引和值添加到结果列表中
                    tmp.append([i, j, value])
            conf_matrix = tmp
            conf_matrix_label = [["M", "I", "F"], ["F", "I", "M"]]
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))

            # 绘制ROC曲线
            y_probs = grid_search.best_estimator_.decision_function(self.X_test)

            # 为每个类别计算ROC曲线和AUC值
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            roc_data = []
            for i in range(len(self.label_encoder.classes_)):
                aoc_tmp = []
                fpr_tmp, tpr_tmp, _ = roc_curve(self.y_test == i, y_probs[:, i])
                fpr[i], tpr[i] = fpr_tmp.tolist(), tpr_tmp.tolist()
                for f, j in zip(fpr[i], tpr[i]):
                    aoc_tmp.append([f, j])
                roc_data.append(aoc_tmp)
                roc_auc[i] = auc(fpr_tmp, tpr_tmp)
            result = {
                'params': param_grid,
                'best_params': best_params,
                'best_score': best_score,
                'num_components': self.num_components,
                'explained_variance_ratios': self.explained_variance_ratios.tolist(),
                'training_time': training_time,
                'test_time': test_time,
                'accuracy': accuracy,
                'label': label,
                'conf_matrix': conf_matrix,
                'conf_matrix_label': conf_matrix_label,
                'roc_data': roc_data,
                'roc_auc': roc_auc
            }

            return result

    def mlp(self, from_user=None):
        # 设置预测模式和展示模式
        if from_user is not None:
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))
            # 读取pytorch模型参数
            model = torch.load('./models/mlp.pth')
            from_user = self.pca.transform(np.array(from_user).reshape(1, -1))
            from_user_tensor = torch.FloatTensor(from_user)
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            from_user_tensor = from_user_tensor.to(device)
            model.eval()
            with torch.no_grad():
                outputs = model(from_user_tensor)
                _, predicted = torch.max(outputs, 1)
            user_predict = label[int(predicted.cpu().numpy()[0])]
            result = {
                'predict': user_predict
            }

            return result
        else:
            # 使用MLP分类器
            X_train_tensor = torch.FloatTensor(self.X_train)
            y_train_tensor = torch.LongTensor(self.y_train.values)
            X_test_tensor = torch.FloatTensor(self.X_test)
            y_test_tensor = torch.FloatTensor(self.y_test.values)

            # 移动数据到GPU
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            X_train_tensor = X_train_tensor.to(device)
            y_train_tensor = y_train_tensor.to(device)
            X_test_tensor = X_test_tensor.to(device)
            y_test_tensor = y_test_tensor.to(device)

            # 初始化神经网络模型
            input_size = self.X_train.shape[1]
            output_size = len(self.label_encoder.classes_)
            model = NeuralNetwork(input_size, output_size).to(device)

            # 定义损失函数和优化器
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters(), lr=0.001)

            # 将数据转换为DataLoader
            batch_size = 100
            train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
            train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

            best_score = 0

            # 训练神经网络
            num_epochs = 60
            start_time = time.time()
            for epoch in range(num_epochs):
                model.train()
                for batch_X, batch_y in train_loader:
                    optimizer.zero_grad()
                    outputs = model(batch_X)
                    loss = criterion(outputs, batch_y)
                    loss.backward()
                    optimizer.step()
                # 在训练集上进行评估
                model.eval()
                with torch.no_grad():
                    outputs = model(X_train_tensor)
                    _, predicted = torch.max(outputs, 1)
                y_pred = predicted.cpu().numpy()
                accuracy = accuracy_score(self.y_train, y_pred)
                if accuracy > best_score:
                    best_score = accuracy
                    torch.save(model, './models/mlp.pth')

            training_time = time.time() - start_time

            # 在测试集上进行评估
            model = torch.load('./models/mlp.pth')
            model.eval()
            start_time = time.time()
            with torch.no_grad():
                outputs = model(X_test_tensor)
                _, predicted = torch.max(outputs, 1)
            test_time = time.time() - start_time

            # 将预测转换为numpy数组
            y_pred = predicted.cpu().numpy()

            # 计算准确率
            accuracy = accuracy_score(self.y_test, y_pred)

            # 计算混淆矩阵
            conf_matrix = confusion_matrix(self.y_test, y_pred)
            conf_matrix = conf_matrix[::-1]
            tmp = []
            for i, sublist in enumerate(conf_matrix):
                # 遍历子列表，获取索引和值
                for j, value in enumerate(sublist):
                    # 将索引和值添加到结果列表中
                    tmp.append([i, j, value])
            conf_matrix = tmp
            conf_matrix_label = [["M", "I", "F"], ["F", "I", "M"]]
            label = dict(zip(range(3), self.label_encoder.inverse_transform(range(3))))

            # 绘制ROC曲线
            y_probs = F.softmax(outputs, dim=1).cpu().numpy()

            # 为每个类别计算ROC曲线和AUC值
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            roc_data = []
            for i in range(len(self.label_encoder.classes_)):
                aoc_tmp = []
                fpr_tmp, tpr_tmp, _ = roc_curve(self.y_test == i, y_probs[:, i])
                fpr[i], tpr[i] = fpr_tmp.tolist(), tpr_tmp.tolist()
                for f, j in zip(fpr[i], tpr[i]):
                    aoc_tmp.append([f, j])
                roc_data.append(aoc_tmp)
                roc_auc[i] = auc(fpr_tmp, tpr_tmp)
            result = {
                'best_score': best_score * 100,
                'num_components': self.num_components,
                'explained_variance_ratios': self.explained_variance_ratios.tolist(),
                'training_time': training_time,
                'test_time': test_time,
                'accuracy': accuracy.tolist(),
                'label': label,
                'conf_matrix': conf_matrix,
                'conf_matrix_label': conf_matrix_label,
                'roc_data': roc_data,
                'roc_auc': roc_auc
            }

            return result
