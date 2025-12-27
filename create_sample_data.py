#!/usr/bin/env python3
"""
샘플 검색 결과 생성 스크립트
웹 대시보드 테스트용 샘플 데이터를 생성합니다.
"""

import pickle
import random
from datetime import datetime, timedelta


def create_sample_data(keyword, num_prices=50):
    """샘플 가격 데이터 생성"""
    # 키워드별 가격 범위 설정
    price_ranges = {
        "무선마우스": (15000, 120000),
        "키보드": (25000, 180000),
        "모니터": (150000, 800000),
        "노트북": (500000, 3000000),
        "헤드셋": (20000, 250000),
    }

    # 가격 범위 가져오기 (기본값: 10000~100000)
    min_price, max_price = price_ranges.get(keyword, (10000, 100000))

    # 정규분포를 따르는 가격 데이터 생성
    mean_price = (min_price + max_price) / 2
    std_price = (max_price - min_price) / 4

    prices = []
    for _ in range(num_prices):
        price = int(random.normalvariate(mean_price, std_price))
        # 범위 제한
        price = max(min_price, min(max_price, price))
        prices.append(price)

    # 통계 계산
    stats = {
        "count": len(prices),
        "average": sum(prices) / len(prices),
        "max": max(prices),
        "min": min(prices),
    }

    return {"keyword": keyword, "prices": sorted(prices), "statistics": stats}


def save_sample_file(data, hours_ago=0):
    """샘플 파일 저장 (시간 조정 가능)"""
    keyword = data["keyword"]
    timestamp = datetime.now() - timedelta(hours=hours_ago)
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")

    # 안전한 파일명 생성
    safe_keyword = "".join(
        c for c in keyword if c.isalnum() or c in (" ", "-", "_")
    ).strip()
    safe_keyword = safe_keyword.replace(" ", "_")

    filename = f"result_{safe_keyword}_{timestamp_str}.pkl"

    try:
        with open(filename, "wb") as f:
            pickle.dump(data, f)
        print(f"생성 완료: {filename}")
        return filename
    except Exception as e:
        print(f"저장 실패: {e}")
        return None


def main():
    """샘플 데이터 생성 메인 함수"""
    print("=" * 60)
    print("📊 샘플 검색 결과 생성 스크립트")
    print("=" * 60)
    print()

    # 다양한 시간대의 샘플 데이터 생성
    samples = [
        ("무선마우스", 45, 1),
        ("키보드", 52, 3),
        ("모니터", 38, 6),
        ("노트북", 30, 12),
        ("헤드셋", 41, 24),
    ]

    created_files = []

    for keyword, num_prices, hours_ago in samples:
        print(f"생성 중: {keyword} (가격 {num_prices}개, {hours_ago}시간 전)")
        data = create_sample_data(keyword, num_prices)
        filename = save_sample_file(data, hours_ago)
        if filename:
            created_files.append(filename)
        print()

    print("=" * 60)
    print(f"총 {len(created_files)}개의 샘플 파일 생성 완료!")
    print("=" * 60)
    print()
    print("생성된 파일:")
    for filename in created_files:
        print(f"  - {filename}")
    print()
    print("   http://localhost:8080")
    print()


if __name__ == "__main__":
    main()
