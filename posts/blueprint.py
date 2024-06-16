from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from .forms import PostForm, PostEditForm
# from app import db

from flask_security import login_required


from models import *

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tag = request.form['tag']

        if title:
            try:
                post = Post(title=title, body=body)

                isTrue = False
                tagSplit = tag.split('*')
                # print(tagSplit)
                allTagName = []
                for i in Tag.query.all():
                    allTagName.append(i.name)
                print(allTagName)
                # for t in range(len(Tag.query.all())):
                #     if str(Tag.query.all()[t].name) in tagSplit:
                #         print('rererere')
                #         post.tags.append(Tag.query.all()[t])
                #         isTrue = True
                #         db.session.add(post)
                #         break
                #
                # if isTrue == False:
                #     # tag = Tag(name=tag.split(','))
                #     for t in range(len(tagSplit)):
                #         newTag = Tag(name=tagSplit[t])
                #         post.tags.append(newTag)
                #         db.session.add(newTag, post)

                for t in range(len(tagSplit)):
                    if tagSplit[t] in allTagName:
                        post.tags.append(Tag.query.filter(Tag.name==tagSplit[t]).first())
                        db.session.add(post)
                    else:
                        newTag = Tag(name=tagSplit[t])
                        post.tags.append(newTag)
                        db.session.add(newTag, post)

                # print(tag)
                # print(post.tags)
                # print(tag)
                db.session.commit()
            except Exception as e:
                print(e)

            return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug==slug).first()
    # print(Post.query.filter(Post.slug==slug).first().exists())

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostEditForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)


@posts.route('/<slug>/delete/', methods=['POST', 'GET'])
@login_required
def delete_post(slug):
    post = Post.query.filter(Post.slug==slug).first()

    try:
        db.session.delete(post)
        db.session.commit()
        print("удаление прошло успешно")
        return redirect(url_for('posts.index'))
    except:
        print('при удаленияя произошла ошибка')



@posts.route('/')
def index():
    # posts = Post.query.all()
    q = request.args.get('q')
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)) #.all()
        # tags = Tag.query.filter(Tag.name.contains(q))
    else:
        posts = Post.query.order_by(Post.created_on.desc())

    pages = posts.paginate(page=page, per_page=5)


    return render_template('posts/index.html', posts=posts, pages=pages)



@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@posts.route('/tags')
def tag_list():
    # posts = Post.query.all()
    q = request.args.get('q')
    page = request.args.get('page')

    tags = Tag.query.all()

    # pages = tags.paginate(page=page, per_page=5)

    return render_template('posts/tag_list.html', tags=tags)


@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts.order_by(Post.created_on.desc())
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)

