#!/usr/bin/env python3
"""
CLI 버전 간단 데모 스크립트
네트워크 없이 로컬에서 작동을 테스트합니다.
"""

from price_analyzer_cli import DataAnalyzer, Visualizer, print_statistics, print_price_list


def demo():
    """데모 데이터를 사용한 시연"""
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  CLI 버전 데모 (샘플 데이터 사용)".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # 샘플 데이터 생성
    sample_prices = [
        15900, 18900, 22000, 25000, 28900,
        32000, 35500, 39900, 42000, 45900,
        49000, 52000, 55900, 59000, 62000
    ]
    
    keyword = "무선마우스 (샘플 데이터)"
    
    # 분석기 및 시각화 도구 생성
    analyzer = DataAnalyzer()
    visualizer = Visualizer()
    
    print("\n🎬 데모를 시작합니다...")
    print(f"검색 키워드: {keyword}")
    
    # 통계 분석
    stats = analyzer.calculate_statistics(sample_prices)
    
    # 결과 출력
    print_statistics(stats, keyword)
    print_price_list(sample_prices, limit=10)
    
    # 히스토그램 생성
    print("\n📊 히스토그램 생성 중...")
    visualizer.save_histogram(sample_prices, keyword, 'demo_histogram.png')
    
    # 결과 저장
    print("\n💾 결과 저장 중...")
    data = {
        'keyword': keyword,
        'prices': sample_prices,
        'statistics': stats
    }
    analyzer.save_results(data, 'demo_result.pkl')
    
    # 결과 불러오기 테스트
    print("\n📂 저장된 결과 불러오기 테스트...")
    loaded = analyzer.load_results('demo_result.pkl')
    
    if loaded:
        print("✅ 모든 기능이 정상적으로 작동합니다!")
    
    print("\n" + "=" * 60)
    print("데모 완료! 생성된 파일:")
    print("  - demo_histogram.png (히스토그램 이미지)")
    print("  - demo_result.pkl (분석 결과 데이터)")
    print("=" * 60)
    print("\n실제 크롤링을 시작하려면:")
    print("  python3 price_analyzer_cli.py")
    print("\n")


if __name__ == "__main__":
    demo()
