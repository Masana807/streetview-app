# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:28:17 2025

@author: masan
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder="static")  # static フォルダを設定
CORS(app)  # CORSを有効化

REPORTS_FILE = "reports.json"

# 📌 ファイルから報告データを読み込む
def load_reports():
    if os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 📌 ファイルに報告データを保存する
def save_reports(reports):
    with open(REPORTS_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2, ensure_ascii=False)  # UTF-8で保存

# 📌 初期データをロード
reports = load_reports()

# ルートアクセス時に index.html を表示
@app.route('/')
def home():
    index_path = os.path.join(app.static_folder, 'index.html')
    if os.path.exists(index_path):
        return send_file(index_path)
    return "Street View App is running!"

# favicon.ico を配信
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# 📌 植生報告のエンドポイント（POST）
@app.route('/report', methods=['POST'])
def report():
    global reports
    data = request.json
    if not data or 'latitude' not in data or 'longitude' not in data or 'description' not in data:
        return jsonify({"error": "Invalid request"}), 400

    reports.append(data)
    save_reports(reports)  # 📌 追加後に保存
    return jsonify({"message": "Report received", "data": data}, ensure_ascii=False), 201  # 文字化け対策

# 📌 すべての報告を取得（GET）
@app.route('/reports', methods=['GET'])
def get_reports():
    return jsonify(reports), 200  # 文字化け対策

# 📌 Render で適切なポートを使用する設定
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # RenderのPORTを取得
    app.run(host='0.0.0.0', port=port, debug=True)
