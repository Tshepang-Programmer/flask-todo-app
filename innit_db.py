import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

load_dotenv()

def Create_DB():
    try:
        # Connect to default database
        conn = psycopg2.connect(
            database='postgres',  # must connect to existing DB
            host= os.getenv('DB_HOST'),
            user= os.getenv('DB_USER'),
            password= os.getenv('DB_PASSWORD'),
            port= os.getenv('DB_PORT')
        )
        conn.autocommit = True  # required for CREATE DATABASE
        cur = conn.cursor()

        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", ('Flask_Todo',))
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier('Flask_Todo')
            ))
            print("✅ Database Flask_Todo created successfully.")
        else:
            print("ℹ️ Database Flask_Todo already exists.")

    except Exception as e:
        print(f"❌ Error creating database: {e}")

    finally:
        cur.close()
        conn.close()

def db_conn():
    conn = psycopg2.connect(
        database ='Flask_Todo',
        host ="localhost",
        user = 'Tshepang',
        password= 'Testingtesting',
        port ='5432'
     )
    return conn


def create_table():
    try:
        conn= db_conn()
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Todo_list
        (ID serial Primary Key,title Varchar(50), 
         description varchar(200),
         created_at TIMESTAMP DEFAULT NOW(), 
         duration FLOAT,
         is_done BOOLEAN DEFAULT FALSE)
        ''')
        print("✅ table created")
    except Exception as e:
        print(f'❌ Error:{e}')
    finally:
        conn.commit()
        cur.close()
        conn.close()

def insert_data():
    try:
        conn= db_conn()
        cur= conn.cursor()
        cur.execute('''
        INSERT INTO Todo_list(title,description,created_at,duration)
        VALUES ('TESTING','THIS IS ME TESTING HOW THE DATA WILL LOOK','2025-08-23',2)
        ''')
        print('✅Data inserted')
    except Exception as e:
        print(f'❌ error {e}')
    finally:
        conn.commit()
        cur.close()
        conn.close()

while True:
    print('\n __________________________________')
    print(" 1.Create database \n 2. Create Table \nf  3. insert data into table \n 4. Drop table \n If you want to exit press q")
    instruction =input("what would you like to do ? ")
    print('\n __________________________________')
    
    if instruction == "1":
        Create_DB()
    elif instruction == "2":
        create_table()
    elif instruction == "3":
        insert_data()
     # elif instruction == "4":
     #     drop_table()
    elif instruction.lower() == "q":
        break
    else: 
        print("Error option not valid ")


