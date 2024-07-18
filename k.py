import pandas as pd
from sqlalchemy import create_engine

# 엑셀 파일 경로
excel_file_path = "C:/Users/HS/Desktop/quiz_collection.xlsx"

# MySQL 데이터베이스 연결 정보
db_user = 'root'
db_password = '090412'
db_host = 'localhost'  # 일반적으로 'localhost' 또는 원격 서버 IP
db_port = '3306'  # 일반적으로 '3306'
db_name = 'quiz'

# pandas를 사용하여 엑셀 파일 읽기 (열 이름이 없는 경우)
df = pd.read_excel(excel_file_path, header=None)

# 열 이름을 MySQL 테이블의 열 이름과 일치시킴
df.columns = ['id', 'name', 'thumbnail_url']

# SQLAlchemy를 사용하여 MySQL 데이터베이스에 연결
connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)

# 데이터베이스에 데이터프레임 삽입 (table_name은 실제 테이블 이름으로 변경)
table_name = 'quiz_collection'
df.to_sql(table_name, con=engine, if_exists='append', index=False)


print(f"Data has been successfully inserted into the '{table_name}' table in the MySQL database '{db_name}'.")


