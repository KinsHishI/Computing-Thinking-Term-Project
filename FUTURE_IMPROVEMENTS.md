# 프로젝트 개선 및 확장 아이디어

## 🎯 현재 프로젝트 완성도

현재 프로젝트는 기본 요구사항을 완벽하게 충족하고 있습니다:
- ✅ 웹 크롤링
- ✅ 정규표현식
- ✅ 통계 분석
- ✅ 데이터 시각화
- ✅ GUI/CLI
- ✅ 파일 I/O
- ✅ 예외 처리

**현재 점수 예상: A ~ A+**

---

## 🚀 개선 및 확장 아이디어 (우선순위순)

### 1단계: 쉬운 개선 (단기 - 1-2시간)

#### 1.1 데이터베이스 연동 ⭐⭐⭐
**난이도**: ⭐⭐ | **효과**: ⭐⭐⭐⭐⭐

```python
# SQLite를 활용한 히스토리 관리
import sqlite3
from datetime import datetime

class PriceHistory:
    """가격 히스토리를 데이터베이스로 관리"""
    
    def __init__(self, db_file='price_history.db'):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                search_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                avg_price REAL,
                min_price INTEGER,
                max_price INTEGER,
                count INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id INTEGER,
                price INTEGER,
                FOREIGN KEY (search_id) REFERENCES searches(id)
            )
        ''')
        self.conn.commit()
    
    def save_search(self, keyword, prices, stats):
        """검색 결과를 DB에 저장"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO searches (keyword, avg_price, min_price, max_price, count)
            VALUES (?, ?, ?, ?, ?)
        ''', (keyword, stats['average'], stats['min'], stats['max'], stats['count']))
        
        search_id = cursor.lastrowid
        
        # 가격 데이터 저장
        for price in prices:
            cursor.execute('INSERT INTO prices (search_id, price) VALUES (?, ?)',
                         (search_id, price))
        
        self.conn.commit()
        return search_id
    
    def get_price_trend(self, keyword, days=7):
        """특정 키워드의 가격 추이 조회"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT search_date, avg_price, min_price, max_price
            FROM searches
            WHERE keyword = ?
            AND search_date >= datetime('now', '-' || ? || ' days')
            ORDER BY search_date
        ''', (keyword, days))
        return cursor.fetchall()
```

**장점**:
- 가격 추이 분석 가능
- 여러 검색 결과 비교 쉬움
- SQL 학습 내용 적용
- 데이터 관리 체계화

---

#### 1.2 가격 변동 알림 기능 ⭐⭐
**난이도**: ⭐ | **효과**: ⭐⭐⭐

```python
class PriceAlert:
    """목표 가격 도달 시 알림"""
    
    def __init__(self):
        self.alerts = {}  # {keyword: target_price}
    
    def set_alert(self, keyword, target_price):
        """알림 설정"""
        self.alerts[keyword] = target_price
        print(f"✅ '{keyword}' 가격이 {target_price:,}원 이하가 되면 알림")
    
    def check_alerts(self, keyword, current_min_price):
        """알림 확인"""
        if keyword in self.alerts:
            target = self.alerts[keyword]
            if current_min_price <= target:
                self.send_notification(keyword, current_min_price, target)
                return True
        return False
    
    def send_notification(self, keyword, price, target):
        """알림 전송"""
        print("\n" + "="*60)
        print("🔔 가격 알림!")
        print("="*60)
        print(f"상품: {keyword}")
        print(f"목표 가격: {target:,}원")
        print(f"현재 최저가: {price:,}원")
        print("="*60)
        
        # macOS 시스템 알림 (선택사항)
        import os
        os.system(f'''
            osascript -e 'display notification "{keyword}이(가) {price:,}원!" with title "가격 알림"'
        ''')
```

---

#### 1.3 엑셀 내보내기 기능 ⭐
**난이도**: ⭐ | **효과**: ⭐⭐⭐

```python
def export_to_excel(self, keyword, prices, stats, filename=None):
    """결과를 엑셀 파일로 내보내기"""
    import pandas as pd
    from datetime import datetime
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'price_report_{keyword}_{timestamp}.xlsx'
    
    # 통계 요약
    summary_df = pd.DataFrame([stats])
    
    # 가격 데이터
    prices_df = pd.DataFrame({
        '순번': range(1, len(prices) + 1),
        '가격 (원)': prices
    })
    
    # 엑셀 파일 작성
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        summary_df.to_excel(writer, sheet_name='통계 요약', index=False)
        prices_df.to_excel(writer, sheet_name='가격 목록', index=False)
    
    print(f"📊 엑셀 파일 저장: {filename}")
```

**필요 라이브러리**:
```bash
pip install pandas openpyxl
```

---

### 2단계: 중급 개선 (중기 - 3-5시간)

#### 2.1 여러 쇼핑몰 통합 비교 ⭐⭐⭐⭐
**난이도**: ⭐⭐⭐ | **효과**: ⭐⭐⭐⭐⭐

```python
class MultiSiteScraper:
    """여러 쇼핑몰 크롤링"""
    
    def __init__(self):
        self.scrapers = {
            'danawa': DanawaScraper(),
            'coupang': CoupangScraper(),
            'elevenst': ElevenStScraper()
        }
    
    def scrape_all(self, keyword):
        """모든 사이트에서 가격 수집"""
        results = {}
        
        for site_name, scraper in self.scrapers.items():
            try:
                prices = scraper.scrape_prices(keyword)
                results[site_name] = {
                    'prices': prices,
                    'avg': sum(prices) / len(prices) if prices else 0,
                    'min': min(prices) if prices else 0
                }
            except Exception as e:
                print(f"❌ {site_name} 수집 실패: {e}")
        
        return results
    
    def compare_sites(self, results):
        """사이트별 가격 비교"""
        print("\n🏪 쇼핑몰별 가격 비교")
        print("="*60)
        
        for site, data in sorted(results.items(), 
                                 key=lambda x: x[1]['min']):
            print(f"{site:12s}: 최저 {data['min']:>10,}원 | "
                  f"평균 {data['avg']:>10,.0f}원")
```

---

#### 2.2 가격 추이 그래프 ⭐⭐⭐
**난이도**: ⭐⭐ | **효과**: ⭐⭐⭐⭐

```python
def plot_price_trend(self, keyword, history):
    """가격 추이 그래프"""
    import matplotlib.pyplot as plt
    from datetime import datetime
    
    dates = [datetime.strptime(h[0], '%Y-%m-%d %H:%M:%S') for h in history]
    avg_prices = [h[1] for h in history]
    min_prices = [h[2] for h in history]
    max_prices = [h[3] for h in history]
    
    plt.figure(figsize=(12, 6))
    
    # 평균 가격 추이
    plt.plot(dates, avg_prices, 'b-o', label='평균', linewidth=2)
    
    # 최저/최고 가격 범위
    plt.fill_between(dates, min_prices, max_prices, 
                     alpha=0.3, label='가격 범위')
    
    plt.title(f'{keyword} 가격 추이', fontsize=16, fontweight='bold')
    plt.xlabel('날짜', fontsize=12)
    plt.ylabel('가격 (원)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # 가격 포맷팅
    ax = plt.gca()
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, p: f'{int(x):,}')
    )
    
    plt.tight_layout()
    plt.savefig(f'trend_{keyword}.png', dpi=150)
    plt.show()
```

---

#### 2.3 웹 대시보드 (Flask) ⭐⭐⭐⭐⭐
**난이도**: ⭐⭐⭐⭐ | **효과**: ⭐⭐⭐⭐⭐

```python
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)
scraper = PriceScraper()
analyzer = DataAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """가격 검색 API"""
    keyword = request.json.get('keyword')
    
    try:
        prices = scraper.scrape_prices(keyword)
        stats = analyzer.calculate_statistics(prices)
        
        return jsonify({
            'success': True,
            'keyword': keyword,
            'stats': stats,
            'prices': prices[:20]  # 상위 20개만
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/<keyword>')
def get_history(keyword):
    """가격 히스토리 조회"""
    db = PriceHistory()
    history = db.get_price_trend(keyword, days=30)
    
    return jsonify({
        'keyword': keyword,
        'history': history
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**HTML 템플릿 (templates/index.html)**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>가격 분석 대시보드</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .search-box { margin: 20px 0; }
        input { padding: 10px; font-size: 16px; width: 300px; }
        button { padding: 10px 20px; font-size: 16px; }
        .result { margin-top: 20px; }
        canvas { max-width: 800px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>🔍 지능형 가격 분석 대시보드</h1>
    
    <div class="search-box">
        <input type="text" id="keyword" placeholder="검색 키워드 입력">
        <button onclick="search()">검색</button>
    </div>
    
    <div id="result" class="result"></div>
    <canvas id="priceChart"></canvas>
    
    <script>
        async function search() {
            const keyword = document.getElementById('keyword').value;
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({keyword})
            });
            
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('result').innerHTML = `
                    <h2>${data.keyword} 분석 결과</h2>
                    <p>평균: ${data.stats.average.toLocaleString()}원</p>
                    <p>최저: ${data.stats.min.toLocaleString()}원</p>
                    <p>최고: ${data.stats.max.toLocaleString()}원</p>
                `;
                
                // 히스토그램 그리기
                drawChart(data.prices);
            }
        }
        
        function drawChart(prices) {
            const ctx = document.getElementById('priceChart');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: prices.map((p, i) => i + 1),
                    datasets: [{
                        label: '가격',
                        data: prices,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)'
                    }]
                }
            });
        }
    </script>
</body>
</html>
```

---

### 3단계: 고급 개선 (장기 - 1주일+)

#### 3.1 머신러닝 가격 예측 ⭐⭐⭐⭐⭐
**난이도**: ⭐⭐⭐⭐⭐ | **효과**: ⭐⭐⭐⭐⭐

```python
from sklearn.linear_model import LinearRegression
import numpy as np

class PricePredictor:
    """가격 예측 모델"""
    
    def __init__(self):
        self.model = LinearRegression()
    
    def train(self, history):
        """히스토리 데이터로 학습"""
        # 날짜를 숫자로 변환
        X = np.array([[i] for i in range(len(history))])
        y = np.array([h['avg_price'] for h in history])
        
        self.model.fit(X, y)
    
    def predict_future(self, days=7):
        """미래 가격 예측"""
        future_X = np.array([[i] for i in range(days)])
        predictions = self.model.predict(future_X)
        
        return predictions
```

---

#### 3.2 자동화 및 스케줄링 ⭐⭐⭐
**난이도**: ⭐⭐⭐ | **효과**: ⭐⭐⭐⭐

```python
import schedule
import time

class PriceMonitor:
    """자동 가격 모니터링"""
    
    def __init__(self):
        self.scraper = PriceScraper()
        self.db = PriceHistory()
        self.alert = PriceAlert()
    
    def monitor_keyword(self, keyword, target_price=None):
        """키워드 모니터링"""
        try:
            prices = self.scraper.scrape_prices(keyword)
            stats = DataAnalyzer.calculate_statistics(prices)
            
            # DB 저장
            self.db.save_search(keyword, prices, stats)
            
            # 알림 확인
            if target_price:
                self.alert.check_alerts(keyword, stats['min'])
            
            print(f"[{datetime.now()}] {keyword}: {stats['min']:,}원")
            
        except Exception as e:
            print(f"❌ 모니터링 오류: {e}")
    
    def start(self, keywords, interval='1h'):
        """모니터링 시작"""
        for keyword in keywords:
            if interval == '1h':
                schedule.every().hour.do(
                    self.monitor_keyword, keyword
                )
            elif interval == '1d':
                schedule.every().day.at("10:00").do(
                    self.monitor_keyword, keyword
                )
        
        print("🔄 자동 모니터링 시작...")
        while True:
            schedule.run_pending()
            time.sleep(60)

# 사용 예시
monitor = PriceMonitor()
monitor.alert.set_alert('노트북', 900000)
monitor.start(['노트북', '마우스'], interval='1h')
```

---

## 📊 개선 우선순위 추천

### 학기말 프로젝트용 (시간 제한)
1. **SQLite 데이터베이스** (1-2시간)
   - 가장 큰 효과
   - 구현 쉬움
   - 추가 학습 내용 적용

2. **엑셀 내보내기** (30분)
   - 빠르고 실용적
   - 사용자 편의성 향상

3. **가격 알림** (30분)
   - 차별화 요소
   - 실용성 높음

### 포트폴리오용 (시간 여유)
1. **웹 대시보드 (Flask)**
   - 가장 인상적
   - 실무 활용도 높음

2. **여러 쇼핑몰 통합**
   - 실용성 최고
   - 기술력 증명

3. **가격 추이 그래프**
   - 시각적 효과

---

## 💡 구현 순서 제안

### 빠른 개선 (1-2시간)
```bash
# 1. SQLite 추가
pip install pandas openpyxl

# 2. price_analyzer_cli.py에 클래스 추가
# 3. 메뉴에 새 기능 추가
# 4. 테스트
```

### 코드 추가 위치
```python
# price_analyzer_cli.py 끝에 추가

class PriceHistory:
    # ... SQLite 코드 ...

class PriceAlert:
    # ... 알림 코드 ...

def export_to_excel(keyword, prices, stats):
    # ... 엑셀 내보내기 ...

# interactive_mode() 메뉴에 추가
print("메뉴:")
print("  1. 가격 데이터 수집 및 분석")
print("  2. 저장된 결과 불러오기")
print("  3. 가격 추이 확인 (DB)")  # NEW
print("  4. 알림 설정")  # NEW
print("  5. 엑셀 내보내기")  # NEW
print("  6. 종료")
```

---

## 🎯 현실적인 추천

### 지금 바로 추가 (30분)
- ✅ 엑셀 내보내기
- ✅ 가격 알림 기능

### 시간 여유 있으면 (2시간)
- ✅ SQLite 데이터베이스
- ✅ 가격 추이 그래프

### 나중에 (졸업 후)
- 웹 대시보드
- 머신러닝 예측
- 여러 쇼핑몰 통합

---

## 📝 결론

**현재 상태로도 충분히 우수합니다!** (A~A+ 예상)

하지만 **30분만 투자**하면:
- 엑셀 내보내기 추가
- 실용성과 편의성 대폭 향상
- 차별화 요소 확보
- **A+ 확정 가능성 높음**

어떤 기능을 추가하고 싶으신가요? 바로 구현해드리겠습니다! 🚀
