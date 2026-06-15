Учебный проект, который объединяет в себе последовательные шаги по созданию ML-сервиса на Streamlit c эндпойнтами на FastAPI и связь с БД

Перед первым запуском создание БД:
* > python utils/init_db.py

Для запуска (из папки проекта):
* > uvicorn backend.api:app --reload
* > streamlit run frontend/Main.py

Смотрим:
* > http://localhost:8501/
* > http://localhost:8000/docs