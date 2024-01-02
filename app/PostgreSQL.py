import psycopg2
import os

class PostgreSQLConnector:
    def __init__(self):
        self.db_url = os.environ.get('DATABASE_URL')
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(self.db_url)
        self.cursor = self.conn.cursor()

    def execute_query(self, sql_query):
        self.cursor.execute(sql_query)

    def fetch_all(self):
        return self.cursor.fetchall()

    def commit_changes(self):
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

"""
# 使用範例
import app.PostgreSQL as PostgreSQL

# 創建 PostgreSQLConnector 實例
pg_connector = PostgreSQL.PostgreSQLConnector()

# 連接到數據庫
pg_connector.connect()

# 執行 SQL 查詢
sql_query = "SELECT * FROM medication_record;"
pg_connector.execute_query(sql_query)

# 獲取查詢結果
result = pg_connector.fetch_all()
print("Query Result:")
print(result)

# 如果需要提交更改，例如插入、更新或删除操作
# pg_connector.commit_changes()

# 關閉連接
pg_connector.close_connection()
"""