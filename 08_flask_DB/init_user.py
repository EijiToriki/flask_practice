# テーブルに初期データを追加
from app import app, db, User

with app.app_context():
  # 一旦テーブルを空に
  db.drop_all()
  # テーブルの作成
  db.create_all()

  user1 = User("test_user1@test.com", "user1", "111")
  user2 = User("test_user2@test.com", "user2", "222")
  # テーブルに一括でデータを追加
  db.session.add_all([user1, user2])
  # テーブルに1つずつデータを追加
  # db.session.add(user1)
  # db.session.add(user2)

  db.session.commit()

  print(user1.id)
  print(user2.id)