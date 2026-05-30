import streamlit as st
import pandas as pd
import os

# 1. ページの設定（画面を横いっぱいに広く使う）
st.set_page_config(page_title="FXハッキング", layout="wide")

st.title("🚀 FX自動ハッキング・ダッシュボード (視認性特化版)")
st.write("【勝率極大化】通貨強弱 × 大衆比率 × 国債利回り 完全解析システム")

# Excelファイルを100%見つけるセンサー
target_file = "FX_Auto_Hacking_Database_v3.xlsx"
possible_paths = [
    target_file,
    os.path.join(os.path.expanduser("~"), "Desktop", target_file),
    os.path.join(os.path.expanduser("~"), target_file)
]

df_db = None
for path in possible_paths:
    if os.path.exists(path):
        try:
            df_db = pd.read_excel(path, sheet_name="Dashboard")
            break
        except:
            pass

if df_db is not None:
    # 列名自動修復センサー
    found_header = False
    for i in range(min(15, len(df_db))):
        if df_db.iloc[i].astype(str).str.contains("通貨ペア").any():
            new_header = df_db.iloc[i]
            df_db = df_db[i+1:]
            df_db.columns = new_header
            found_header = True
            break

    if found_header:
        # 項目名のNaNを完全に消し去る
        cleaned_columns = []
        for idx, col in enumerate(df_db.columns):
            col_str = str(col).strip()
            if pd.isna(col) or col_str == "nan" or col_str == "":
                cleaned_columns.append(f"未定義_{idx}")
            else:
                cleaned_columns.append(col_str)
        df_db.columns = cleaned_columns

        # 「通貨ペア」という列が安全に存在する場合
        if "通貨ペア" in df_db.columns:
            # データ内の空白を徹底排除
            df_clean = df_db.dropna(subset=["通貨ペア"]).copy()
            df_clean = df_clean[df_clean["通貨ペア"].astype(str).str.strip() != ""]
            df_clean = df_clean.fillna("-")
            df_clean = df_clean.reset_index(drop=True)
            
            # 2. 画面の描画処理（最上部のアラート）
            st.subheader("🚨 現在のリアルタイムアラート")
            
            col1 = "①金利×価格 乖離度" if "①金利×価格 乖離度" in df_clean.columns else None
            col2 = "②強弱×比率 乖離度" if "②強弱×比率 乖離度" in df_clean.columns else None
            
            has_alert = False
            if col1 or col2:
                cond = pd.Series(False, index=df_clean.index)
                if col1: cond = cond | df_clean[col1].astype(str).str.contains("★")
                if col2: cond = cond | df_clean[col2].astype(str).str.contains("★")
                alert_rows = df_clean[cond]
                
                if not alert_rows.empty:
                    for index, row in alert_rows.iterrows():
                        strategy = row.get("相関＆乖離の総合戦略判定（シグナル）", "戦略を確認中")
                        st.warning(f"【限界乖離発生！】 🔥 {row['通貨ペア']} が大チャンス！ 【戦略】：{strategy}")
                        has_alert = True
                        
            if not has_alert:
                st.success("現在、大口の罠・大衆のパニックは検知されていません。監視体制を維持します。")
            
            # 💡【今回の超重大リフォーム！】
            # 文字が切れる表形式をやめて、1通貨ペアずつ綺麗に「カード形式」で並べます。
            # これにより、スマホでも文字が100%自動改行され、絶対に最後まで読めるようになります！
            st.subheader("📊 全通貨ペアの最新ステータス・戦略コメント一覧")
            
            for index, row in df_clean.iterrows():
                pair_name = row["通貨ペア"]
                strategy = row.get("相関＆乖離の総合戦略判定（シグナル）", "-")
                kairi1 = row.get("①金利×価格 乖離度", "-")
                kairi2 = row.get("②強弱×比率 乖離度", "-")
                
                # チャンス度（★が入っているか）に応じてカードの色や目立ち方を変える仕掛け
                is_star = "★" in str(kairi1) or "★" in str(kairi2)
                
                # 見出し部分
                if is_star:
                    header_text = f"🔥 【大チャンス】{pair_name} （①金利:{kairi1} / ②強弱:{kairi2}）"
                else:
                    header_text = f"🔹 {pair_name} （①金利:{kairi1} / ②強弱:{kairi2}）"
                
                # 各通貨ペアを折りたたみ・または枠線で囲んで表示（文字が100%自動改行されます）
                with st.expander(header_text, expanded=is_star):
                    st.markdown(f"**🎯 総合戦略判定（買い・売りの指示）：**")
                    # ここで大きな文字でコメントを表示。絶対に途中で切れません。
                    st.info(strategy)
            
        else:
            st.error("⚠️ Excelファイルの項目名『通貨ペア』が正しく認識できませんでした。")
    else:
        st.error("⚠️ Excelファイルの項目名が見つかりませんでした。")
else:
    st.error("⚠️ Excelファイル自体がパソコン内で見つかりません。")
