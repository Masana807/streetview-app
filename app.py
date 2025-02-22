# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:28:17 2025

@author: masan
"""


import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORSを有効化

# テスト用のルート
@app.route('/')
def home():
    return "Street View App is running!"

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

# すべての報告を取得
@app.route('/reports', methods=['GET'])
def get_reports():
    return jsonify(reports)

# Render で適切なポートを使用する設定
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # 環境変数 PORT を取得（デフォルト 5000）
    app.run(host='0.0.0.0', port=port, debug=True)
