from main import SessionLocal, Admin
import bcrypt

db = SessionLocal()
password_hash = bcrypt.hashpw("1234".encode("utf-8"), bcrypt.gensalt())
admin_user = Admin(username="admin", password=password_hash)
db.add(admin_user)
db.commit()
db.close()
print("تم إنشاء مستخدم Admin بنجاح!")
