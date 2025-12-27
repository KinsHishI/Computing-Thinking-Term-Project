from price_analyzer_cli import DataAnalyzer, print_statistics
import os
import glob


def test_auto_filename():
    """자동 파일명 생성 테스트"""
    print("=" * 60)
    print("자동 파일명 생성 기능 테스트")
    print("=" * 60)
    
    analyzer = DataAnalyzer()
    
    # 테스트 데이터 1
    test_data_1 = {
        'keyword': '무선마우스',
        'prices': [15900, 22000, 28900, 35500, 42000],
        'statistics': {
            'average': 28860,
            'max': 42000,
            'min': 15900,
            'count': 5
        }
    }
    
    # 테스트 데이터 2
    test_data_2 = {
        'keyword': 'USB 메모리',
        'prices': [9900, 12000, 15000, 18000],
        'statistics': {
            'average': 13725,
            'max': 18000,
            'min': 9900,
            'count': 4
        }
    }
    
    # 테스트 데이터 3
    test_data_3 = {
        'keyword': '키보드/마우스 세트!@#',  # 특수문자 포함
        'prices': [35000, 42000, 49000],
        'statistics': {
            'average': 42000,
            'max': 49000,
            'min': 35000,
            'count': 3
        }
    }
    
    print("\n첫 번째 데이터 저장 중...")
    filename1 = analyzer.save_results(test_data_1)
    print(f"저장 완료: {filename1}")
    
    print("\n두 번째 데이터 저장 중...")
    filename2 = analyzer.save_results(test_data_2)
    print(f"저장 완료: {filename2}")
    
    print("\n세 번째 데이터 저장 중 (특수문자 처리)...")
    filename3 = analyzer.save_results(test_data_3)
    print(f"저장 완료: {filename3}")
    
    # 파일 목록 확인
    print("\n" + "=" * 60)
    print("생성된 파일 목록:")
    print("=" * 60)
    pkl_files = sorted(glob.glob('result_*.pkl'), key=os.path.getmtime, reverse=True)
    
    for i, file in enumerate(pkl_files[:5], 1):
        file_size = os.path.getsize(file)
        print(f"{i}. {file} ({file_size} bytes)")
    
    # 파일 불러오기 테스트
    print("\n" + "=" * 60)
    print("파일 불러오기 테스트")
    print("=" * 60)
    
    if pkl_files:
        test_file = pkl_files[0]
        print(f"\n📂 '{test_file}' 불러오는 중...")
        loaded_data = analyzer.load_results(test_file)
        
        if loaded_data:
            keyword = loaded_data.get('keyword', 'Unknown')
            stats = loaded_data.get('statistics', {})
            print_statistics(stats, keyword)
    
    print("\n" + "=" * 60)
    print("테스트 완료!")
    print("=" * 60)
    print("\n주요 기능:")
    print("  • 키워드와 타임스탬프로 고유한 파일명 자동 생성")
    print("  • 특수문자는 자동으로 제거됨")
    print("  • 각 검색 결과가 별도의 파일로 저장되어 덮어쓰기 방지")
    print("  • 파일명 형식: result_[키워드]_[YYYYMMDD_HHMMSS].pkl")
    print("\n🗑️  테스트 파일 정리:")
    print("  rm result_*.pkl")
    print()


if __name__ == "__main__":
    test_auto_filename()
