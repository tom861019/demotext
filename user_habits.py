# user_habits.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from user_model import db

class UserHabit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_name = db.Column(db.String(120), nullable=False)
    click_count = db.Column(db.Integer, default=1)

def init_habits(app):
    pass

def record_habit(image_name):
    if current_user.is_authenticated:
        habit = UserHabit.query.filter_by(user_id=current_user.id, image_name=image_name).first()
        if habit:
            habit.click_count += 1
            print(f"更新點擊次數: {image_name}, 次數: {habit.click_count}")
        else:
            habit = UserHabit(user_id=current_user.id, image_name=image_name)
            db.session.add(habit)
            print(f"新增點擊記錄: {image_name}")
        db.session.commit()