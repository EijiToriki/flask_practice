from app import app, db, User, BlogPost

with app.app_context():
  all_posts = BlogPost.query.all()
  print(all_posts)