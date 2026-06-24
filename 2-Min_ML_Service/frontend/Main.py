import streamlit as st
import requests

st.set_page_config(page_title="ML Predictor", layout="wide")
st.title("🏠 Предсказание стоимости недвижимости")
st.markdown("Введите 9 признаков объекта и получите предсказание.")

with st.form("prediction_form"):
    st.subheader("Введите данные")

    col1, col2, col3 = st.columns(3)
    with col1:
        levels = st.number_input("Количество этажей", value=5.0, step=1.0)
        rooms = st.number_input("Количество комнат", value=3.0, step=1.0)
        area = st.number_input("Общая площадь", value=65.0, step=1.0)
    with col2:
        kitchen_area = st.number_input("Площадь кухни", value=12.0, step=0.5)
        geo_lat = st.number_input("Широта (geo_lat)", value=55.0, step=0.01)
        geo_lon = st.number_input("Долгота (geo_lon)", value=37.0, step=0.01)
    with col3:
        object_type = st.number_input("Тип объекта (object_type)", value=1.0, step=1.0)
        level_last = st.number_input("Последний этаж? (level_last)", value=0.0, step=1.0)
        level_first = st.number_input("Первый этаж? (level_first)", value=0.0, step=1.0)

    submitted = st.form_submit_button("🔮 Получить предсказание", use_container_width=True)

if submitted:
    payload = {
        "levels": levels,
        "rooms": rooms,
        "area": area,
        "kitchen_area": kitchen_area,
        "geo_lat": geo_lat,
        "geo_lon": geo_lon,
        "object_type": object_type,
        "level_last": level_last,
        "level_first": level_first
    }
    try:
        with st.spinner("Модель думает..."):
            response = requests.post("http://localhost:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result['message']}")
            st.metric(label="Предсказанная цена", value=f"{result['prediction']:.2f}")
        else:
            st.error(f"❌ Ошибка сервера: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("🚫 Не удалось подключиться к серверу. Запущен ли бэкенд (uvicorn)?")
    except Exception as e:
        st.error(f"⚠️ Непредвиденная ошибка: {str(e)}")