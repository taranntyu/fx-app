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
        df = pd.read_excel(FILE_PATH)
        
        if df.empty:
            st.info("現在、表示するデータがありません。")
        else:
            # 💡見出しの名前が違っても大丈夫なように、左から順番（位置）でデータを強制取得します
            cols = st.columns(3)
            
            for index, row in df.iterrows():
                col = cols[index % 3]
                with col:
                    # エクセルの A列(0), B列(1), C列(2), D列(3) のデータを順番に抜き出す
                    currency = str(row.iloc[0]) if len(df.columns) > 0 else "不明"
                    judge = str(row.iloc[1]) if len(df.columns) > 1 else "-"
                    importance = str(row.iloc[2]) if len(df.columns) > 2 else ""
                    comment = str(row.iloc[3]) if len(df.columns) > 3 else ""
                    
                    # 買いは赤、売りは青に色分け
                    color = "red" if judge == "買い" else "blue" if judge == "売り" else "black"
                    
                    st.markdown(f"""
                    <div style="border: 2px solid #e6e6e6; border-radius: 10px; padding: 15px; margin-bottom: 15px; background-color: #f9f9f9; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                        <h3 style="margin-top: 0; color: #1f77b4; border-bottom: 2px solid #1f77b4; padding-bottom: 5px;">{currency}</h3>
                        <p style="font-size: 18px; margin: 10px 0;"><strong>判定：</strong> <span style="font-size: 1.3em; font-weight: bold; color: {color};">{judge}</span></p>
                        <p style="font-size: 18px; margin: 10px 0;"><strong>重要度：</strong> <span style="color: #ffaa00; font-size: 1.2em;">{importance}</span></p>
                        <div style="background-color: #ffffff; padding: 10px; border-radius: 5px; border: 1px dashed #ccc;">
                            <p style="margin: 0; font-size: 14px; color: #555;"><strong>📝コメント</strong><br>{comment}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
    except Exception as e:
        st.error(f"データの読み込み中にエラーが発生しました。詳細: {e}")
