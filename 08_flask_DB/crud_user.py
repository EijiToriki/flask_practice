# crud = create, read, update, drop
from app import app, db, User

with app.app_context():
  ## ユーザ追加例
  user3 = User("test_user3@test.com", "user3", "333")
  db.session.add(user3)
  db.session.commit()

  ## 全レコードの取得
  all_users = User.query.all()
  print(all_users)

  ## レコードの取得（ID指定)
  userid_1 = User.query.get(1)
  print(userid_1)

  # レコードの取得(フィルタによる条件指定)
  username_user2 = User.query.filter_by(username="user2")
  print(username_user2.all())

  # レコードの更新
  userid_1 = User.query.get(1)
  userid_1.username ="Test UserA"
  db.session.add(userid_1)
  db.session.commit()

  # レコードの削除
  userid_2 = User.query.get(2)
  db.session.delete(userid_2)
  db.session.commit()

  # 全レコードの取得
  all_users = User.query.all()
  print(all_users)