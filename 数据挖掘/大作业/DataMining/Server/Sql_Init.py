import pymysql
import pandas as pd

# MySQL数据库连接参数
db_params = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'datamining',
    'charset': 'utf8mb4',
}


# SQL语句
create_table_query = """
CREATE TABLE abalone (
    id INT(12) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    Sex VARCHAR(10) NOT NULL,
    Length FLOAT(10) NOT NULL,
    Diameter FLOAT(10) NOT NULL,
    Height FLOAT(10) NOT NULL,
    Whole FLOAT(10) NOT NULL,
    Shucked FLOAT(10) NOT NULL,
    Viscera FLOAT(10) NOT NULL,
    Shell FLOAT(10) NOT NULL,
    Rings INT(10) NOT NULL
)
"""

# 连接到MySQL数据库
connection = pymysql.connect(**db_params)

try:
    # 创建一个数据库游标
    with connection.cursor() as cursor:
        # 执行创建表的SQL语句
        cursor.execute(create_table_query)

    # 提交事务
    connection.commit()

finally:
    # 关闭数据库连接
    connection.close()

# CSV文件路径
csv_file_path = '../data/abalone.csv'

# 读取CSV文件到Pandas DataFrame
df = pd.read_csv(csv_file_path)
print(df)
# 连接到MySQL数据库
connection = pymysql.connect(**db_params)
count = 0

try:
    # 创建一个数据库游标
    with connection.cursor() as cursor:
        # 使用批量插入将数据插入到MySQL表中
        for index, row in df.iterrows():
            try:
                sql = "INSERT INTO abalone (Sex, Length, Diameter, Height, Whole, Shucked, Viscera, Shell, Rings) VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = tuple(row)
                cursor.execute(sql, values)
                count += 1
            except Exception as e:
                print(f"Error inserting row {index + 1}: {e}")

        # 提交事务
        connection.commit()

finally:
    # 关闭数据库连接
    connection.close()