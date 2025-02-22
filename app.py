# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:28:17 2025

@author: masan
"""


from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# テスト用のルート
@app.route("/")
def home():
    return "ストリートビュー報告アプリへようこそ！"

# 地点報告のエンドポイント
reports = []

@app.route("/report", methods=["POST"])
def report_location():
    data = request.json
    if "lat" in data and "lng" in data and "description" in data:
        reports.append(data)
        return jsonify({"message": "報告が追加されました", "reports": reports}), 201
    return jsonify({"error": "必要な情報が不足しています"}), 400

@app.route("/reports", methods=["GET"])
def get_reports():
    return jsonify({"reports": reports})

# Flaskアプリの起動設定
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

