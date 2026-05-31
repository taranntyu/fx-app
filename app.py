import streamlit as st
import pandas as pd
import os

# --- 画面の基本設定 ---
st.set_page_config(page_title="FX 自動ハッキングダッシュボード", layout="wide")
st.title("📊 FX 自動ハッキングダッシュボード")

FILE_PATH = "FX_Auto_Hacking_Database_v3.xlsx"

if not os.path.exists(FILE_PATH):
    st.warning(f"⚠️ エクセルファイル（{FILE_PATH}）が見つかりません。")
else:
    try:
        # エクセルを読み込む
        df = pd.read_excel(FILE_PATH)
        
        # 空白や不要な行・列を綺麗に掃除する
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')
        df = df.fillna("")
        
        if df.empty:
            st.info("現在、表示するデータがありません。")
        else:
            st.write("最新の相場分析データです。（項目をタップすると並び替えができます）")
            
            # ✨ ここがポイント！エクセルをそのまま一番綺麗な「表」で表示する魔法
            st.dataframe(
                df,
                use_container_width=True,  # スマホの画面幅にピッタリ合わせる
                height=600  # 表の高さをしっかり確保
            )
                    
    except Exception as e:
        st.error(f"データの読み込み中にエラーが発生しました。詳細: {e}")
