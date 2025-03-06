# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from auth import auth_bp
from user_model import db, init_auth
from search import init_search_routes
from image_detail import init_detail_routes
from user_habits import init_habits
from recommender import init_recommender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # 替換為安全的密鑰
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化資料庫和模組
db.init_app(app)
init_auth(app)
init_search_routes(app)
init_detail_routes(app)
init_habits(app)
init_recommender(app)
app.register_blueprint(auth_bp)

# 在應用啟動時創建資料庫
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)