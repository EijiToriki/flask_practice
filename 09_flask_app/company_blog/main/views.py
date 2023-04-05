from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from company_blog.models import BlogCategory, BlogPost
from company_blog.main.forms import BlogCategoryForm, UpdateCategoryForm, BlogPostForm
from company_blog import db
from company_blog.main.image_handler import add_featured_image

main = Blueprint('main', __name__)

@main.route('/category_maintenance', methods=['GET', 'POST'])
@login_required
def category_maintenance():
    page = request.args.get('page', 1, type=int)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).paginate(page=page, per_page=10)
    form = BlogCategoryForm()
    if form.validate_on_submit():
        blog_category = BlogCategory(category=form.category.data)
        db.session.add(blog_category)
        db.session.commit()
        flash('ブログカテゴリが追加されました。')
        return redirect(url_for('main.category_maintenance'))
    elif form.errors:
        form.category.data = ""
        flash(form.errors['category'][0])

    return render_template('category_maintenance.html', blog_categories=blog_categories, form=form)


@main.route('/<int:category_id>/update_category', methods=['GET', 'POST'])
@login_required
def update_category(category_id):
    category = BlogCategory.query.get_or_404(category_id)
    if not current_user.is_administrator():
        abort(403)
    form = UpdateCategoryForm(category_id)
    if form.validate_on_submit():
        category.category = form.category.data
        db.session.commit()
        flash('カテゴリ名が更新されました')
        return redirect(url_for('main.category_maintenance'))
    elif request.method == 'GET':
        form.category.data = category.category
    return render_template('category_update.html', form=form)


@main.route('/<int:category_id>/delete_category', methods=['GET', 'POST'])
@login_required
def delete_category(category_id):
    category = BlogCategory.query.get_or_404(category_id)
    if not current_user.is_administrator():
        abort(403)
    db.session.delete(category)
    db.session.commit()
    flash('カテゴリが削除されました')
    return redirect(url_for('main.category_maintenance'))


@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        if form.picuture.data:
            pic = add_featured_image(form.picuture.data)
        else:
            pic = ''
        blog_post = BlogPost(title=form.title.data, text=form.text.data, featured_image=pic, user_id=current_user.id, category_id=form.category.id, summary=form.summary.data)
        db.session.add(blog_post)
        db.session.commit()
        flash('ブログ投稿が作成されました')
        return redirect(url_for('main.category_maintenance'))
    return render_template('create_post.html', form=form)
