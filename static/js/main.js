// 상품 가격 분석 대시보드 - JavaScript

// 전역 변수
let currentChart = null;
let currentResult = null;

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 대시보드 초기화 중...');
    loadHistory();

    // 엔터키로 검색
    document.getElementById('searchInput').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            searchPrice();
        }
    });
});

// 가격 검색 함수
async function searchPrice() {
    const keyword = document.getElementById('searchInput').value.trim();

    if (!keyword) {
        showError('검색 키워드를 입력해주세요.');
        return;
    }

    // UI 상태 변경
    setSearching(true);
    hideError();
    hideResults();

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ keyword: keyword })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || '검색 중 오류가 발생했습니다.');
        }

        if (data.success) {
            currentResult = data;
            displayResults(data);

            // 저장 완료 메시지 표시
            if (data.saved_filename) {
                showSuccess(`"${keyword}" 검색 완료! ${data.stats.count}개의 가격을 분석했습니다.\n💾 자동 저장: ${data.saved_filename}`);
            } else {
                showSuccess(`"${keyword}" 검색 완료! ${data.stats.count}개의 가격을 분석했습니다.`);
            }

            // 히스토리 자동 새로고침
            setTimeout(() => loadHistory(), 500);
        } else {
            throw new Error(data.error || '결과를 가져올 수 없습니다.');
        }

    } catch (error) {
        console.error('검색 오류:', error);
        showError(error.message);
    } finally {
        setSearching(false);
    }
}

// 검색 상태 UI 업데이트
function setSearching(isSearching) {
    const btn = document.getElementById('searchBtn');
    const input = document.getElementById('searchInput');
    const btnText = document.getElementById('searchBtnText');
    const btnLoading = document.getElementById('searchBtnLoading');

    btn.disabled = isSearching;
    input.disabled = isSearching;

    if (isSearching) {
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
    } else {
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}

// 결과 표시
function displayResults(data) {
    // 통계 카드 업데이트
    document.getElementById('statCount').textContent = data.stats.count.toLocaleString() + '개';
    document.getElementById('statAverage').textContent = Math.round(data.stats.average).toLocaleString() + '원';
    document.getElementById('statMax').textContent = data.stats.max.toLocaleString() + '원';
    document.getElementById('statMin').textContent = data.stats.min.toLocaleString() + '원';

    // 히스토그램 차트 생성
    createChart(data.histogram);

    // 가격 목록 표시
    displayPriceList(data.prices.slice(0, 20)); // 상위 20개만

    // 저장 버튼 상태 업데이트
    updateSaveButton(data.saved_filename);

    // 결과 섹션 표시
    showResults();

    // 히스토리 새로고침
    setTimeout(() => loadHistory(), 500);
}

// 차트 생성
function createChart(histogramData) {
    const ctx = document.getElementById('priceChart').getContext('2d');

    // 기존 차트 제거
    if (currentChart) {
        currentChart.destroy();
    }

    // 새 차트 생성
    currentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: histogramData.labels,
            datasets: [{
                label: '가격 분포',
                data: histogramData.values,
                backgroundColor: 'rgba(79, 70, 229, 0.6)',
                borderColor: 'rgba(79, 70, 229, 1)',
                borderWidth: 2,
                borderRadius: 8,
                hoverBackgroundColor: 'rgba(79, 70, 229, 0.8)',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function (context) {
                            return '상품 수: ' + context.parsed.y + '개';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0,
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 11
                        },
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        display: false
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// 가격 목록 표시
function displayPriceList(prices) {
    const priceListDiv = document.getElementById('priceList');
    priceListDiv.innerHTML = '';

    prices.forEach((price, index) => {
        const priceItem = document.createElement('div');
        priceItem.className = 'price-item fade-in';
        priceItem.style.animationDelay = `${index * 0.03}s`;
        priceItem.textContent = price.toLocaleString() + '원';
        priceListDiv.appendChild(priceItem);
    });
}

// ================================================================
// 저장 버튼 상태 업데이트
// ================================================================
function updateSaveButton(savedFilename) {
    const saveBtn = document.querySelector('.action-buttons button');
    if (saveBtn && savedFilename) {
        saveBtn.innerHTML = '✅ 자동 저장됨';
        saveBtn.style.background = '#10B981';
        saveBtn.title = `저장 완료: ${savedFilename}`;
        // 3초 후 원래 상태로 복구
        setTimeout(() => {
            saveBtn.innerHTML = '💾 다시 저장';
            saveBtn.style.background = '';
            saveBtn.title = '';
        }, 3000);
    }
}

// 결과 저장
async function saveResult() {
    if (!currentResult) {
        showError('저장할 결과가 없습니다.');
        return;
    }

    try {
        const response = await fetch('/api/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                keyword: currentResult.keyword,
                prices: currentResult.prices,
                stats: currentResult.stats
            })
        });

        const data = await response.json();

        if (data.success) {
            showSuccess(`결과가 ${data.filename}으로 저장되었습니다.`);
            setTimeout(() => loadHistory(), 500);
        } else {
            throw new Error(data.error);
        }

    } catch (error) {
        console.error('저장 오류:', error);
        showError('저장 중 오류가 발생했습니다: ' + error.message);
    }
}

// 히스토리 로드
async function loadHistory() {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '<p class="loading">히스토리를 불러오는 중...</p>';

    try {
        const response = await fetch('/api/history');
        const data = await response.json();

        if (data.success && data.history.length > 0) {
            historyList.innerHTML = '';

            data.history.forEach((item, index) => {
                const historyItem = createHistoryItem(item, index);
                historyList.appendChild(historyItem);
            });
        } else {
            historyList.innerHTML = '<p class="loading">저장된 검색 결과가 없습니다.</p>';
        }

    } catch (error) {
        console.error('히스토리 로드 오류:', error);
        historyList.innerHTML = '<p class="loading">히스토리를 불러올 수 없습니다.</p>';
    }
}

// 히스토리 아이템 생성
function createHistoryItem(item, index) {
    const div = document.createElement('div');
    div.className = 'history-item slide-in';
    div.style.animationDelay = `${index * 0.1}s`;
    div.onclick = () => loadHistoryItem(item.filename);

    const stats = item.stats || {};

    div.innerHTML = `
        <div class="history-header">
            <div class="history-keyword">🔍 ${item.keyword}</div>
            <div class="history-date">📅 ${item.date}</div>
        </div>
        <div class="history-stats">
            <div class="history-stat">
                📊 개수: <strong>${(stats.count || 0).toLocaleString()}</strong>
            </div>
            <div class="history-stat">
                💰 평균: <strong>${Math.round(stats.average || 0).toLocaleString()}원</strong>
            </div>
            <div class="history-stat">
                ⬆️ 최고: <strong>${(stats.max || 0).toLocaleString()}원</strong>
            </div>
            <div class="history-stat">
                ⬇️ 최저: <strong>${(stats.min || 0).toLocaleString()}원</strong>
            </div>
        </div>
    `;

    return div;
}

// 히스토리 아이템 불러오기
async function loadHistoryItem(filename) {
    try {
        const response = await fetch(`/api/load/${filename}`);
        const result = await response.json();

        if (result.success && result.data) {
            const data = result.data;

            // 검색창에 키워드 표시
            document.getElementById('searchInput').value = data.keyword;

            // 히스토그램 데이터 생성
            const prices = data.prices || [];
            const histogramData = createHistogramFromPrices(prices);

            // 결과 표시
            currentResult = {
                keyword: data.keyword,
                stats: data.statistics,
                prices: prices,
                histogram: histogramData
            };

            displayResults(currentResult);
            showSuccess(`"${data.keyword}" 검색 결과를 불러왔습니다.`);

            // 상단으로 스크롤
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            throw new Error(result.error || '파일을 불러올 수 없습니다.');
        }

    } catch (error) {
        console.error('불러오기 오류:', error);
        showError('결과를 불러오는 중 오류가 발생했습니다: ' + error.message);
    }
}

// 가격 배열에서 히스토그램 데이터 생성
function createHistogramFromPrices(prices) {
    if (!prices || prices.length === 0) {
        return { labels: [], values: [] };
    }

    const min = Math.min(...prices);
    const max = Math.max(...prices);
    const binCount = 20;
    const binSize = (max - min) / binCount;

    const bins = new Array(binCount).fill(0);
    const labels = [];

    // 구간별 개수 계산
    prices.forEach(price => {
        const binIndex = Math.min(Math.floor((price - min) / binSize), binCount - 1);
        bins[binIndex]++;
    });

    // 레이블 생성
    for (let i = 0; i < binCount; i++) {
        const binStart = Math.round(min + i * binSize);
        labels.push(binStart.toLocaleString());
    }

    return {
        labels: labels,
        values: bins
    };
}

// UI 유틸리티 함수
function showResults() {
    document.getElementById('resultSection').style.display = 'block';
}

function hideResults() {
    document.getElementById('resultSection').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = '❌ ' + message;
    errorDiv.style.display = 'block';

    // 3초 후 자동 숨김
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    document.getElementById('errorMessage').style.display = 'none';
}

function showSuccess(message) {
    // 임시 성공 메시지 표시
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.5s ease-out;
        font-weight: 600;
    `;
    successDiv.textContent = '✅ ' + message;
    document.body.appendChild(successDiv);

    // 3초 후 제거
    setTimeout(() => {
        successDiv.style.animation = 'fadeOut 0.5s ease-out';
        setTimeout(() => {
            document.body.removeChild(successDiv);
        }, 500);
    }, 3000);
}

// 콘솔 로그 스타일
console.log('%c🎨 상품 가격 분석 대시보드', 'color: #4F46E5; font-size: 20px; font-weight: bold;');
console.log('%c버전: 1.1 | Computing Thinking Term Project', 'color: #6B7280; font-size: 12px;');
