from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from company_blog.models import BlogCategory, BlogPost, Inquiry
from company_blog.main.forms import BlogCategoryForm, UpdateCategoryForm, BlogPostForm, BlogSearchForm, InquiryForm
from company_blog import db
from company_blog.main.image_handler import add_featured_image

main = Blueprint('main', __name__)


@main.route('/blog_maintenance', methods=['GET', 'POST'])
@login_required
def blog_maintenance():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    return render_template('blog_maintenance.html', blog_posts=blog_posts)



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
        print(form.category.id)
        if form.picture.data:
            pic = add_featured_image(form.picture.data)
        else:
            pic = ''
        blog_post = BlogPost(title=form.title.data, text=form.text.data, featured_image=pic, user_id=current_user.id, category_id=form.category.data, summary=form.summary.data)
        db.session.add(blog_post)
        db.session.commit()
        flash('ブログ投稿が作成されました')
        return redirect(url_for('main.blog_maintenance'))
    return render_template('create_post.html', form=form)


@main.route('/<int:blog_post_id>/blog_post')
def blog_post(blog_post_id):
    form = BlogSearchForm()
    # ブログ記事の取得
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template(
        'blog_post.html', 
        post=blog_post, 
        recent_blog_posts=recent_blog_posts, 
        blog_categories=blog_categories,
        form=form
    )


@main.route('/<int:blog_post_id>/delete_post', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('ブログ投稿が削除されました')
    return redirect(url_for('main.blog_maintenance'))


@main.route('/<int:blog_post_id>/update_post', methods=['GET', 'POST'])
@login_required
def update_blog_post(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)
    if post.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category_id = form.category.data
        post.summary = form.summary.data
        post.text = form.text.data
        if form.picture.data:
            post.featured_image = add_featured_image(form.picture.data)
        db.session.commit()
        flash('ブログ記事が更新されました')
        return redirect(url_for('main.blog_post', blog_post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category_id
        form.summary.data = post.summary
        form.text.data = post.text
        form.picture.data = post.featured_image
    return render_template('create_post.html', form=form)


@main.route('/')
def index():
    form = BlogSearchForm()
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template(
        'index.html', 
        blog_posts=blog_posts, 
        recent_blog_posts=recent_blog_posts, 
        blog_categories=blog_categories,
        form=form
    )


@main.route('/search', methods=['GET', 'POST'])
def search():
    form = BlogSearchForm()
    searchtext = ""

    if form.validate_on_submit():
        searchtext = form.searchText.data
    elif request.method == 'GET':
        form.searchText.data == ""
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter((BlogPost.text.contains(searchtext)) | (BlogPost.title.contains(searchtext)) | (BlogPost.summary.contains(searchtext))).order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template(
        'index.html', 
        blog_posts=blog_posts, 
        recent_blog_posts=recent_blog_posts, 
        blog_categories=blog_categories,
        form=form,
        search_word=searchtext
    )


@main.route('/<int:blog_category_id>/category_search')
def category_search(blog_category_id):
    form = BlogSearchForm()

    # カテゴリ名の取得
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first_or_404()
    print(blog_category)
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter(BlogPost.category_id==blog_category_id).order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template(
        'index.html', 
        blog_posts=blog_posts, 
        recent_blog_posts=recent_blog_posts, 
        blog_categories=blog_categories,
        form=form,
        blog_category=blog_category
    )

@main.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    form = InquiryForm()

    if form.validate_on_submit():
        inquiry_post = Inquiry(
            name=form.name.data, 
            email=form.email.data, 
            title=form.title.data, 
            text=form.text.data
            )
        db.session.add(inquiry_post)
        db.session.commit()
        flash('お問い合わせが送信されました')
        return redirect(url_for('main.inquiry'))

    return render_template('inquiry.html', form=form)


@main.route('/inquiry_maintenance', methods=['GET', 'POST'])
@login_required
def inquiry_maintenance():
    page = request.args.get('page', 1, type=int)
    inquiry_posts = Inquiry.query.order_by(Inquiry.id.desc()).paginate(page=page, per_page=10)

    return render_template('inquiry_maintenance.html', inquiry_posts=inquiry_posts)


@main.route('/<int:inquiry_id>/display_inquiry')
@login_required
def display_inquiry(inquiry_id):
    form = InquiryForm()
    inquiry = Inquiry.query.get_or_404(inquiry_id)

    form.name.data = inquiry.name
    form.title.data = inquiry.title
    form.email.data = inquiry.email
    form.title.data = inquiry.title
    form.text.data = inquiry.text

    return render_template('inquiry.html', form=form, inquiry_id=inquiry_id)


@main.route('/<int:inquiry_id>/delete_inquiry', methods=['GET', 'POST'])
@login_required
def delete_inquiry(inquiry_id):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    if not current_user.is_administrator():
        abort(403)
    db.session.delete(inquiry)
    db.session.commit()
    flash('お問い合わせが削除されました')
    return redirect(url_for('main.inquiry_maintenance'))
    