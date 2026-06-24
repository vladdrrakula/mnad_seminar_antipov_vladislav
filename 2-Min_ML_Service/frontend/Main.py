import streamlit as st
import requests

st.set_page_config(page_title="ML Predictor", layout="wide")
st.title("🏠 Предсказание на основе моей ML-модели")
st.markdown("Введите 9 признаков объекта недвижимости и получите предсказание.")

with st.form("prediction_form"):
    st.subheader("Признаки объекта")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        level = st.number_input("level (уровень/этаж)", value=1.0, step=0.5)
        levels = st.number_input("levels (всего этажей)", value=5.0, step=1.0)
        rooms = st.number_input("rooms (комнаты)", value=2.0, step=1.0)
    
    with col2:
        area = st.number_input("area (площадь)", value=50.0, step=1.0)
        kitchen_area = st.number_input("kitchen_area (кухня)", value=10.0, step=0.5)
        building_type = st.number_input("building_type (тип здания)", value=1.0, step=1.0)
    
    with col3:
        object_type = st.number_input("object_type (тип объекта)", value=0.0, step=1.0)
        level_last = st.number_input("level_last (последний этаж?)", value=0.0, step=1.0)
        level_first = st.number_input("level_first (первый этаж?)", value=0.0, step=1.0)

    submitted = st.form_submit_button("🔮 Получить предсказание", use_container_width=True)

if submitted:
    payload = {
        "level": level,
        "levels": levels,
        "rooms": rooms,
        "area": area,
        "kitchen_area": kitchen_area,
        "building_type": building_type,
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
            st.metric(label="Предсказанное значение", value=f"{result['prediction']:.2f}")
        else:
            st.error(f"❌ Ошибка сервера: {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("🚫 Не удалось подключиться к серверу. Запущен ли бэкенд (uvicorn)?")
    except Exception as e:
        st.error(f"⚠️ Непредвиденная ошибка: {str(e)}")
