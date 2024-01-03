import psycopg2
import os

class PostgreSQLConnector:
    def __init__(self):
        self.db_url =  os.environ.get('DATABASE_URL')
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

def create_table():
    # 創建 PostgreSQLConnector 實例
    pg_connector = PostgreSQLConnector()
    # 連接到數據庫
    pg_connector.connect()
    # 定義建立資料表的 SQL 查詢
    create_table_query = """
    CREATE TABLE medication_records (
        record_id BIGSERIAL NOT NULL,
        user_id VARCHAR(50),
        redate DATE,
        pres_hosp VARCHAR(255),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
        updated_at TIMESTAMP WITH TIME ZONE,
        PRIMARY KEY (record_id)
    );
    """

    create_table_2 = """
    CREATE TABLE medication_record_detail (
        detail_id BIGSERIAL NOT NULL,
        record_id BIGINT REFERENCES medication_records(record_id),
        trade_name VARCHAR(255),
        generic_name VARCHAR(255),
        dose_per_unit VARCHAR(255),
        dose_per_time VARCHAR(255),
        dose_per_day VARCHAR(255),
        day_limit VARCHAR(255),
        morning BOOLEAN DEFAULT FALSE,
        noon BOOLEAN DEFAULT FALSE,
        night BOOLEAN DEFAULT FALSE,
        bed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
        updated_at TIMESTAMP WITH TIME ZONE,
        PRIMARY KEY (detail_id),
        FOREIGN KEY (record_id) REFERENCES medication_records(record_id)
    );

"""

    # 執行 SQL 查詢
    pg_connector.execute_query(create_table_query)
    pg_connector.execute_query(create_table_2)
    
    pg_connector.commit_changes()
    # 關閉連接
    pg_connector.close_connection()

def save_record_to_database(user_id, data):
    pg_connector = PostgreSQLConnector()
    # 連接到數據庫
    pg_connector.connect()

    record = data[0]
    print(record)
    create_query = f"INSERT INTO medication_records (user_id , redate,pres_hosp ) VALUES (%s, %s, %s) RETURNING record_id;", (user_id, record['redate'], record['pres_hosp'])
    pg_connector.execute_query(create_query)
    pg_connector.commit_changes()
    # 關閉連接
    pg_connector.close_connection()
    
    inserted_id = pg_connector.fetchone()[0]
    print(inserted_id)
    # # 提交事務
    return inserted_id


def save_record_detail_to_db(record_id, data):
   record = data[1:]
   # 連接到 PostgreSQL 資料庫
   pg_connector = PostgreSQLConnector()
    # 連接到數據庫
   pg_connector.connect()

    
    # 執行插入資料的 SQL 語句
   print(record)
   for each in record:
    create_query = f"INSERT INTO medication_record_detail (record_id,trade_name,generic_name,dose_per_unit,dose_per_time,dose_per_day,day_limit,morning,noon,night, bed ) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s) RETURNING record_id;", (record_id, each["trade_name"], each["generic_name"], each["dose_per_unit"],each["dose_per_time"],each["dose_per_day"],each["day_limit"],each["morning"],each["noon"],each["night"],each["bed"])
    pg_connector.execute_query(create_query)

   # 關閉連接
   pg_connector.commit_changes()
   pg_connector.close_connection()
    
    
 


"""
# 使用範例
db_url = 
# 創建 PostgreSQLConnector 實例
pg_connector = PostgreSQLConnector()
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