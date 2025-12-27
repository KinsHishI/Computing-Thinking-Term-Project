"""
Flask 웹 대시보드 - 상품 가격 분석 시스템
브라우저에서 실행되는 웹 인터페이스
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# 프로젝트 모듈 import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from price_analyzer_cli import PriceScraper, DataAnalyzer, Visualizer

app = Flask(__name__)
CORS(app)  # CORS 설정

# 전역 객체
scraper = PriceScraper()
analyzer = DataAnalyzer()
visualizer = Visualizer()


@app.route("/")
def index():
    """메인 페이지"""
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def search():
    """가격 검색 API"""
    try:
        data = request.get_json()
        keyword = data.get("keyword", "").strip()

        if not keyword:
            return (
                jsonify({"success": False, "error": "검색 키워드를 입력해주세요."}),
                400,
            )

        # 가격 수집
        prices = scraper.scrape_prices(keyword)

        if not prices:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "수집된 가격 데이터가 없습니다. 다른 키워드를 시도해보세요.",
                    }
                ),
                404,
            )

        # 통계 분석
        stats = analyzer.calculate_statistics(prices)

        # 히스토그램 데이터 생성 (20개 구간)
        import numpy as np

        hist, bin_edges = np.histogram(prices, bins=20)
        histogram_data = {
            "labels": [f"{int(bin_edges[i]):,}" for i in range(len(bin_edges) - 1)],
            "values": hist.tolist(),
        }

        # 검색 결과 자동 저장
        save_data = {"keyword": keyword, "prices": prices, "statistics": stats}
        saved_filename = analyzer.save_results(save_data)
        print(f"검색 결과 자동 저장: {saved_filename}")

        return jsonify(
            {
                "success": True,
                "keyword": keyword,
                "stats": {
                    "count": stats["count"],
                    "average": round(stats["average"], 0),
                    "max": stats["max"],
                    "min": stats["min"],
                    "range": stats["max"] - stats["min"],
                },
                "prices": prices[:50],  # 상위 50개
                "histogram": histogram_data,
                "saved_filename": saved_filename,  # 저장된 파일명 추가
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": f"오류 발생: {str(e)}"}), 500


@app.route("/api/history")
def get_history():
    """저장된 검색 결과 목록 조회"""
    try:
        import glob
        import os
        from datetime import datetime

        pkl_files = glob.glob("result_*.pkl")
        history = []

        for file in sorted(pkl_files, key=os.path.getmtime, reverse=True)[:10]:
            try:
                data = analyzer.load_results(file)
                if data:
                    mtime = os.path.getmtime(file)
                    history.append(
                        {
                            "filename": file,
                            "keyword": data.get("keyword", "Unknown"),
                            "date": datetime.fromtimestamp(mtime).strftime(
                                "%Y-%m-%d %H:%M"
                            ),
                            "stats": data.get("statistics", {}),
                        }
                    )
            except:
                continue

        return jsonify({"success": True, "history": history})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/save", methods=["POST"])
def save_result():
    """검색 결과 저장"""
    try:
        data = request.get_json()
        keyword = data.get("keyword")
        prices = data.get("prices")
        stats = data.get("stats")

        save_data = {"keyword": keyword, "prices": prices, "statistics": stats}

        filename = analyzer.save_results(save_data)

        return jsonify(
            {
                "success": True,
                "filename": filename,
                "message": f"결과가 {filename}으로 저장되었습니다.",
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/load/<filename>")
def load_result(filename):
    """저장된 결과 불러오기"""
    try:
        data = analyzer.load_results(filename)

        if not data:
            return jsonify({"success": False, "error": "파일을 찾을 수 없습니다."}), 404

        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌐 Flask 웹 대시보드 시작!")
    print("=" * 60)
    print("\n브라우저에서 다음 주소를 열어주세요:")
    print("👉 http://localhost:8080")
    print("\n종료하려면 Ctrl+C를 누르세요.\n")
    print("=" * 60 + "\n")

    app.run(debug=True, host="0.0.0.0", port=8080)
