# 🌐 Flask 웹 대시보드 사용 가이드

## 📖 목차
1. [개요](#개요)
2. [서버 실행 방법](#서버-실행-방법)
3. [기능 소개](#기능-소개)
4. [사용법](#사용법)
5. [문제 해결](#문제-해결)

---

## 개요

상품 가격 분석 시스템의 웹 대시보드입니다. 브라우저에서 실시간으로 상품 가격을 검색하고, 통계를 확인하며, 인터랙티브한 차트로 데이터를 시각화할 수 있습니다.

### 주요 특징
- ✅ **모던한 UI**: 반응형 디자인으로 모바일/데스크톱 모두 지원
- ✅ **실시간 분석**: 다나와 웹사이트에서 실시간 가격 수집
- ✅ **인터랙티브 차트**: Chart.js를 사용한 동적 히스토그램
- ✅ **검색 히스토리**: 최근 검색 결과 자동 저장 및 불러오기
- ✅ **REST API**: JSON 기반 API로 확장 가능

### 기술 스택
- **Backend**: Flask 3.0+ (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **차트**: Chart.js
- **데이터**: BeautifulSoup4, Requests

---

## 서버 실행 방법

### 1. 필수 패키지 설치
```bash
# 가상환경 활성화 (이미 활성화되어 있다면 생략)
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt
```

### 2. 서버 시작
```bash
# 일반 실행
python app.py

# 또는 백그라운드 실행
nohup python app.py > server.log 2>&1 &
```

### 3. 브라우저에서 접속
```
http://localhost:8080
```

### 포트 변경 (선택사항)
만약 8080 포트가 사용 중이라면 `app.py` 파일의 마지막 줄을 수정하세요:
```python
app.run(debug=True, host='0.0.0.0', port=원하는포트번호)
```

---

## 기능 소개

### 1. 실시간 가격 검색
- 키워드 입력 후 검색 버튼 클릭 (또는 엔터)
- 다나와 웹사이트에서 실시간으로 가격 수집
- 평균, 최고, 최저 가격 통계 자동 계산

### 2. 가격 분포 히스토그램
- 20개 구간으로 나눈 가격 분포 차트
- 마우스 오버 시 상세 정보 표시
- 애니메이션 효과로 시각적 피드백

### 3. 가격 목록
- 수집된 가격 상위 20개 표시
- 그리드 레이아웃으로 한눈에 확인

### 4. 검색 결과 저장
- "💾 저장" 버튼으로 현재 결과 저장
- 자동으로 고유한 파일명 생성
- Pickle 형식으로 저장

### 5. 검색 히스토리
- 최근 검색 결과 10개 자동 표시
- 클릭하여 이전 검색 결과 불러오기
- 검색 날짜, 키워드, 통계 정보 표시

---

## 사용법

### 기본 사용 흐름

#### STEP 1: 검색
```
1. 검색창에 키워드 입력 (예: "무선마우스")
2. 🔍 검색 버튼 클릭 또는 엔터
3. 분석 완료까지 대기 (5-10초)
```

#### STEP 2: 결과 확인
```
✅ 통계 카드에서 수집 개수, 평균, 최고/최저 가격 확인
✅ 히스토그램에서 가격 분포 시각화 확인
✅ 가격 목록에서 개별 가격들 확인
```

#### STEP 3: 결과 저장 (선택)
```
💾 저장 버튼 클릭
→ result_[키워드]_[타임스탬프].pkl 파일로 저장
```

#### STEP 4: 히스토리 활용
```
📂 최근 검색 결과 섹션에서
→ 이전 검색 결과 클릭하여 다시 확인
```

### 실전 예제

#### 예제 1: 무선 마우스 가격 비교
```
1. 검색: "무선마우스"
2. 결과 확인:
   - 평균 가격: 35,000원
   - 최저 가격: 15,000원
   - 최고 가격: 120,000원
3. 저장 후 다른 키워드 검색
4. 히스토리에서 비교 분석
```

#### 예제 2: 여러 제품 비교
```
1. "키보드" 검색 → 저장
2. "마우스" 검색 → 저장
3. "모니터" 검색 → 저장
4. 히스토리에서 각 제품의 가격대 비교
```

---

## API 엔드포인트

웹 대시보드는 다음 REST API를 제공합니다:

### POST /api/search
가격 검색
```json
// Request
{
  "keyword": "무선마우스"
}

// Response
{
  "success": true,
  "keyword": "무선마우스",
  "stats": {
    "count": 150,
    "average": 35000,
    "max": 120000,
    "min": 15000,
    "range": 105000
  },
  "prices": [15000, 18000, ...],
  "histogram": {
    "labels": ["15,000", "20,000", ...],
    "values": [5, 12, ...]
  }
}
```

### GET /api/history
검색 히스토리 조회
```json
// Response
{
  "success": true,
  "history": [
    {
      "filename": "result_무선마우스_20231227_143022.pkl",
      "keyword": "무선마우스",
      "date": "2023-12-27 14:30",
      "stats": {...}
    }
  ]
}
```

### POST /api/save
결과 저장
```json
// Request
{
  "keyword": "무선마우스",
  "prices": [15000, 18000, ...],
  "stats": {...}
}

// Response
{
  "success": true,
  "filename": "result_무선마우스_20231227_143022.pkl",
  "message": "결과가 저장되었습니다."
}
```

### GET /api/load/<filename>
저장된 결과 불러오기
```json
// Response
{
  "success": true,
  "data": {
    "keyword": "무선마우스",
    "prices": [15000, 18000, ...],
    "statistics": {...}
  }
}
```

---

## 문제 해결

### 1. 포트 5000/8080이 이미 사용 중
**증상**: "Address already in use" 에러

**해결 방법**:
```bash
# 방법 1: 포트 사용 프로세스 확인 및 종료
lsof -ti:8080 | xargs kill -9

# 방법 2: 다른 포트 사용
# app.py 마지막 줄 수정
app.run(debug=True, host='0.0.0.0', port=9000)
```

**macOS AirPlay Receiver 문제**:
- 시스템 설정 → 일반 → AirPlay 수신기 끄기

### 2. 검색 결과가 나오지 않음
**증상**: "수집된 가격 데이터가 없습니다" 메시지

**해결 방법**:
1. 키워드를 더 구체적으로 변경
2. 인터넷 연결 확인
3. 서버 로그 확인:
```bash
# 터미널에서 실행 중인 서버의 로그 확인
# 또는 백그라운드 실행 시
tail -f server.log
```

### 3. 히스토그램이 표시되지 않음
**증상**: 차트 영역이 비어있음

**해결 방법**:
1. 브라우저 콘솔 확인 (F12 → Console)
2. Chart.js CDN 로딩 확인
3. 브라우저 캐시 삭제 후 새로고침 (Ctrl+Shift+R)

### 4. 저장 기능이 작동하지 않음
**증상**: "저장 중 오류가 발생했습니다" 메시지

**해결 방법**:
1. 프로젝트 디렉토리 쓰기 권한 확인
```bash
ls -la | grep result_
chmod 755 .
```

2. 디스크 용량 확인
```bash
df -h
```

### 5. 서버가 느리게 응답함
**증상**: 검색 시 오래 걸림 (30초 이상)

**해결 방법**:
1. 인터넷 속도 확인
2. 다나와 서버 상태 확인 (브라우저에서 직접 접속)
3. 동시 검색 수 줄이기
4. `price_analyzer_cli.py`의 타임아웃 설정 확인

---

## 고급 기능

### 커스텀 스타일링
`static/css/style.css` 파일을 수정하여 디자인 변경 가능:
```css
/* 예: 메인 색상 변경 */
:root {
    --primary-color: #FF6B6B;  /* 빨간색으로 변경 */
}
```

### API 외부 접근 허용
네트워크의 다른 기기에서 접근하려면:
```python
# app.py
app.run(debug=False, host='0.0.0.0', port=8080)
```
그 다음 브라우저에서:
```
http://[서버IP주소]:8080
```

### 프로덕션 배포
개발 서버 대신 프로덕션 서버 사용:
```bash
# Gunicorn 설치
pip install gunicorn

# 실행
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

---

## 스크린샷 설명

### 메인 화면
- **헤더**: 프로젝트 제목 및 설명
- **검색 섹션**: 키워드 입력 및 검색 버튼
- **통계 카드**: 수집 개수, 평균, 최고/최저 가격
- **히스토그램**: 가격 분포 차트
- **가격 목록**: 개별 가격 그리드
- **히스토리**: 최근 검색 결과 목록

### 반응형 디자인
- 데스크톱: 4열 그리드
- 태블릿: 2열 그리드
- 모바일: 1열 세로 레이아웃

---

## 프로젝트 구조

```
Computing-Thinking-Term-Project/
├── app.py                    # Flask 서버 메인 파일
├── templates/
│   └── index.html           # 웹 대시보드 HTML
├── static/
│   ├── css/
│   │   └── style.css        # 스타일시트
│   └── js/
│       └── main.js          # JavaScript 로직
├── price_analyzer_cli.py    # 백엔드 모듈
├── requirements.txt          # Python 패키지 목록
└── *.pkl                    # 저장된 검색 결과
```

---

## 참고 자료

- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [Chart.js 문서](https://www.chartjs.org/)
- [BeautifulSoup4 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

## 라이선스
Computing Thinking Term Project © 2023

---

**즐거운 가격 분석 되세요! 🎉**
