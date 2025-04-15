# init_db.py
import time
from app.db import get_db_connection  # تأكد أن اسم الملف db.py والوظيفة get_db_connection موجودة

time.sleep(5)  # ننتظر قليلاً حتى تتأكد قاعدة البيانات اشتغلت (مفيد في Docker)

conn = get_db_connection()
cur = conn.cursor()

# إنشاء جدول المستخدمين
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")


# إضافة مستخدم افتراضي
cur.execute(
    "INSERT INTO users (username, password) VALUES (%s, %s) ON CONFLICT DO NOTHING",
    ("admin", "password")
)

conn.commit()
cur.close()
conn.close()

print("✅ Database initialized.")
