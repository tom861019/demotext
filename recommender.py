# recommender.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from user_habits import UserHabit
from flask_login import current_user
import os

def get_recommended_images(all_images, similarity_threshold=0.05):  # 移除 limit 參數
    print(f"所有圖片: {all_images}")

    if not current_user.is_authenticated:
        print("未登入，返回所有圖片")
        return all_images
    
    habits = UserHabit.query.filter_by(user_id=current_user.id).all()
    print(f"原始習慣查詢結果: {[(h.image_name, h.click_count) for h in habits]}")

    if not habits:
        print("無習慣記錄，返回所有圖片")
        return all_images

    # 提取點擊歷史並計算權重
    clicked_images = {habit.image_name: habit.click_count for habit in habits}
    print(f"點擊歷史: {clicked_images}")

    # 計算名稱相似性
    clicked_texts = [' '.join(img.split('.')[:-1]) for img in clicked_images.keys()]
    all_image_texts = [' '.join(img.split('.')[:-1]) for img in all_images]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(clicked_texts + all_image_texts)
    clicked_vectors = tfidf_matrix[:len(clicked_texts)]
    all_vectors = tfidf_matrix[len(clicked_texts):]
    similarity_scores = cosine_similarity(clicked_vectors, all_vectors).mean(axis=0)
    print(f"相似性分數: {list(zip(all_images, similarity_scores))}")

    # 計算得分並過濾相關圖片
    image_scores = {}
    for i, image in enumerate(all_images):
        base_score = similarity_scores[i]  # 相似性分數
        click_count = clicked_images.get(image, 0)  # 點擊次數
        score = (click_count * 1.0) + (base_score if base_score >= similarity_threshold else 0)
        image_scores[image] = score  # 保留所有圖片的得分，即使為 0

    # 按得分排序，所有圖片都顯示
    recommended_images = sorted(image_scores.keys(), key=lambda x: image_scores[x], reverse=True)
    print(f"推薦圖片: {recommended_images}")

    return recommended_images

def init_recommender(app):
    pass