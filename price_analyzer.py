import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pickle
import threading
from typing import List, Dict, Optional


class PriceScraper:
    """다나와 웹사이트에서 가격 데이터를 크롤링하는 클래스"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
            # 검색 요청
            params = {"query": keyword, "tab": "goods"}

            response = requests.get(
                self.base_url, params=params, headers=self.headers, timeout=10
            )
            response.raise_for_status()

            # HTML 파싱
            soup = BeautifulSoup(response.text, "html.parser")

            # 가격 데이터 추출 (정규표현식 사용)
            price_pattern = r"(\d[\d,]*)\s*원"
            text_content = soup.get_text()

            # 모든 가격 패턴 찾기
            matches = re.findall(price_pattern, text_content)

            # 리스트 함축을 사용한 데이터 정제
            prices = [
                int(match.replace(",", ""))
                for match in matches
                if self._is_valid_price(match)
            ]

            # 중복 제거 및 정렬
            prices = sorted(list(set(prices)))

        except requests.exceptions.RequestException as e:
            print(f"네트워크 오류 발생: {e}")
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
            price = int(price_str.replace(",", ""))
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
            return {"average": 0, "max": 0, "min": 0, "count": 0}

        return {
            "average": sum(prices) / len(prices),
            "max": max(prices),
            "min": min(prices),
            "count": len(prices),
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
                keyword = data.get("keyword", "unknown")
                # 파일명에 사용할 수 없는 문자 제거
                safe_keyword = "".join(
                    c for c in keyword if c.isalnum() or c in (" ", "_")
                ).strip()
                safe_keyword = safe_keyword.replace(" ", "_")[:20]  # 최대 20자로 제한
                filename = f"result_{safe_keyword}_{timestamp}.pkl"

            with open(filename, "wb") as f:
                pickle.dump(data, f)

            return filename  # 저장된 파일명 반환
        except Exception as e:
            print(f"파일 저장 오류: {e}")
            raise

    @staticmethod
    def load_results(filename: str = "last_result.pkl") -> Optional[Dict]:
        """
        pickle 파일에서 분석 결과를 불러옵니다.

        Args:
            filename: 불러올 파일명

        Returns:
            저장된 데이터 또는 None
        """
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("저장된 결과 파일이 없습니다.")
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
            plt.rcParams["font.family"] = "AppleGothic"
            plt.rcParams["axes.unicode_minus"] = False
        except:
            try:
                # Windows용 한글 폰트 설정
                plt.rcParams["font.family"] = "Malgun Gothic"
                plt.rcParams["axes.unicode_minus"] = False
            except:
                print("한글 폰트 설정 실패. 기본 폰트를 사용합니다.")

    def plot_histogram(self, prices: List[int], keyword: str):
        """
        가격 분포 히스토그램을 그립니다.

        Args:
            prices: 가격 데이터 리스트
            keyword: 검색 키워드
        """
        if not prices:
            messagebox.showwarning("경고", "시각화할 데이터가 없습니다.")
            return

        try:
            plt.figure(figsize=(10, 6))

            # 히스토그램 생성
            plt.hist(prices, bins=20, color="skyblue", edgecolor="black", alpha=0.7)

            # 차트 설정
            plt.title(f"Price Distribution - {keyword}", fontsize=16, fontweight="bold")
            plt.xlabel("가격 (원)", fontsize=12)
            plt.ylabel("빈도", fontsize=12)
            plt.grid(axis="y", alpha=0.3)

            # 통계선 추가
            avg_price = sum(prices) / len(prices)
            plt.axvline(
                avg_price,
                color="red",
                linestyle="--",
                linewidth=2,
                label=f"평균: {avg_price:,.0f}원",
            )
            plt.legend()

            # 가격 포맷팅
            ax = plt.gca()
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{int(x):,}"))

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"시각화 오류: {e}")
            messagebox.showerror(
                "오류", f"그래프 생성 중 오류가 발생했습니다: {str(e)}"
            )


class PriceAnalyzerGUI:
    """전체 기능을 통합하는 GUI 클래스"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("상품 가격 분석 및 추적 시스템")
        self.root.geometry("700x600")

        # 컴포넌트 초기화
        self.scraper = PriceScraper()
        self.analyzer = DataAnalyzer()
        self.visualizer = Visualizer()

        # 데이터 저장 변수
        self.current_prices = []
        self.current_keyword = ""

        # GUI 구성
        self._setup_gui()

    def _setup_gui(self):
        """GUI 레이아웃을 구성합니다."""

        # 상단 프레임: 검색 영역
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill=tk.X, padx=10)

        tk.Label(top_frame, text="검색 키워드:", font=("Arial", 12)).pack(
            side=tk.LEFT, padx=5
        )

        self.keyword_entry = tk.Entry(top_frame, width=30, font=("Arial", 12))
        self.keyword_entry.pack(side=tk.LEFT, padx=5)
        self.keyword_entry.bind("<Return>", lambda e: self.start_collection())

        self.collect_btn = tk.Button(
            top_frame,
            text="수집 시작",
            command=self.start_collection,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
        )
        self.collect_btn.pack(side=tk.LEFT, padx=5)

        # 중단 프레임: 결과 표시 영역
        middle_frame = tk.Frame(self.root)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(
            middle_frame, text="수집 결과 및 통계:", font=("Arial", 11, "bold")
        ).pack(anchor=tk.W)

        self.result_text = scrolledtext.ScrolledText(
            middle_frame, width=80, height=20, font=("Courier", 10), wrap=tk.WORD
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # 하단 프레임: 기능 버튼들
        bottom_frame = tk.Frame(self.root, pady=10)
        bottom_frame.pack(fill=tk.X, padx=10)

        self.graph_btn = tk.Button(
            bottom_frame,
            text="그래프 보기",
            command=self.show_graph,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            state=tk.DISABLED,
        )
        self.graph_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(
            bottom_frame,
            text="결과 저장",
            command=self.save_results,
            bg="#FF9800",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            state=tk.DISABLED,
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.load_btn = tk.Button(
            bottom_frame,
            text="결과 불러오기",
            command=self.load_results,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(
            bottom_frame,
            text="초기화",
            command=self.clear_results,
            bg="#F44336",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
        ).pack(side=tk.RIGHT, padx=5)

    def start_collection(self):
        """가격 데이터 수집을 시작합니다 (비동기 처리)"""
        keyword = self.keyword_entry.get().strip()

        if not keyword:
            messagebox.showwarning("경고", "검색 키워드를 입력해주세요.")
            return

        self.current_keyword = keyword
        self.collect_btn.config(state=tk.DISABLED, text="수집 중...")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"'{keyword}' 검색 중...\n")
        self.result_text.insert(
            tk.END, "데이터를 수집하고 있습니다. 잠시만 기다려주세요...\n\n"
        )

        # 비동기 처리를 위한 쓰레드 생성
        thread = threading.Thread(target=self._collect_data, args=(keyword,))
        thread.daemon = True
        thread.start()

    def _collect_data(self, keyword: str):
        """실제 데이터 수집을 수행합니다 (백그라운드)"""
        try:
            # 가격 데이터 크롤링
            prices = self.scraper.scrape_prices(keyword)

            # GUI 업데이트는 메인 쓰레드에서
            self.root.after(0, self._update_results, prices)

        except Exception as e:
            self.root.after(0, self._show_error, str(e))

    def _update_results(self, prices: List[int]):
        """수집 결과를 GUI에 업데이트합니다."""
        self.current_prices = prices

        if not prices:
            self.result_text.insert(tk.END, "수집된 가격 데이터가 없습니다.\n")
            self.result_text.insert(tk.END, "다른 키워드로 다시 시도해보세요.")
        else:
            # 통계 계산
            stats = self.analyzer.calculate_statistics(prices)

            # 결과 출력
            self.result_text.insert(tk.END, "=" * 60 + "\n")
            self.result_text.insert(tk.END, f"검색 키워드: {self.current_keyword}\n")
            self.result_text.insert(tk.END, "=" * 60 + "\n\n")

            self.result_text.insert(tk.END, "📊 통계 분석 결과\n")
            self.result_text.insert(tk.END, "-" * 60 + "\n")
            self.result_text.insert(tk.END, f"수집된 가격 개수: {stats['count']:,}개\n")
            self.result_text.insert(tk.END, f"평균 가격: {stats['average']:,.0f}원\n")
            self.result_text.insert(tk.END, f"최고 가격: {stats['max']:,}원\n")
            self.result_text.insert(tk.END, f"최저 가격: {stats['min']:,}원\n")
            self.result_text.insert(
                tk.END, f"가격 범위: {stats['max'] - stats['min']:,}원\n"
            )
            self.result_text.insert(tk.END, "-" * 60 + "\n\n")

            # 가격 리스트 출력 (상위 10개)
            self.result_text.insert(tk.END, "수집된 가격 목록 (일부)\n")
            self.result_text.insert(tk.END, "-" * 60 + "\n")
            for i, price in enumerate(prices[:10], 1):
                self.result_text.insert(tk.END, f"{i:2d}. {price:,}원\n")

            if len(prices) > 10:
                self.result_text.insert(tk.END, f"... 외 {len(prices) - 10}개\n")

            # 버튼 활성화
            self.graph_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)

        self.collect_btn.config(state=tk.NORMAL, text="수집 시작")

    def _show_error(self, error_msg: str):
        """오류 메시지를 표시합니다."""
        self.result_text.insert(tk.END, f"\n오류 발생: {error_msg}\n")
        self.collect_btn.config(state=tk.NORMAL, text="수집 시작")
        messagebox.showerror("오류", error_msg)

    def show_graph(self):
        """히스토그램을 새 창으로 표시합니다."""
        if not self.current_prices:
            messagebox.showwarning("경고", "표시할 데이터가 없습니다.")
            return

        self.visualizer.plot_histogram(self.current_prices, self.current_keyword)

    def save_results(self):
        """현재 결과를 파일로 저장합니다."""
        if not self.current_prices:
            messagebox.showwarning("경고", "저장할 데이터가 없습니다.")
            return

        try:
            stats = self.analyzer.calculate_statistics(self.current_prices)
            data = {
                "keyword": self.current_keyword,
                "prices": self.current_prices,
                "statistics": stats,
            }

            # 자동으로 고유한 파일명 생성
            saved_filename = self.analyzer.save_results(data)
            messagebox.showinfo(
                "성공", f"결과가 '{saved_filename}' 파일로 저장되었습니다."
            )
        except Exception as e:
            messagebox.showerror("오류", f"저장 중 오류가 발생했습니다: {str(e)}")

    def load_results(self):
        """저장된 결과를 불러옵니다."""
        from tkinter import filedialog
        import os

        try:
            # pkl 파일 선택 대화상자
            filename = filedialog.askopenfilename(
                title="결과 파일 선택",
                initialdir=os.getcwd(),
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
            )

            if not filename:
                return  # 사용자가 취소한 경우

            data = self.analyzer.load_results(filename)

            if data is None:
                messagebox.showinfo("알림", "파일을 불러올 수 없습니다.")
                return

            # 데이터 복원
            self.current_keyword = data.get("keyword", "Unknown")
            self.current_prices = data.get("prices", [])
            stats = data.get("statistics", {})

            # 결과 표시
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "📂 저장된 결과를 불러왔습니다.\n\n")

            self._update_results(self.current_prices)

            messagebox.showinfo("성공", "결과를 성공적으로 불러왔습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"불러오기 중 오류가 발생했습니다: {str(e)}")

    def clear_results(self):
        """결과를 초기화합니다."""
        self.result_text.delete(1.0, tk.END)
        self.keyword_entry.delete(0, tk.END)
        self.current_prices = []
        self.current_keyword = ""
        self.graph_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)


def main():
    """메인 실행 함수"""
    root = tk.Tk()
    app = PriceAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
