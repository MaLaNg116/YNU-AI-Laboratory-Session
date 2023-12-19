from flask import Flask, jsonify, request
from algorithms import Algorithms
from flask_cors import CORS
import numpy as np
import pymysql
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

app = Flask(__name__)

CORS(app, resources=r'/*')

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


@app.route('/GetData', methods=['GET'])
def get_data():
    try:
        # 创建一个数据库游标
        with connection.cursor() as cursor:
            # 执行创建表的SQL语句
            cursor.execute("SELECT * FROM abalone")
            keys = ["id", "sex", "length", "diameter", "height", "whole", "shucked", "viscera", "shell", "rings"]
            data = list(cursor.fetchall())
            data = [dict(zip(keys, d)) for d in data]
            response = {
                'code': 200,
                'msg': 'success',
                'data': data
            }
            return jsonify(response), 200
    except:
        response = {
            'code': 500,
            'msg': 'error',
            'data': None
        }
        return jsonify(response), 500


@app.route('/GetNaiveBayes/<pca_dim>', methods=['GET', 'POST'])
def get_naive_bayes(pca_dim):
    if request.method == 'GET':
        if pca_dim == 'None':
            pca_dim = None
        elif int(pca_dim) <= 0 or int(pca_dim) > 8:
            response = {
                'code': 400,
                'msg': 'pca_dim must be a integer in range [1, 8]',
                'data': None
            }
            return jsonify(response), 400
        try:
            data = Algorithms(pca_dim=int(pca_dim) if pca_dim is not None else None).naive_bayes()
            response = {
                'code': 200,
                'msg': 'success',
                'data': data
            }
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    elif request.method == 'POST':
        from_user = request.get_json()
        print(from_user)
        if from_user is None or len(from_user) < int(pca_dim):
            response = {
                'code': 400,
                'msg': 'data is invalid',
                'data': None
            }
            return jsonify(response), 400
        try:
            predict = Algorithms().naive_bayes(from_user)
            response = {
                'code': 200,
                'msg': 'success',
                'data': predict
            }
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    else:
        response = {
            'code': 405,
            'msg': 'method not allowed',
            'data': None
        }
        return jsonify(response), 405


@app.route('/GetDecisionTree/<pca_dim>', methods=['GET', 'POST'])
def get_decision_tree(pca_dim):
    if request.method == 'GET':
        if pca_dim == 'None':
            pca_dim = None
        elif int(pca_dim) <= 0 or int(pca_dim) > 8:
            response = {
                'code': 400,
                'msg': 'pca_dim must be a integer in range [1, 8]',
                'data': None
            }
            return jsonify(response), 400
        try:
            data = Algorithms(pca_dim=int(pca_dim) if pca_dim is not None else None).decision_tree()
            response = {
                'code': 200,
                'msg': 'success',
                'data': data
            }
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    elif request.method == 'POST':
        from_user = request.get_json()
        print(from_user)
        if from_user is None or len(from_user) < int(pca_dim):
            response = {
                'code': 400,
                'msg': 'data is invalid',
                'data': None
            }
            return jsonify(response), 400
        try:
            predict = Algorithms().decision_tree(from_user)
            response = {
                'code': 200,
                'msg': 'success',
                'data': predict
            }
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    else:
        response = {
            'code': 405,
            'msg': 'method not allowed',
            'data': None
        }
        return jsonify(response), 405


@app.route('/GetRandomForest/<pca_dim>', methods=['GET', 'POST'])
def get_random_forest(pca_dim):
    if request.method == 'GET':
        if pca_dim == 'None':
            pca_dim = None
        elif int(pca_dim) <= 0 or int(pca_dim) > 8:
            response = {
                'code': 400,
                'msg': 'pca_dim must be a integer in range [1, 8]',
                'data': None
            }
            return jsonify(response), 400
        try:
            data = Algorithms(pca_dim=int(pca_dim) if pca_dim is not None else None).random_forest()
            response = {
                'code': 200,
                'msg': 'success',
                'data': data
            }
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    elif request.method == 'POST':
        from_user = request.get_json()
        print(from_user)
        if from_user is None or len(from_user) < int(pca_dim):
            response = {
                'code': 400,
                'msg': 'data is invalid',
                'data': None
            }
            return jsonify(response), 400
        try:
            predict = Algorithms().random_forest(from_user)
            response = {
                'code': 200,
                'msg': 'success',
                'data': predict
            }
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    else:
        response = {
            'code': 405,
            'msg': 'method not allowed',
            'data': None
        }
        return jsonify(response), 405


@app.route('/GetSVM/<pca_dim>', methods=['GET', 'POST'])
def get_svm(pca_dim):
    if request.method == 'GET':
        if pca_dim == 'None':
            pca_dim = None
        elif int(pca_dim) <= 0 or int(pca_dim) > 8:
            response = {
                'code': 400,
                'msg': 'pca_dim must be a integer in range [1, 8]',
                'data': None
            }
            return jsonify(response), 400
        try:
            data = Algorithms(pca_dim=int(pca_dim) if pca_dim is not None else None).svm_model()
            response = {
                'code': 200,
                'msg': 'success',
                'data': data
            }
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    elif request.method == 'POST':
        from_user = request.get_json()
        print(from_user)
        if from_user is None or len(from_user) < int(pca_dim):
            response = {
                'code': 400,
                'msg': 'data is invalid',
                'data': None
            }
            return jsonify(response), 400
        try:
            predict = Algorithms().svm_model(from_user)
            response = {
                'code': 200,
                'msg': 'success',
                'data': predict
            }
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    else:
        response = {
            'code': 405,
            'msg': 'method not allowed',
            'data': None
        }
        return jsonify(response), 405


@app.route('/GetMLP/<pca_dim>', methods=['GET', 'POST'])
def get_mlp(pca_dim):
    if request.method == 'GET':
        if pca_dim == 'None':
            pca_dim = None
        elif int(pca_dim) <= 0 or int(pca_dim) > 8:
            response = {
                'code': 400,
                'msg': 'pca_dim must be a integer in range [1, 8]',
                'data': None
            }
            return jsonify(response), 400
        try:
            data = Algorithms(pca_dim=int(pca_dim) if pca_dim is not None else None).mlp()
            response = {
                'code': 200,
                'msg': 'success',
                'data': data
            }
            # 解决int64无法序列化的问题
            response = json.loads(json.dumps(response, cls=NpEncoder))
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    elif request.method == 'POST':
        from_user = request.get_json()
        print(from_user)
        if from_user is None or len(from_user) < int(pca_dim):
            response = {
                'code': 400,
                'msg': 'data is invalid',
                'data': None
            }
            return jsonify(response), 400
        try:
            predict = Algorithms().mlp(from_user)
            response = {
                'code': 200,
                'msg': 'success',
                'data': predict
            }
            return jsonify(response), 200
        except Exception as e:
            print(e)
            response = {
                'code': 500,
                'msg': 'error',
                'data': None
            }
            return jsonify(response), 500
    else:
        response = {
            'code': 405,
            'msg': 'method not allowed',
            'data': None
        }
        return jsonify(response), 405


if __name__ == '__main__':
    app.run(port=5000, debug=False)
