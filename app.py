# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:28:17 2025

@author: masan
"""


from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# 報告データを保存するファイル
REPORTS_FILE = "reports.json"

# ファイルが存在しない場合は作成
if not os.path.exists(REPORTS_FILE):
    with open(REPORTS_FILE, "w") as f:
        json.dump([], f)


@app.route("/")
def index():
    """メインページを表示"""
    return render_template("index.html")


@app.route("/report", methods=["POST"])
def report():
    """報告データを受け取って保存"""
    try:
        data = request.json
        lat = data.get("lat")
        lon = data.get("lon")
        imageUrl = data.get("imageUrl")
        comment = data.get("comment")

        if not lat or not lon or not comment:
            return jsonify({"error": "すべてのフィールドを入力してください"}), 400

        # データを読み込んでリストに追加
        with open(REPORTS_FILE, "r") as f:
            reports = json.load(f)

        new_report = {"lat": lat, "lon": lon, "imageUrl": imageUrl, "comment": comment}
        reports.append(new_report)

        # ファイルに書き込む
        with open(REPORTS_FILE, "w") as f:
            json.dump(reports, f, indent=4)

        return jsonify({"message": "報告が保存されました", "report": new_report})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/reports", methods=["GET"])
def get_reports():
    """保存された報告データを取得"""
    try:
        with open(REPORTS_FILE, "r") as f:
            reports = json.load(f)
        return jsonify(reports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
