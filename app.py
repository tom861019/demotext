# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import init_routes
from image_handler import init_image_routes
from auth import auth_bp
from user_model import db, init_auth
from search import init_search_routes
from image_detail import init_detail_routes
from user_habits import init_habits
from recommender import init_recommender  # 新增推薦系統模組

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # 請自行替換為安全的密鑰
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化資料庫和模組
db.init_app(app)
init_auth(app)
init_routes(app)
init_image_routes(app)
init_search_routes(app)
init_detail_routes(app)
init_habits(app)
init_recommender(app)  # 新增推薦系統初始化
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 創建資料庫表格
    app.run(debug=True)