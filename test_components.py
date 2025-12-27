from price_analyzer import PriceScraper, DataAnalyzer, Visualizer


def test_scraper():
    """PriceScraper 클래스 테스트"""
    print("=" * 60)
    print("1. PriceScraper 테스트")
    print("=" * 60)
    
    scraper = PriceScraper()
    
    try:
        print("키워드 '무선마우스'로 가격 수집 중...")
        prices = scraper.scrape_prices("무선마우스")
        
        print(f"수집 성공: {len(prices)}개의 가격 데이터")
        if prices:
            print(f"   샘플 데이터: {prices[:5]}")
        else:
            print("수집된 데이터가 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    
    print()


def test_analyzer():
    """DataAnalyzer 클래스 테스트"""
    print("=" * 60)
    print("2. DataAnalyzer 테스트")
    print("=" * 60)
    
    # 테스트 데이터
    test_prices = [10000, 15000, 20000, 25000, 30000, 35000, 40000]
    
    analyzer = DataAnalyzer()
    stats = analyzer.calculate_statistics(test_prices)
    
    print("테스트 데이터:", test_prices)
    print(f"통계 계산 결과:")
    print(f"   평균: {stats['average']:,.0f}원")
    print(f"   최대: {stats['max']:,}원")
    print(f"   최소: {stats['min']:,}원")
    print(f"   개수: {stats['count']}개")
    
    # 파일 저장/불러오기 테스트
    try:
        test_data = {
            'keyword': 'test',
            'prices': test_prices,
            'statistics': stats
        }
        analyzer.save_results(test_data, 'test_result.pkl')
        print("파일 저장 성공: test_result.pkl")
        
        loaded_data = analyzer.load_results('test_result.pkl')
        if loaded_data:
            print("파일 불러오기 성공")
            print(f"   불러온 키워드: {loaded_data['keyword']}")
    except Exception as e:
        print(f"파일 I/O 오류: {e}")
    
    print()


def test_visualizer():
    """Visualizer 클래스 테스트"""
    print("=" * 60)
    print("3. Visualizer 테스트")
    print("=" * 60)
    
    # 테스트 데이터 (정규 분포 형태)
    import random
    test_prices = [int(random.gauss(50000, 15000)) for _ in range(100)]
    test_prices = [p for p in test_prices if 10000 <= p <= 100000]
    
    visualizer = Visualizer()
    
    try:
        print(f"테스트 데이터: {len(test_prices)}개")
        print("히스토그램 생성 중...")
        visualizer.plot_histogram(test_prices, "테스트 상품")
        print("✅ 히스토그램 생성 완료 (창을 닫으면 계속됩니다)")
    except Exception as e:
        print(f"시각화 오류: {e}")
    
    print()


def test_integration():
    """통합 테스트"""
    print("=" * 60)
    print("4. 통합 테스트")
    print("=" * 60)
    
    scraper = PriceScraper()
    analyzer = DataAnalyzer()
    visualizer = Visualizer()
    
    keyword = "USB"
    
    try:
        print(f"키워드 '{keyword}'로 전체 프로세스 테스트 중...")
        
        # 1. 크롤링
        print("  [1/3] 데이터 수집 중...")
        prices = scraper.scrape_prices(keyword)
        
        if not prices:
            print("수집된 데이터가 없어 테스트를 종료합니다.")
            return
        
        print(f"{len(prices)}개 수집 완료")
        
        # 2. 분석
        print("  [2/3] 통계 분석 중...")
        stats = analyzer.calculate_statistics(prices)
        print(f"평균: {stats['average']:,.0f}원, 범위: {stats['min']:,}~{stats['max']:,}원")
        
        # 3. 저장
        print("  [3/3] 결과 저장 중...")
        data = {
            'keyword': keyword,
            'prices': prices,
            'statistics': stats
        }
        analyzer.save_results(data, 'integration_test.pkl')
        print("저장 완료: integration_test.pkl")
        
        print("\n통합 테스트 성공!")
        
    except Exception as e:
        print(f"통합 테스트 실패: {e}")
    
    print()


def main():
    """메인 테스트 실행"""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   가격 분석 시스템 컴포넌트 테스트                             ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    # 각 컴포넌트 테스트
    test_analyzer()  # 네트워크 없이 가능한 테스트 먼저
    
    # 사용자 선택
    print("=" * 60)
    print("네트워크 관련 테스트를 진행하시겠습니까?")
    print("크롤링 테스트는 실제 웹사이트에 요청을 보냅니다.")
    choice = input("진행하시려면 'y'를 입력하세요 (y/n): ").lower()
    
    if choice == 'y':
        test_scraper()
        test_integration()
        
        # 시각화 테스트
        viz_choice = input("\n히스토그램 테스트를 진행하시겠습니까? (y/n): ").lower()
        if viz_choice == 'y':
            test_visualizer()
    
    print("=" * 60)
    print("테스트 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
