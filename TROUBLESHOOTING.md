# tkinter 호환성 문제 해결 가이드

## 문제 상황

macOS에서 `price_analyzer.py` (GUI 버전)를 실행할 때 다음 오류가 발생할 수 있습니다:

```
macOS 26 (2601) or later required, have instead 16 (1601) !
zsh: abort      python3 price_analyzer.py
```

## 원인

- macOS 구버전의 tkinter 라이브러리가 최신 WebKit을 요구하지만 시스템이 이를 지원하지 않음
- Python 3.9.6에 포함된 tkinter 8.5 버전의 호환성 문제

## 해결 방법

### ✅ 방법 1: CLI 버전 사용 (권장)

프로젝트에 tkinter 의존성이 없는 **CLI (Command Line Interface) 버전**이 포함되어 있습니다.

```bash
# 대화형 모드로 실행
python3 price_analyzer_cli.py

# 빠른 분석 (키워드를 직접 전달)
python3 price_analyzer_cli.py 무선마우스
```

**CLI 버전의 특징:**
- ✅ 모든 환경에서 작동 (macOS, Linux, Windows)
- ✅ tkinter 의존성 없음
- ✅ 동일한 기능 제공 (크롤링, 통계, 시각화)
- ✅ 히스토그램은 PNG 파일로 저장
- ✅ 터미널에서 바로 결과 확인

### 방법 2: Homebrew로 Python 재설치

최신 Python과 tkinter를 설치합니다:

```bash
# Homebrew 설치 (없는 경우)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python과 tkinter 설치
brew install python-tk@3.11

# 새로운 Python으로 실행
/usr/local/bin/python3.11 price_analyzer.py
```

### 방법 3: Anaconda/Miniconda 사용

Anaconda를 사용하여 격리된 환경을 만듭니다:

```bash
# Miniconda 설치
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh

# 환경 생성 및 활성화
conda create -n price_analyzer python=3.10
conda activate price_analyzer

# 라이브러리 설치
pip install -r requirements.txt

# 프로그램 실행
python price_analyzer.py
```

## CLI 버전 사용법

### 1. 대화형 모드

```bash
$ python3 price_analyzer_cli.py

╔══════════════════════════════════════════════════════════╗
║                                                          ║
║    지능형 상품 가격 분석 및 추적 시스템 (CLI 버전)                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

------------------------------------------------------------
메뉴:
  1. 가격 데이터 수집 및 분석
  2. 저장된 결과 불러오기
  3. 종료
------------------------------------------------------------

선택하세요 (1-3): 1

검색 키워드를 입력하세요: 무선마우스

🔍 '무선마우스' 검색 중...
✅ 47개의 가격 데이터 수집 완료

============================================================
📊 무선마우스 - 가격 분석 결과
============================================================
수집된 가격 개수: 47개
평균 가격:                28,450원
최고 가격:                89,900원
최저 가격:                 9,800원
가격 범위:                80,100원
============================================================

💰 수집된 가격 목록 (상위 10개):
------------------------------------------------------------
 1.           9,800원
 2.          12,900원
 3.          15,900원
 ...

📊 히스토그램 저장 완료: price_histogram.png

결과를 저장하시겠습니까? (y/n): y
💾 결과 저장 완료: last_result.pkl
```

### 2. 빠른 분석 모드

키워드를 인자로 전달하면 즉시 분석하고 결과를 저장합니다:

```bash
python3 price_analyzer_cli.py 무선키보드
```

### 3. 스크립트 자동화

CLI 버전은 자동화 스크립트에서도 사용할 수 있습니다:

```bash
#!/bin/bash
# 여러 키워드를 순차적으로 분석

keywords=("무선마우스" "무선키보드" "USB 메모리")

for keyword in "${keywords[@]}"; do
    echo "분석 중: $keyword"
    python3 price_analyzer_cli.py "$keyword"
    sleep 5  # 서버 부담 방지
done
```

## 기능 비교

| 기능 | GUI 버전 | CLI 버전 |
|------|---------|---------|
| 가격 크롤링 | ✅ | ✅ |
| 통계 분석 | ✅ | ✅ |
| 히스토그램 | 팝업 창 | PNG 파일 저장 |
| 결과 저장/불러오기 | ✅ | ✅ |
| 사용자 인터페이스 | 그래픽 | 터미널 텍스트 |
| macOS 구버전 지원 | ❌ | ✅ |
| 자동화 스크립트 | 어려움 | 쉬움 |

## 프로젝트 제출 시 참고사항

### 보고서 작성

두 버전 모두 포함되어 있으므로 다음과 같이 설명할 수 있습니다:

1. **GUI 버전** (`price_analyzer.py`):
   - tkinter를 활용한 사용자 친화적 인터페이스
   - 13장 PPT 내용 적용
   - 최신 환경에서 최적화

2. **CLI 버전** (`price_analyzer_cli.py`):
   - 환경 독립적인 커맨드라인 인터페이스
   - 모든 macOS 버전 지원
   - 자동화 및 스크립트 활용 가능

### 시연 방법

**환경에 따라 선택:**

- **최신 macOS (Big Sur 이상)**: GUI 버전 사용
- **구버전 macOS**: CLI 버전 사용
- **원격 서버**: CLI 버전 사용

### 코드 설명

두 버전 모두 동일한 핵심 로직을 사용합니다:

- `PriceScraper`: 웹 크롤링
- `DataAnalyzer`: 통계 분석
- `Visualizer`: 데이터 시각화

차이점은 **사용자 인터페이스**만 다릅니다:
- GUI 버전: tkinter 이벤트 기반
- CLI 버전: 메뉴 선택 및 터미널 출력

## 추가 도움말

### 생성되는 파일

CLI 버전 사용 시 다음 파일이 생성됩니다:

- `price_histogram.png`: 가격 분포 히스토그램 이미지
- `last_result.pkl`: 분석 결과 데이터
- `demo_histogram.png`: 데모 실행 시 생성
- `demo_result.pkl`: 데모 결과 데이터

### 이미지 파일 확인

```bash
# macOS에서 이미지 열기
open price_histogram.png

# 또는 미리보기로 열기
qlmanage -p price_histogram.png
```

### 저장된 데이터 확인

Python으로 pickle 파일을 읽어볼 수 있습니다:

```python
import pickle

with open('last_result.pkl', 'rb') as f:
    data = pickle.load(f)
    print(f"키워드: {data['keyword']}")
    print(f"평균 가격: {data['statistics']['average']:,.0f}원")
```

## 문의사항

문제가 계속되면 다음을 확인해주세요:

1. Python 버전: `python3 --version`
2. 설치된 라이브러리: `pip3 list | grep -E "requests|beautifulsoup4|matplotlib"`
3. 에러 메시지 전문

---
