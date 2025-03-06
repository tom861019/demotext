# image_detail.py
from flask import render_template, abort
from flask_login import current_user
from user_habits import record_habit
import os

def init_detail_routes(app):
    IMAGE_DIR = os.path.join(app.static_folder, 'images')

    @app.route('/image/<image_name>')
    def image_detail(image_name):
        if image_name in os.listdir(IMAGE_DIR) and image_name.endswith(('.jpg', '.png')):
            print(f"進入詳細頁面: {image_name}")
            record_habit(image_name)
            return render_template('detail.html', image_name=image_name, user=current_user)
        else:
            abort(404)