# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:28:17 2025

@author: masan
"""

import os
from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")  # 静的ファイルとテンプレートのフォルダを指定
CORS(app)  # CORSを有効化

# ルートアクセス時に index.html を表示
@app.route('/')
def home():
    index_path = os.path.join(app.static_folder, 'index.html')
    if os.path.exists(index_path):
        return send_file(index_path)
    return "Welcome to Street View App<br>This is the home page of the Street View reporting application.<br><a href='/reports'>View Reports</a>"

# favicon.ico を配信
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# 植生報告データを格納するリスト
reports = []

# 植生報告のエンドポイント
@app.route('/report', methods=['POST'])
def report():
    data = request.json
    if not data or 'latitude' not in data or 'longitude' not in data or 'description' not in data:
        return jsonify({"error": "Invalid request"}), 400

    reports.append(data)
    return jsonify({"message": "Report received", "data": data}), 201

# すべての報告を取得し、HTMLの表で表示
@app.route('/reports', methods=['GET'])
def get_reports():
    return render_template("reports.html", reports=reports)

# Render で適切なポートを使用する設定
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # RenderのPORTを取得
    app.run(host='0.0.0.0', port=port, debug=True)
