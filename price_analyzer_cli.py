import requests
from bs4 import BeautifulSoup
import re
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 사용하지 않음
import matplotlib.pyplot as plt
import pickle
from typing import List, Dict, Optional
import os


class PriceScraper:
    """다나와 웹사이트에서 가격 데이터를 크롤링하는 클래스"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = "http://search.danawa.com/dsearch.php"
        self.min_price = 1000
        self.max_price = 100000000
    
    def scrape_prices(self, keyword: str) -> List[int]:
        """
        특정 키워드로 다나와를 검색하고 가격 데이터를 수집합니다.
        
        Args:
            keyword: 검색할 상품 키워드
            
        Returns:
            수집된 가격 리스트 (정수형)
        """
        prices = []
        
        try:
            print(f"\n🔍 '{keyword}' 검색 중...")
            
            # 검색 요청
            params = {
                'query': keyword,
                'tab': 'goods'
            }
            
            response = requests.get(
                self.base_url, 
                params=params, 
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 가격 데이터 추출 (정규표현식 사용)
            price_pattern = r"(\d[\d,]*)\s*원"
            text_content = soup.get_text()
            
            # 모든 가격 패턴 찾기
            matches = re.findall(price_pattern, text_content)
            
            # 리스트 함축을 사용한 데이터 정제
            prices = [
                int(match.replace(',', ''))
                for match in matches
                if self._is_valid_price(match)
            ]
            
            # 중복 제거 및 정렬
            prices = sorted(list(set(prices)))
            
            print(f"✅ {len(prices)}개의 가격 데이터 수집 완료")
            
        except requests.exceptions.RequestException as e:
            print(f"네트워크 오류: {e}")
            raise Exception(f"크롤링 중 네트워크 오류가 발생했습니다: {str(e)}")
        except Exception as e:
            print(f"데이터 파싱 오류: {e}")
            raise Exception(f"데이터 파싱 중 오류가 발생했습니다: {str(e)}")
        
        return prices
    
    def _is_valid_price(self, price_str: str) -> bool:
        """
        가격이 유효한 범위 내에 있는지 확인합니다.
        
        Args:
            price_str: 쉼표가 포함된 가격 문자열
            
        Returns:
            유효 여부
        """
        try:
            price = int(price_str.replace(',', ''))
            return self.min_price <= price <= self.max_price
        except ValueError:
            return False


class DataAnalyzer:
    """가격 데이터의 통계 분석을 수행하는 클래스"""
    
    @staticmethod
    def calculate_statistics(prices: List[int]) -> Dict[str, float]:
        """
        가격 리스트의 통계를 계산합니다.
        
        Args:
            prices: 가격 데이터 리스트
            
        Returns:
            통계 정보 딕셔너리 (평균, 최대, 최소, 개수)
        """
        if not prices:
            return {
                'average': 0,
                'max': 0,
                'min': 0,
                'count': 0
            }
        
        return {
            'average': sum(prices) / len(prices),
            'max': max(prices),
            'min': min(prices),
            'count': len(prices)
        }
    
    @staticmethod
    def save_results(data: Dict, filename: str = None):
        """
        분석 결과를 pickle 파일로 저장합니다.
        
        Args:
            data: 저장할 데이터
            filename: 저장할 파일명 (None이면 자동 생성)
        """
        try:
            # 파일명이 지정되지 않은 경우 자동 생성
            if filename is None:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                keyword = data.get('keyword', 'unknown')
                # 파일명에 사용할 수 없는 문자 제거
                safe_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '_')).strip()
                safe_keyword = safe_keyword.replace(' ', '_')[:20]  # 최대 20자로 제한
                filename = f'result_{safe_keyword}_{timestamp}.pkl'
            
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
            print(f"결과 저장 완료: {filename}")
            
            return filename  # 저장된 파일명 반환
        except Exception as e:
            print(f"파일 저장 오류: {e}")
            raise
    
    @staticmethod
    def load_results(filename: str = 'last_result.pkl') -> Optional[Dict]:
        """
        pickle 파일에서 분석 결과를 불러옵니다.
        
        Args:
            filename: 불러올 파일명
            
        Returns:
            저장된 데이터 또는 None
        """
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
            print(f"결과 불러오기 완료: {filename}")
            return data
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {filename}")
            return None
        except Exception as e:
            print(f"파일 불러오기 오류: {e}")
            return None


class Visualizer:
    """데이터 시각화를 담당하는 클래스"""
    
    def __init__(self):
        self._setup_korean_font()
    
    def _setup_korean_font(self):
        """한글 깨짐 방지를 위한 폰트 설정"""
        try:
            # macOS용 한글 폰트 설정
            plt.rcParams['font.family'] = 'AppleGothic'
            plt.rcParams['axes.unicode_minus'] = False
        except:
            try:
                # Windows용 한글 폰트 설정
                plt.rcParams['font.family'] = 'Malgun Gothic'
                plt.rcParams['axes.unicode_minus'] = False
            except:
                print("⚠️  한글 폰트 설정 실패. 기본 폰트를 사용합니다.")
    
    def save_histogram(self, prices: List[int], keyword: str, filename: str = 'price_histogram.png'):
        """
        가격 분포 히스토그램을 파일로 저장합니다.
        
        Args:
            prices: 가격 데이터 리스트
            keyword: 검색 키워드
            filename: 저장할 파일명
        """
        if not prices:
            print("시각화할 데이터가 없습니다.")
            return
        
        try:
            plt.figure(figsize=(10, 6))
            
            # 히스토그램 생성
            plt.hist(prices, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
            
            # 차트 설정
            plt.title(f'Price Distribution - {keyword}', fontsize=16, fontweight='bold')
            plt.xlabel('가격 (원)', fontsize=12)
            plt.ylabel('빈도', fontsize=12)
            plt.grid(axis='y', alpha=0.3)
            
            # 통계선 추가
            avg_price = sum(prices) / len(prices)
            plt.axvline(avg_price, color='red', linestyle='--', linewidth=2, label=f'평균: {avg_price:,.0f}원')
            plt.legend()
            
            # 가격 포맷팅
            ax = plt.gca()
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
            
            plt.tight_layout()
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"히스토그램 저장 완료: {filename}")
            
        except Exception as e:
            print(f"시각화 오류: {e}")


def print_statistics(stats: Dict, keyword: str):
    """통계 결과를 출력합니다."""
    print("\n" + "=" * 60)
    print(f"📊 {keyword} - 가격 분석 결과")
    print("=" * 60)
    print(f"수집된 가격 개수: {stats['count']:,}개")
    print(f"평균 가격:       {stats['average']:>15,.0f}원")
    print(f"최고 가격:       {stats['max']:>15,}원")
    print(f"최저 가격:       {stats['min']:>15,}원")
    print(f"가격 범위:       {stats['max'] - stats['min']:>15,}원")
    print("=" * 60)


def print_price_list(prices: List[int], limit: int = 10):
    """가격 리스트를 출력합니다."""
    print(f"\n💰 수집된 가격 목록 (상위 {min(limit, len(prices))}개):")
    print("-" * 60)
    for i, price in enumerate(prices[:limit], 1):
        print(f"{i:2d}. {price:>15,}원")
    
    if len(prices) > limit:
        print(f"... 외 {len(prices) - limit}개")


def interactive_mode():
    """대화형 모드로 프로그램을 실행합니다."""
    print("\n" + "╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  지능형 상품 가격 분석 및 추적 시스템 (CLI 버전)".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    scraper = PriceScraper()
    analyzer = DataAnalyzer()
    visualizer = Visualizer()
    
    while True:
        print("\n" + "-" * 60)
        print("메뉴:")
        print("  1. 가격 데이터 수집 및 분석")
        print("  2. 저장된 결과 불러오기")
        print("  3. 종료")
        print("-" * 60)
        
        choice = input("\n선택하세요 (1-3): ").strip()
        
        if choice == '1':
            keyword = input("\n검색 키워드를 입력하세요: ").strip()
            
            if not keyword:
                print("키워드를 입력해주세요.")
                continue
            
            try:
                # 가격 수집
                prices = scraper.scrape_prices(keyword)
                
                if not prices:
                    print("수집된 가격 데이터가 없습니다.")
                    continue
                
                # 통계 분석
                stats = analyzer.calculate_statistics(prices)
                
                # 결과 출력
                print_statistics(stats, keyword)
                print_price_list(prices, limit=10)
                
                # 히스토그램 생성
                visualizer.save_histogram(prices, keyword)
                
                # 결과 저장 여부
                save = input("\n결과를 저장하시겠습니까? (y/n): ").strip().lower()
                if save == 'y':
                    data = {
                        'keyword': keyword,
                        'prices': prices,
                        'statistics': stats
                    }
                    analyzer.save_results(data)
                
            except Exception as e:
                print(f"\n오류 발생: {e}")
        
        elif choice == '2':
            # 저장된 pkl 파일 목록 표시
            import glob
            pkl_files = sorted(glob.glob('*.pkl'), key=os.path.getmtime, reverse=True)
            
            if not pkl_files:
                print("\n저장된 결과 파일이 없습니다.")
                continue
            
            print("\n저장된 결과 파일 목록:")
            print("-" * 60)
            for i, file in enumerate(pkl_files[:10], 1):  # 최대 10개만 표시
                # 파일 수정 시간
                mtime = os.path.getmtime(file)
                from datetime import datetime
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                print(f"{i:2d}. {file:40s} ({date_str})")
            
            if len(pkl_files) > 10:
                print(f"... 외 {len(pkl_files) - 10}개")
            
            print("-" * 60)
            choice_input = input("\n파일 번호 또는 파일명 입력 (Enter=최근 파일): ").strip()
            
            # 파일 선택
            if not choice_input:
                filename = pkl_files[0]  # 가장 최근 파일
            elif choice_input.isdigit() and 1 <= int(choice_input) <= len(pkl_files):
                filename = pkl_files[int(choice_input) - 1]
            else:
                filename = choice_input
            
            data = analyzer.load_results(filename)
            
            if data:
                keyword = data.get('keyword', 'Unknown')
                prices = data.get('prices', [])
                stats = data.get('statistics', {})
                
                if stats:
                    print_statistics(stats, keyword)
                    print_price_list(prices, limit=10)
        
        elif choice == '3':
            print("\n프로그램을 종료합니다. 👋")
            break
        
        else:
            print("올바른 메뉴를 선택해주세요.")


def quick_analyze(keyword: str):
    """빠른 분석 모드 (커맨드라인 인자로 실행)"""
    print("\n" + "=" * 60)
    print(f"빠른 분석 모드: {keyword}")
    print("=" * 60)
    
    scraper = PriceScraper()
    analyzer = DataAnalyzer()
    visualizer = Visualizer()
    
    try:
        # 가격 수집
        prices = scraper.scrape_prices(keyword)
        
        if not prices:
            print("수집된 가격 데이터가 없습니다.")
            return
        
        # 통계 분석
        stats = analyzer.calculate_statistics(prices)
        
        # 결과 출력
        print_statistics(stats, keyword)
        print_price_list(prices, limit=10)
        
        # 히스토그램 생성
        visualizer.save_histogram(prices, keyword)
        
        # 자동 저장
        data = {
            'keyword': keyword,
            'prices': prices,
            'statistics': stats
        }
        analyzer.save_results(data)
        
    except Exception as e:
        print(f"\n오류 발생: {e}")


def main():
    """메인 실행 함수"""
    import sys
    
    # 커맨드라인 인자 확인
    if len(sys.argv) > 1:
        keyword = ' '.join(sys.argv[1:])
        quick_analyze(keyword)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
