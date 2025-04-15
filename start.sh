#!/bin/sh

# انتظر قاعدة البيانات
sleep 5

# تهيئة القاعدة
python init_db.py

# تشغيل السيرفر
flask run --host=0.0.0.0
