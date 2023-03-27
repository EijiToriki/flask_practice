from company_blog import db
from company_blog.models import BlogCategory

# db.drop_all()
# db.create_all()

for i in range(1, 81):
    c1 = BlogCategory(category=f'category{i}') 
    db.session.add(c1)
    db.session.commit()
