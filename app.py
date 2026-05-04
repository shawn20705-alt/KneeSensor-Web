import streamlit as st
import pandas as pd
import requests

st.title('KneeSensor 六軸原始數據監測')

# ==========================================
# 1. ThingSpeak 連線設定 (⚠️請換成你的資料)
# ==========================================
CHANNEL_ID = '3366273'       # 3366273
READ_API_KEY = '4FWLCIDKMF424SLX'   # 替換成你的讀取金鑰

# ==========================================
# 2. 從雲端抓取 6 軸資料的函數
# ==========================================
def get_raw_data():
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=100"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['feeds'])
        
        if not df.empty:
            # 取出時間與 field1 ~ field6
            df = df[['created_at', 'field1', 'field2', 'field3', 'field4', 'field5', 'field6']]
            # 重新命名為好懂的名稱
            df.columns = ['時間', 'ax', 'ay', 'az', 'gx', 'gy', 'gz']
            
            # 將文字轉換為時間與數字格式
            df['時間'] = pd.to_datetime(df['時間'])
            for col in ['ax', 'ay', 'az', 'gx', 'gy', 'gz']:
                df[col] = pd.to_numeric(df[col])
            
            return df
    return pd.DataFrame()

# ==========================================
# 3. 網頁畫面排版與顯示
# ==========================================
df = get_raw_data()

if not df.empty:
    st.success("✅ 成功連線至 ThingSpeak，取得最新數據！")
    
    # 繪製 加速度計 (Accel) 折線圖
    st.subheader('🏃 加速度變化 (ax, ay, az)')
    st.line_chart(df.set_index('時間')[['ax', 'ay', 'az']])
    
    # 繪製 陀螺儀 (Gyro) 折線圖
    st.subheader('🌪️ 陀螺儀變化 (gx, gy, gz)')
    st.line_chart(df.set_index('時間')[['gx', 'gy', 'gz']])
    
    # 在最下方顯示原始數據表
    st.subheader('📋 原始數據報表')
    st.dataframe(df)
else:
    st.info("🔄 正在等待 ThingSpeak 數據... (如果一直沒畫面，請確認 ESP32 有在發送數據)")