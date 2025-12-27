#!/bin/bash

echo "🔍 웹 대시보드 디버깅 도구"
echo ""

# 1. 서버 상태 확인
echo "1️⃣ Flask 서버 상태 확인..."
if lsof -ti:8080 > /dev/null 2>&1; then
    echo "   ✅ 서버가 8080 포트에서 실행 중입니다."
else
    echo "   ❌ 서버가 실행되고 있지 않습니다!"
    echo "   실행 명령: python3 app.py"
    exit 1
fi
echo ""

# 2. pkl 파일 확인
echo "2️⃣ 저장된 검색 결과 파일 확인..."
pkl_count=$(ls -1 result_*.pkl 2>/dev/null | wc -l)
if [ $pkl_count -gt 0 ]; then
    echo "   ✅ $pkl_count 개의 파일이 있습니다:"
    ls -lh result_*.pkl | awk '{print "      -", $9, "("$5")"}'
else
    echo "   ⚠️  저장된 파일이 없습니다."
    echo "   샘플 생성 명령: python3 create_sample_data.py"
fi
echo ""

# 3. API 테스트
echo "3️⃣ API 엔드포인트 테스트..."
echo ""

echo "   📍 GET /api/history"
history_response=$(curl -s http://localhost:8080/api/history)
if echo "$history_response" | grep -q "success"; then
    history_count=$(echo "$history_response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('history', [])))")
    echo "   ✅ 응답 성공! (히스토리 $history_count 개)"
else
    echo "   ❌ 응답 실패!"
    echo "   $history_response"
fi
echo ""

# 4. 브라우저 접속 정보
echo "4️⃣ 브라우저 접속 정보"
echo "   🌐 메인 페이지: http://localhost:8080"
echo "   📊 API 히스토리: http://localhost:8080/api/history"
echo ""

# 5. 문제 해결 가이드
echo "======================================"
echo "🔧 문제 해결 가이드"
echo ""
echo "❓ 히스토리가 표시되지 않는 경우:"
echo "   1. 브라우저를 새로고침 (Cmd+R 또는 F5)"
echo "   2. 브라우저 콘솔 확인 (F12 → Console)"
echo "   3. '🔄 새로고침' 버튼 클릭"
echo "   4. 브라우저 캐시 삭제 (Cmd+Shift+R)"
echo ""
echo "❓ API 오류가 발생하는 경우:"
echo "   1. 서버 로그 확인 (터미널)"
echo "   2. pkl 파일 권한 확인: ls -la result_*.pkl"
echo "   3. 서버 재시작: Ctrl+C 후 python3 app.py"
echo ""
echo "❓ 샘플 데이터가 필요한 경우:"
echo "   python3 create_sample_data.py"
echo ""
echo "======================================"
