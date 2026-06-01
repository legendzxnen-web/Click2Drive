import pymysql

DB_HOST     = 'localhost'
DB_USER     = 'root'
DB_PASSWORD = ''
DB_NAME     = 'click2drive'

def init():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    cursor.execute(f"USE `{DB_NAME}`;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            first_name  VARCHAR(50)  NOT NULL,
            last_name   VARCHAR(50)  NOT NULL,
            email       VARCHAR(120) NOT NULL UNIQUE,
            password    VARCHAR(255) NOT NULL,
            created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == '__main__':
    init()
