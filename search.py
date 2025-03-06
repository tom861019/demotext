# search.py
from flask import render_template, request
from flask_login import current_user
from recommender import get_recommended_images
import os

def init_search_routes(app):
    IMAGE_DIR = os.path.join(app.static_folder, 'images')

    @app.route('/', methods=['GET', 'POST'])
    def home():
        all_images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('.jpg', '.png'))]
        print(f"讀取的圖片: {all_images}")

        if not all_images:
            return render_template('index.html', images=[], user=current_user, error="圖片目錄中沒有找到任何圖片")

        if request.method == 'POST':
            search_query = request.form['search'].lower()
            images = [img for img in all_images if search_query in img.lower()]
            print(f"搜尋結果: {images}")
        else:
            images = get_recommended_images(all_images, similarity_threshold=0.05)
            print(f"最終顯示的圖片: {images}")
            if not images and current_user.is_authenticated:
                return render_template('index.html', images=[], user=current_user, error="無相關推薦圖片，請嘗試點擊更多圖片")

        return render_template('index.html', images=images, user=current_user)