# Wallet API

## Описание

**Wallet API** — REST API для управления электронными кошельками, позволяющее выполнять операции пополнения и снятия
средств, а также получать баланс кошелька.

---

## Содержание

1. [Технологический стек](#технологический-стек)
2. [Установка и запуск](#установка-и-запуск)
    - [Клонирование репозитория](#клонирование-репозитория)
    - [Создание `.env` файла](#создание-env-файла)
    - [Запуск приложения](#запуск-приложения)
3. [Тестирование](#тестирование)
4. [Эндпоинты API](#эндпоинты-api)
5. [Миграции базы данных](#миграции-базы-данных)
    - [Django Migrations](#django-migrations)
    - [Liquibase](#liquibase)
6. [Структура проекта](#структура-проекта)
7. [Особенности реализации](#особенности-реализации)
8. [Автор](#автор)

---

## Технологический стек

Проект построен с использованием следующих технологий:

- **Backend**: Django, Django REST Framework
- **Язык программирования**: Python 3.11
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker, Docker Compose
- **Миграции (опционально)**: Liquibase
- **Тестирование**: Pytest
- **HTTP API**: REST
---

## Установка и запуск

### Клонирование репозитория

Клонируйте проект с GitHub и перейдите в директорию проекта:

```bash
    git clone <repository_url>
    cd <project_name>
```

### Создание `.env` файла

Создайте файл `.env` в корне проекта и укажите необходимые параметры:

```env
# Настройки приложения
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*

# Настройки базы данных
POSTGRES_DATABASE=wallet_app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Параметры приложения
BACKEND_SERVER_PORT=8000
```

### Запуск приложения

Запустите приложение с помощью Docker Compose:

```bash
    docker-compose up --build
```

Приложение станет доступно по адресу: [http://localhost:8000](http://localhost:8000).

---

## Тестирование
### Общее тестирование. 
Для запуска всех тестов используйте команду:
```bash
    docker-compose exec web coverage run --source='.' manage.py test
```
Для генерации отчета покрытия тестами используйте:
```bash
    docker-compose exec web coverage report
```

### Выборочное тестирование:
Для запуска тестов кошелька выполните команду:

```bash
    docker-compose exec web python manage.py test wallet.tests.WalletServiceTests
```

Для запуска тестов пользователя выполните команду:

```bash
    docker-compose exec web python manage.py test users.tests.UserViewSetTestCase
```
---
>[Коллекция Postman](https://drive.google.com/file/d/1MDvakvf_vothPGOLSy5_uZZjgK1Fv8z7/view?usp=sharing) 
> для быстрой проверки основного функционала.
---

## Эндпоинты API

При создании пользователя автоматически создается кошелек.

### 1. POST `/api/v1/users/`

- **Описание**: Создание нового пользователя.
- **Тело запроса**:

   ```JSON
   {
       "email": "user@example.com",
       "password": "password123",
       "first_name": "Super",
       "last_name": "User"
   }
   ```
- **Пример запроса:**
   ```Bash
   curl -X POST http://localhost:8000/api/v1/users/ \
   -H "Content-Type: application/json" \
   -d '{
           "email": "user@example.com",
           "password": "password123",
           "first_name": "Super",
           "last_name": "User"
        }'
   ```
- **Пример ответа:**
   ```JSON
   {
       "id": 2,
       "email": "user@example.com",
       "first_name": "Super",
       "last_name": "User"
   }
   ```

- **Статус-коды**:
  - `201 Created`: Пользователь успешно создан.
  - `400 Bad Request`: Некорректные данные в запросе.

### 2. GET `/api/v1/wallets/`

- **Описание**: Получение списка всех кошельков пользователя.
- **Пример запроса:**
   ```Bash
   curl -X GET http://localhost:8000/api/v1/wallets/
   ```
- **Пример ответа:**
   ```JSON
   [
    {
        "wallet_id": "e3f9c1d7-9d75-4c8d-8c3f-4a2a6c6d7a3f",
        "balance": 5000
    },
    {
        "wallet_id": "278e0e9d-098e-43d4-bd40-e016c7c7363d",
        "balance": 3000
    }
   ]
   ```

- **Статус-коды**:
  - `200 OK`: Успешный запрос.

### 3. POST `/api/v1/wallets/<WALLET_UUID>/operation/`

- **Описание**: Выполнение операции пополнения (DEPOSIT) или снятия (WITHDRAW) средств с кошелька.
- **Тело запроса**:
   ```JSON
   {
       "operation_type": "DEPOSIT", // или "WITHDRAW"
       "amount": 500 // положительное целое число
   }
   ```
- **Пример запроса (Пополнение):**
   ```Bash
   curl -X POST http://localhost:8000/api/v1/wallets/278e0e9d-098e-43d4-bd40-e016c7c7363d/operation/ \
    -H "Content-Type: application/json" \
    -d '{
          "operation_type": "DEPOSIT",
          "amount": 500
        }'
   ```
- **Пример запроса (Снятие):**
   ```Bash
   curl -X POST http://localhost:8000/api/v1/wallets/278e0e9d-098e-43d4-bd40-e016c7c7363d/operation/
  -H "Content-Type: application/json"
  -d '{
           "operation_type": "WITHDRAW",
           "amount": 100
  }'
   ```
- **Пример ответа:**
   ```JSON
    {
        "message": "Операция выполнена успешно."
    }
   ```
  
- **Статус-коды**:
  - `200 OK`: Успешный запрос.
  - `404 Not Found`: Кошелек не найден.
  - `400 Bad Request`: Некорректный запрос (например, недостаточно средств или неверный формат).

### 4. GET `/api/v1/wallets/<WALLET_UUID>/`

- **Описание**: Получение текущего баланса кошелька.
- **Тело запроса**:
   ```Bash
   curl -X GET http://localhost:8000/api/v1/wallets/278e0e9d-098e-43d4-bd40-e016c7c7363d/
   ```

- **Пример ответа:**
   ```JSON
    {
       "wallet_id": "278e0e9d-098e-43d4-bd40-e016c7c7363d",
       "balance": 500
    }
   ```
  
- **Статус-коды**:
  - `200 OK`: Успешный запрос.
  - `404 Not Found`: Кошелек не найден.
  - `400 Bad Request`: Некорректный запрос (например, недостаточно средств или неверный формат).

### 5. GET `/api/v1/wallets/<WALLET_UUID>/info/`

- **Описание**: Получение подробной информации о кошельке.
- **Тело запроса**:
   ```Bash
   curl -X GET http://localhost:8000/api/v1/wallets/278e0e9d-098e-43d4-bd40-e016c7c7363d/info/ 
   ```

- **Пример ответа:**
   ```JSON
    {
    "wallet_id": "278e0e9d-098e-43d4-bd40-e016c7c7363d",
    "balance": 500,
    "owner": "Bella Doe",
    "created_at": "2023-10-05T12:34:56Z"
    }
   ```
  
- **Статус-коды**:
  - `200 OK`: Успешный запрос.
  - `404 Not Found`: Кошелек не найден.
  - `400 Bad Request`: Некорректный запрос (например, недостаточно средств или неверный формат).


## Миграции базы данных

Проект поддерживает два подхода к управлению миграциями:

### Django Migrations

Используйте встроенный механизм миграций Django:

```shell
    python manage.py makemigrations
    python manage.py migrate
```

### Liquibase

Для более сложных сценариев используйте Liquibase.

**Генерация changelog.xml:**

```shell
    liquibase --url=jdbc:postgresql://localhost:5432/wallet_app --username=postgres --password=your_password generate-changelog --output-file=resources/changelog.xml
```

**Применение изменений:**

```shell
  liquibase update
```

---

## Структура проекта

```plaintext
├── config/                     # Конфигурация проекта Django
│   ├── asgi.py                 # ASGI-приложение для запуска через ASGI-сервер (например, Daphne, Uvicorn)
│   ├── settings.py             # Основные настройки проекта
│   ├── urls.py                 # Главный роутер проекта
│   └── wsgi.py                 # WSGI-приложение для запуска через WSGI-сервер (например, Gunicorn)
│
├── resources/                  # Ресурсы для Liquibas 
│   ├── changelog.xml           # Структура базы данных, сгенерированная Liquibase 
│   ├── liquibase.properties    # Настройки Liquibase 
│   └── postgresql-42.6.2.jar   # JDBC драйвер для PostgreSQL 
│
├── wallet/                     # Приложение для работы с кошельками
│   ├── api/                    # Реализация API
│   │   ├── urls.py             # Роуты API для кошельков
│   │   ├── serializers.py      # Сериализаторы для API
│   │   └── views.py            # Обработчики запросов
│   ├── models.py               # Модели базы данных 
│   ├── tests.py                # Тесты для приложения Wallet
│   └── migrations/             # Миграции для базы данных
│
├── users/                      # Приложение для управления пользователями
│   ├── api/                    # Реализация API
│   │   ├── urls.py             # API routes
│   │   ├── serializers.py      # API serializers
│   │   └──views.py            # API views (ViewSet'ы, CBV, etc.)
│   ├── models.py               # Модель пользователя
│   ├── serializers.py          # Сериализаторы для пользователей
│   ├── views.py                # Обработчики запросов
│   ├── tests.py                # Тесты для приложения Users
│   ├── urls.py                 # Роуты для пользователей
│   └── migrations/             # Миграции для базы данных
│
├── docker-compose.yml          # Конфигурация Docker Compose
├── Dockerfile                  # Dockerfile для сборки контейнера приложения
├── manage.py                   # Утилита для управления проектом Django
├── README.md                   # Документация проекта
├── requirements.txt            # Список зависимостей Python
└── .gitignore                  # Файл для исключения файлов из Git
```

---

## Особенности реализации

1. **Конкурентная среда**:
    - Используются транзакции PostgreSQL (`SELECT ... FOR UPDATE`) для предотвращения конфликтов при одновременных
      запросах.

2. **Обработка ошибок**:
    - Валидация входящих данных.
    - Подробные сообщения об ошибках для пользователей (например, недостаточно средств).

3. **Параметризация**:
    - Все настройки выносятся в `.env` файл, что позволяет менять параметры без пересборки контейнеров.

4. **Docker**:
    - Приложение и база данных запускаются в отдельных контейнерах.
    - Конфигурация через `docker-compose.yml`.

5. **Миграции**:
    - Используются Django миграции и опционально Liquibase для сложных сценариев.

---

## Автор

**Angelina Khalueva**  
📧 dev.patient.zero@gmail.com
