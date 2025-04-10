# TF-IDF 

## Функциональные возможности

- **Загрузка файла:** Пользователь может загрузить текстовый файл через веб-интерфейс.
- **Анализ текста:** После загрузки файла приложение производит анализ текста, считая TF и IDF для каждого слова.
- **Отображение результатов:** Результаты выводятся в виде таблицы с колонками: слово, tf, idf.

## Стек технологий

- **Язык программирования:** Python
- **Веб-фреймворк:** Django
- **База данных:** SQLite
- **Фронтенд:** HTML

## Установка и запуск

1. **Клонирование репозитория:**

   ```bash
   git clone https://github.com/royalistofficial/tfidf_project.git
   cd tfidf_project
   ```

2. **Создание и активация виртуального окружения:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/macOS
   venv\Scripts\activate     # Для Windows
   ```

3. **Установка зависимостей:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Применение миграций для создания базы данных:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Запуск сервера:**

   ```bash
   python manage.py runserver
   ```

6. **Доступ к приложению:**

   Перейдите по адресу [http://127.0.0.1:8000/] в браузере.

## Тестирование

Для запуска тестов выполните команду:

```bash
python manage.py test
```


## Структура проекта

```
.
├── manage.py
├── requirements.txt
├── .gitignore
├── app.log
├── tfidf_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── text_processor
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── utils.py
    ├── views.py
    └── templates
        └── text_processor
            ├── base.html
            ├── home.html
            ├── upload.html
            └── results.html
```
