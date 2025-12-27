# 사용 가이드 및 예제

### 1. GUI 모드로 실행 (권장)
```bash
python3 price_analyzer.py
```

프로그램이 실행되면 다음과 같이 사용하세요:

1. **검색어 입력**: "노트북", "키보드", "마우스" 등
2. **수집 시작** 클릭
3. 결과 확인 후 **그래프 보기**
4. 필요시 **결과 저장**

### 2. 컴포넌트 테스트
```bash
python3 test_components.py
```

개별 클래스의 기능을 테스트할 수 있습니다.

## 📖 코드 예제

### 예제 1: 기본적인 가격 수집

```python
from price_analyzer import PriceScraper

# 스크래퍼 생성
scraper = PriceScraper()

# 가격 수집
prices = scraper.scrape_prices("무선마우스")

print(f"수집된 가격: {len(prices)}개")
print(f"가격 범위: {min(prices):,}원 ~ {max(prices):,}원")
```

### 예제 2: 통계 분석

```python
from price_analyzer import DataAnalyzer

# 분석기 생성
analyzer = DataAnalyzer()

# 샘플 데이터
prices = [15900, 23500, 35000, 42000, 18900]

# 통계 계산
stats = analyzer.calculate_statistics(prices)

print(f"평균 가격: {stats['average']:,.0f}원")
print(f"최고 가격: {stats['max']:,}원")
print(f"최저 가격: {stats['min']:,}원")
```

### 예제 3: 결과 저장 및 불러오기

```python
from price_analyzer import DataAnalyzer

analyzer = DataAnalyzer()

# 데이터 저장
data = {
    'keyword': '노트북',
    'prices': [890000, 1200000, 1450000],
    'statistics': {'average': 1180000, 'max': 1450000, 'min': 890000}
}
analyzer.save_results(data, 'my_result.pkl')

# 데이터 불러오기
loaded = analyzer.load_results('my_result.pkl')
print(f"검색어: {loaded['keyword']}")
print(f"평균: {loaded['statistics']['average']:,}원")
```

### 예제 4: 히스토그램 생성

```python
from price_analyzer import Visualizer

# 시각화 도구 생성
visualizer = Visualizer()

# 샘플 데이터
prices = [20000, 25000, 23000, 30000, 22000, 28000, 26000]

# 히스토그램 표시
visualizer.plot_histogram(prices, "무선 키보드")
```

### 예제 5: 전체 프로세스 자동화

```python
from price_analyzer import PriceScraper, DataAnalyzer, Visualizer

def analyze_product(keyword):
    """상품 가격 전체 분석 파이프라인"""
    
    # 1. 데이터 수집
    scraper = PriceScraper()
    prices = scraper.scrape_prices(keyword)
    
    if not prices:
        print("데이터를 찾을 수 없습니다.")
        return
    
    # 2. 통계 분석
    analyzer = DataAnalyzer()
    stats = analyzer.calculate_statistics(prices)
    
    print(f"\n📊 {keyword} 가격 분석 결과")
    print(f"수집 개수: {stats['count']}개")
    print(f"평균 가격: {stats['average']:,.0f}원")
    print(f"가격 범위: {stats['min']:,}원 ~ {stats['max']:,}원")
    
    # 3. 결과 저장
    data = {
        'keyword': keyword,
        'prices': prices,
        'statistics': stats
    }
    analyzer.save_results(data)
    print(f"✅ 결과 저장 완료: last_result.pkl")
    
    # 4. 시각화
    visualizer = Visualizer()
    visualizer.plot_histogram(prices, keyword)

# 실행
analyze_product("USB 메모리")
```

## 🔍 고급 사용법

### 사용자 정의 가격 범위 설정

```python
from price_analyzer import PriceScraper

scraper = PriceScraper()

# 가격 범위 변경 (10만원 ~ 200만원)
scraper.min_price = 100000
scraper.max_price = 2000000

prices = scraper.scrape_prices("노트북")
```

### 리스트 함축을 활용한 데이터 필터링

```python
# 50,000원 이상의 가격만 필터링
high_prices = [p for p in prices if p >= 50000]

# 가격을 만원 단위로 반올림
rounded_prices = [round(p, -4) for p in prices]

# 상위 10개 가격
top_10 = sorted(prices, reverse=True)[:10]
```

### 정규표현식 패턴 이해

```python
import re

# 가격 추출 패턴
pattern = r"(\d[\d,]*)\s*원"

text = "이 상품은 25,900원입니다."
match = re.search(pattern, text)

if match:
    price_str = match.group(1)  # "25,900"
    price_int = int(price_str.replace(',', ''))  # 25900
    print(f"추출된 가격: {price_int:,}원")
```

## 💡 실전 활용 시나리오

### 시나리오 1: 여러 키워드 비교 분석

```python
from price_analyzer import PriceScraper, DataAnalyzer

keywords = ["무선 마우스", "유선 마우스", "게이밍 마우스"]
scraper = PriceScraper()
analyzer = DataAnalyzer()

results = {}

for keyword in keywords:
    try:
        prices = scraper.scrape_prices(keyword)
        stats = analyzer.calculate_statistics(prices)
        results[keyword] = stats['average']
    except Exception as e:
        print(f"{keyword} 수집 실패: {e}")

# 결과 출력
print("\n📊 카테고리별 평균 가격 비교")
for keyword, avg_price in sorted(results.items(), key=lambda x: x[1]):
    print(f"{keyword:20s}: {avg_price:>10,.0f}원")
```

### 시나리오 2: 가격 추이 모니터링

```python
import time
from datetime import datetime
from price_analyzer import PriceScraper, DataAnalyzer

def monitor_price(keyword, interval=3600):
    """특정 상품의 가격을 주기적으로 모니터링"""
    scraper = PriceScraper()
    analyzer = DataAnalyzer()
    
    history = []
    
    print(f"'{keyword}' 가격 모니터링 시작...")
    
    try:
        while True:
            prices = scraper.scrape_prices(keyword)
            stats = analyzer.calculate_statistics(prices)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history.append({
                'time': timestamp,
                'average': stats['average'],
                'min': stats['min'],
                'max': stats['max']
            })
            
            print(f"[{timestamp}] 평균: {stats['average']:,.0f}원")
            
            # 결과 저장
            analyzer.save_results({
                'keyword': keyword,
                'history': history
            }, f'price_history_{keyword}.pkl')
            
            time.sleep(interval)  # interval초 대기
            
    except KeyboardInterrupt:
        print("\n모니터링 종료")

# 1시간마다 체크
# monitor_price("SSD 500GB", interval=3600)
```

## 🎨 GUI 커스터마이징

GUI의 색상이나 폰트를 변경하려면 `price_analyzer.py`의 `_setup_gui()` 메서드를 수정하세요:

```python
# 버튼 색상 변경
self.collect_btn = tk.Button(
    top_frame, 
    text="수집 시작", 
    command=self.start_collection,
    bg="#FF5722",  # 주황색으로 변경
    fg="white",
    font=("Arial", 12, "bold")
)

# 텍스트 영역 폰트 변경
self.result_text = scrolledtext.ScrolledText(
    middle_frame, 
    font=("Monaco", 11),  # 폰트 변경
    bg="#F5F5F5"  # 배경색 변경
)
```

## 🐛 일반적인 문제 해결

### 문제 1: "수집된 가격이 없습니다"
**원인**: 검색 키워드가 너무 구체적이거나 웹사이트 구조 변경  
**해결**: 더 일반적인 키워드 사용 (예: "게이밍 노트북 RTX" → "노트북")

### 문제 2: 네트워크 오류
**원인**: 인터넷 연결 문제 또는 웹사이트 접근 제한  
**해결**: 
- 인터넷 연결 확인
- VPN 사용 시 해제
- 잠시 후 다시 시도

### 문제 3: 한글이 깨져 보임
**원인**: 시스템에 한글 폰트가 없음  
**해결**:
```python
# price_analyzer.py의 Visualizer 클래스에서
plt.rcParams['font.family'] = 'NanumGothic'  # 다른 폰트 시도
```

### 문제 4: tkinter import 오류
**원인**: Python이 tkinter 없이 빌드됨  
**해결**:
```bash
# macOS
brew install python-tk

# Ubuntu/Debian
sudo apt-get install python3-tk
```

## 📚 더 알아보기

### 관련 문서
- [Python requests 문서](https://requests.readthedocs.io/)
- [BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [matplotlib 튜토리얼](https://matplotlib.org/stable/tutorials/index.html)
- [tkinter 가이드](https://docs.python.org/3/library/tkinter.html)

---

문의사항이 있으시면 이슈를 등록해주세요!
