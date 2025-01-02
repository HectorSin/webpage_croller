import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

def parse_ajou_notice():
    url = "https://www.ajou.ac.kr/kr/ajou/notice.do?mode=list&&articleLimit=10&article.offset=0"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    table_body = soup.select_one("table.board-table tbody")
    if not table_body:
        return pd.DataFrame()

    rows = table_body.select("tr")
    data = []
    for row in rows:
        cols = row.select("td")
        if len(cols) < 6:
            continue
        no_text = cols[0].get_text(strip=True)
        # '공지'인 경우 또는 숫자가 아니면 제외
        if no_text == "공지" or not no_text.isdigit():
            continue
        category = cols[1].get_text(strip=True)
        title = cols[2].get_text(strip=True)
        date = cols[5].get_text(strip=True)
        data.append({
            "no": no_text,
            "category": category,
            "title": title,
            "date": date
        })
    return pd.DataFrame(data)

def save_new_notices():
    # 1) 신규 데이터 수집
    df_new = parse_ajou_notice()

    # 2) 기존 엑셀 읽어오기
    try:
        df_existing = pd.read_excel("ajou_notice.xlsx")
    except FileNotFoundError:
        df_existing = pd.DataFrame(columns=["no", "category", "title", "date"])

    # 3) 기존 글번호 집합화
    existing_numbers = set(df_existing["no"].astype(str))

    # 4) 새로 들어온 공지 중, 기존에 없는 것만 필터링
    new_rows = df_new[~df_new["no"].astype(str).isin(existing_numbers)]

    # 5) 새 항목을 맨 위에 오도록 결합 후 엑셀 저장
    if not new_rows.empty:
        df_combined = pd.concat([new_rows, df_existing], ignore_index=True)
        df_combined.to_excel("ajou_notice.xlsx", index=False)
        print(f"아주대 공지사항: 새로 추가된 공지 {len(new_rows)}건 저장 완료 (상단에 추가)")
    else:
        print("아주대 공지사항: 새로운 공지가 없습니다.")

if __name__ == "__main__":
    save_new_notices()
