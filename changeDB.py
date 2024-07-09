import pandas as pd
import mysql.connector

# 连接到 MySQL 数据库
db_connection = mysql.connector.connect(
    host="172.24.247.83",
    user="zhangzhe",
    password="ZZhe!197",
    database="ProjectM"
)

# 读取 CSV 文件
df = pd.read_csv('./data/就业率.csv')

# 获取数据库游标
cursor = db_connection.cursor()

# 遍历 CSV 文件中的每一行，并更新表中对应的记录
for index, row in df.iterrows():
    sql = "UPDATE major_info SET  major_courses = %s WHERE major_name = %s"
    val = (row['专业课程'] ,row['专业名称'])
    cursor.execute(sql, val)

# 提交更改并关闭连接
db_connection.commit()
cursor.close()
db_connection.close()

print("更新完成")
