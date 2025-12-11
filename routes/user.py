from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/')
def list():
    users = User.select()
    return render_template('user_list.html', title='ユーザー一覧', items=users)

@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])

        category = User.judge_category(age)

        User.create(name=name, age=age, category=category)
        return redirect(url_for('user.list'))

    return render_template('user_add.html')

@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.age = int(request.form['age'])
        user.category = User.judge_category(user.age)
        user.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)
