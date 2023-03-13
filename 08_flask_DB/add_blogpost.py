# テーブルに初期データを追加
from app import app, db, BlogPost

with app.app_context():
  # blog_post1 = BlogPost(
  #   title="title1",
  #   text="test1",
  #   featured_image="image1.png",
  #   user_id=1,
  #   summary="summary1"
  # )
  # blog_post2 = BlogPost(
  #   title="title2",
  #   text="test2",
  #   featured_image="image2.png",
  #   user_id=1,
  #   summary="summary2"
  # )
  # blog_post3 = BlogPost(
  #   title="title3",
  #   text="test3",
  #   featured_image="image3.png",
  #   user_id=3,
  #   summary="summary3"
  # )
  # db.session.add_all([blog_post1, blog_post2, blog_post3])


  blog_post4 = BlogPost(
    title="title4",
    text="test4",
    featured_image="image4.png",
    user_id=4,
    summary="summary4"
  )
  db.session.add(blog_post4)

  
  db.session.commit()