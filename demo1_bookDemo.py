from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)


# app的有关配置
# 连接数据库的配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/book_test'
# Set it to True or False to suppress this warning 压制数据库追踪的警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CSRF Token 所需secret key
app.config['SECRET_KEY'] = 'jfslaiunfdnvieep459wewf6safe'


# 实例化数据库连接对象，将app与数据库进行连接
db = SQLAlchemy(app)


class AddBookForm(FlaskForm):
    """图书管理form表单类"""
    author = StringField('作者：', validators=[InputRequired('请输入作者')])
    book = StringField('书名：', validators=[InputRequired('请输入书名')])
    submit = SubmitField('添加')


class Author(db.Model):
    """作者模型，一的一方"""
    # 表名！！！！
    __tablename__ = 'author'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 给Author模型添加关系
    # 定义属性，以便作者模型可以直接通过该属性访问其多的一方的模型的数据（书的模型）
    # backref 给 Book 模型也添加了一个 author 属性，可以通过book.author 获取 book 所对应的作者信息
    books = db.relationship('Book', backref='Author')


class Book(db.Model):
    """书模型多的一方"""

    # 表名！！！
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)

    # 给book模型添加外键
    # 记录一的一方的id作为外键
    author_id = db.Column(db.Integer, db.ForeignKey(Author.id))


@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    try:
        # 查询作者
        author = Author.query.get(author_id)
    except Exception as e:
        print(e)
        return '查询作者失败'

    if not author:
        return '作者不存在'

    # 作者存在,先删书籍,再删除作者
    try:
        # 查询作者相关的图书,并删除
        Book.query.filter(Book.author_id == author_id).delete()

        # 删除作者
        db.session.delete(author)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return '删除作者失败!'

    return redirect(url_for('index'))


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    try:
        # 根据图书id查询图书
        book = Book.query.get(book_id)

    except Exception as e:
        print(e)
        return '查询失败!'
    if not book:
        return '图书不存在!'
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return '删除图书失败!'
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'post'])
def index():

    # form表单对象，并返回给前端
    book_form = AddBookForm()

    # 如果book_form表单可以被提交
    if book_form.validate_on_submit():
        # 1. 取出表单中数据
        # 取值方式一
        author_name = request.form.get('author')
        book_name = request.form.get('book')
        # 取值方式二
        author_name_form = book_form.author.data
        book_name_form = book_form.book.data
        print('方式二取到的 Author name：', author_name_form)
        print('方式二取到的 Book name：', book_name_form)
        # 2. 做具体业务逻辑处理
        # 查询指定名字的作者
        author = Author.query.filter(Author.name == author_name).first()
        # 如果作者不在数据库中
        if not author:
            try:
                # 初始化数据库模型对象
                new_author = Author(name=author_name)
                # 将作者信息添加到数据库的作者表中
                db.session.add(new_author)
                db.session.commit()
                # 添加作者的图书信息
                # 初始化图书信息,并指定其作者
                book = Book(name=book_name, author_id=new_author.id)
                # 将图书指定给特定作者方式二
                # book.author = new_author
                db.session.add(book)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
                flash('添加失败')
        else:
            book = Book.query.filter(Book.name == book_name).first()

            if not book:
                try:
                    # 如果作者已存在,添加作者的图书信息
                    # 初始化图书信息,并指定其作者
                    book = Book(name=book_name, author_id=author.id)
                    db.session.add(book)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    flash('添加失败')
            else:
                # 图书已存在
                flash('图书已存在!')
    else:
        # if request.method == 'post':
        if request.method == 'POST':
            flash("参数错误！")

    # 查询作者所有信息
    authors = Author.query.all()

    # return "Flask BookDemo"
    # 将数据传入到模板中进行渲染返回
    return render_template('book_management.html', authors=authors, form=book_form)


if __name__ == '__main__':
    # 删除所有的表
    db.drop_all()

    # 创建所有的表
    db.create_all()

    # 添加数据， 向数据表中
    # 数据准备
    # 生成作者数据
    au1 = Author(name='老王')
    au2 = Author(name='老尹')
    au3 = Author(name='老刘')
    # 开启与数据库的会话
    db.session.add_all([au1, au2, au3])
    # 将数据提交到数据库相应表中
    db.session.commit()

    # 生成图书数据
    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    db.session.commit()

    app.run(host='192.168.95.131', port=5000, debug=True)
