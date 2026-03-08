import pymysql

# 连接数据库
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root123',
    database='ai_web_gen'
)

try:
    with conn.cursor() as cursor:
        # 检查列是否存在
        cursor.execute("SHOW COLUMNS FROM deployments LIKE 'status'")
        result = cursor.fetchone()

        if not result:
            # 添加列
            cursor.execute("ALTER TABLE deployments ADD COLUMN status VARCHAR(20) DEFAULT 'running'")
            conn.commit()
            print('已添加 status 列')
        else:
            print('status 列已存在')
finally:
    conn.close()