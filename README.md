# API REST сервис Тренажер Английского языка 

Проект является API REST сервисом для подготовки к экзаменам (ЕГЭ и ОГЕ) по английскому языку.

# Стек приложения

## Основной стек

- **Фреймворк**: Django
  - Версия: ~=5.0.2

- **База данных**: MySQL
  - Драйвер: mysqlclient
  - Версия: ~=2.2.4

- **API фреймворк**: Django REST Framework
  - Версия: ~=3.14.0

- **Веб-сервер**: Gunicorn
  - Версия: ~=20.1

## Дополнительные инструменты

- **Библиотека для перечислений**: ChoicesEnum
  - Версия: ~=0.7.0


## Инструменты разработчика (dev-packages)

- **Линтер кода**: Flake8
  - Версия: *

- **Управление переменными окружения**: python-dotenv
  - Версия: *

## Требования

- **Версия Python**: 3.10
- **Полная версия Python**: 3.10.10
- **Pipenv**: 2022.11.11
- **MySQL Server**: 8.3.0
- **docker**: 20.10.20
- **docker-compose**: 2.12.1

# Установка

1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/your_username/english-language-trainer-backend.git
   ```
   
2. Создаём файл .env с переменными окружения(пример описан в файле [.env.example](.env.example)):
  
| Имя                    | Описание                  |
| ---------------------- |---------------------------|
| SECRET_KEY             | Секретный ключ для Django |
| ALLOWED_HOSTS          | Разрешенные IP            |
| DJANGO_SETTINGS_MODULE | Модуль Django             |
| DB_HOST                | Host базы данных          |
| DB_PORT                | Порт базы данных          |
| DB_NAME                | Имя базы данных           |
| DB_USER                | Пользователь              |
| DB_PASS                | Пароль                    |
| DB_ROOT_PASS           | Пароль root пользователя  |

3. Поднимаем контейнер для разработки:
  ```bash
  docker-compose -f docker-compose.dev.yml up --build --detach
  ```