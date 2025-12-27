# 지능형 상품 가격 분석 및 추적 시스템

다나와(Danawa) 웹사이트에서 특정 키워드를 검색해 가격 데이터를 크롤링하고, 통계 분석 및 히스토그램 시각화를 수행하는 Python 프로그램입니다.

## 📋 프로젝트 개요

이 시스템은 Computing Thinking 학기말 프로젝트로 개발되었으며, 다음 기능을 제공합니다:

- 🔍 다나와 웹사이트에서 실시간 가격 데이터 크롤링
- 📊 가격 통계 분석 (평균, 최대, 최소)
- 📈 히스토그램을 통한 가격 분포 시각화
- 💾 분석 결과 저장 및 불러오기 (pickle)
- 🖥️ 사용자 친화적인 GUI 인터페이스 (tkinter)

## 🛠️ 기술 스택

- **언어**: Python 3.7+
- **라이브러리**:
  - `requests`: HTTP 요청 처리
  - `BeautifulSoup4`: HTML 파싱
  - `matplotlib`: 데이터 시각화
  - `tkinter`: GUI 구현 (Python 기본 내장)
  - `pickle`: 데이터 직렬화
  - `re`: 정규표현식 패턴 매칭

## 📦 설치 방법

1. 저장소 클론 또는 다운로드:
```bash
cd /Users/leejeongmin/Python/Computing-Thinking-Term-Project
```

2. 필요한 라이브러리 설치:
```bash
pip install -r requirements.txt
```

## 🚀 실행 방법

### 방법 1: GUI 버전 (권장 - macOS 최신 버전)
```bash
python3 price_analyzer.py
```

**주의**: macOS 구버전에서 tkinter 호환성 문제가 발생할 수 있습니다.

### 방법 2: CLI 버전 (모든 환경 지원) ⭐
```bash
# 대화형 모드
python3 price_analyzer_cli.py

# 빠른 분석 모드 (키워드를 인자로 전달)
python3 price_analyzer_cli.py 무선마우스
```

**CLI 버전 특징**:
- ✅ 모든 macOS/Linux/Windows 환경에서 작동
- ✅ tkinter 의존성 없음
- ✅ 터미널에서 바로 실행
- ✅ 히스토그램은 PNG 파일로 저장
- ✅ **자동 파일명 생성**: 결과가 고유한 파일명으로 저장되어 덮어쓰기 방지

## 💡 사용 방법

### GUI 버전
1. **검색 키워드 입력**: 상단 입력창에 검색할 상품명 입력 (예: "노트북", "키보드")
2. **수집 시작**: "수집 시작" 버튼 클릭 또는 Enter 키 입력
3. **결과 확인**: 중앙 텍스트 영역에서 통계 결과 확인
4. **그래프 보기**: "그래프 보기" 버튼으로 가격 분포 히스토그램 확인
5. **결과 저장**: "결과 저장" 버튼 - 자동으로 `result_[키워드]_[날짜시간].pkl` 형식으로 저장 ⭐
6. **결과 불러오기**: "결과 불러오기" 버튼 - 파일 선택 대화상자에서 원하는 파일 선택

### CLI 버전 ⭐
```bash
# 대화형 모드로 실행
$ python3 price_analyzer_cli.py

메뉴:
  1. 가격 데이터 수집 및 분석
  2. 저장된 결과 불러오기
  3. 종료

선택하세요 (1-3): 1
검색 키워드를 입력하세요: 무선마우스

# 또는 빠른 분석 (키워드를 직접 전달)
$ python3 price_analyzer_cli.py 무선마우스
```

**CLI 버전의 장점**:
- 터미널에서 바로 결과 확인
- 히스토그램은 `price_histogram.png` 파일로 자동 저장
- **스마트 파일명**: `result_무선마우스_20251227_221828.pkl` 형식으로 자동 생성
- **파일 목록 표시**: 저장된 결과를 쉽게 선택하여 불러오기
- 스크립트나 자동화에 활용 가능

## 🏗️ 시스템 구조

### 클래스 다이어그램

```
┌─────────────────┐
│  PriceScraper   │ ← 웹 크롤링 및 데이터 파싱
├─────────────────┤
│ - headers       │
│ - base_url      │
│ - min_price     │
│ - max_price     │
├─────────────────┤
│ + scrape_prices()│
│ - _is_valid_price()│
└─────────────────┘

┌─────────────────┐
│  DataAnalyzer   │ ← 통계 분석 및 파일 I/O
├─────────────────┤
│ + calculate_statistics()│
│ + save_results()│
│ + load_results()│
└─────────────────┘

┌─────────────────┐
│   Visualizer    │ ← 데이터 시각화
├─────────────────┤
│ + plot_histogram()│
│ - _setup_korean_font()│
└─────────────────┘

┌─────────────────┐
│PriceAnalyzerGUI │ ← GUI 통합 관리
├─────────────────┤
│ - scraper       │
│ - analyzer      │
│ - visualizer    │
├─────────────────┤
│ + start_collection()│
│ + show_graph()  │
│ + save_results()│
│ + load_results()│
└─────────────────┘
```

## 🔧 주요 기능 상세

### 1. 크롤링 및 데이터 파싱 (PriceScraper)
- **정규표현식 활용**: `r"(\d[\d,]*)\s*원"` 패턴으로 가격 추출
- **User-Agent 헤더**: 418 에러 방지를 위한 브라우저 헤더 설정
- **가격 범위 필터링**: 1,000원 ~ 100,000,000원 범위 검증
- **예외 처리**: 네트워크 오류 및 파싱 오류 처리

### 2. 데이터 분석 (DataAnalyzer)
- **통계 계산**: 평균, 최대, 최소, 개수
- **pickle 직렬화**: 분석 결과 영구 저장
- **파일 I/O**: 안전한 파일 읽기/쓰기

### 3. 데이터 시각화 (Visualizer)
- **히스토그램**: matplotlib을 활용한 가격 분포 시각화
- **한글 폰트 설정**: macOS/Windows 환경별 한글 깨짐 방지
- **평균선 표시**: 통계적 기준선 시각화

### 4. GUI 인터페이스 (PriceAnalyzerGUI)
- **비동기 처리**: threading을 통한 UI 응답성 유지
- **실시간 상태 표시**: ScrolledText로 진행 상황 표시
- **버튼 상태 관리**: 작업 진행에 따른 버튼 활성화/비활성화

## 📚 학습 내용 적용

본 프로젝트는 다음 강의 내용을 적용했습니다:

- **9장 PPT**: pickle 모듈을 활용한 파일 입출력
- **11장 PPT**: 리스트 함축(List Comprehension) 활용
- **13장 PPT**: tkinter를 활용한 GUI 구성
- **Library 보고서**: requests, BeautifulSoup4 활용한 웹 크롤링
- **SRS 문서**: 체계적인 요구사항 분석 및 시스템 설계

## ⚠️ 주의사항

1. **네트워크 연결**: 인터넷 연결이 필요합니다
2. **웹사이트 정책**: 다나와 웹사이트의 이용약관을 준수해야 합니다
3. **크롤링 속도**: 과도한 요청은 서버에 부담을 줄 수 있습니다
4. **한글 폰트**: macOS는 AppleGothic, Windows는 Malgun Gothic 사용
5. **GUI 버전 호환성**: macOS 구버전에서는 tkinter 문제가 발생할 수 있습니다
   - 해결방법: `price_analyzer_cli.py` (CLI 버전) 사용

## 🐛 문제 해결

### tkinter 호환성 문제 (macOS)
```
macOS 26 (2601) or later required, have instead 16 (1601) !
```
**해결방법**: CLI 버전을 사용하세요
```bash
python3 price_analyzer_cli.py
```

### matplotlib 한글 깨짐
```python
# macOS
plt.rcParams['font.family'] = 'AppleGothic'

# Windows
plt.rcParams['font.family'] = 'Malgun Gothic'
```

### 크롤링 실패 시
- 검색 키워드 변경
- 네트워크 연결 확인
- User-Agent 헤더 확인

## 📖 추가 문서

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - tkinter 호환성 문제 및 해결 방법 상세 가이드
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - 상세 사용법 및 코드 예제
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 프로젝트 구현 요약 및 학습 내용 정리