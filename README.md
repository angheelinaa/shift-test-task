## SHIFT Test Task
REST-сервис для просмотра текущей зарплаты и даты следующего
повышения. Из-за того, что такие данные очень важны и критичны, каждый
сотрудник может видеть только свою сумму. Для обеспечения безопасности реализован метод, где по логину и паролю сотрудника будет выдан
секретный токен, который действует в течение определенного времени. Запрос
данных о зарплате должен выдаваться только при предъявлении валидного токена.

### Требования к решению
Обязательные технические требования:

* код размещен и доступен в публичном репозитории на GitLab;

* оформлена инструкция по запуску сервиса и взаимодействию с проектом;

* сервис реализован на FastAPI.

Необязательные технические требования (по возрастанию трудоемкости):

* зависимости зафиксированы менеджером зависимостей poetry;

### Запуск
1. Клонируйте репозиторий 
```bash
git clone https://github.com/angheelinaa/SHIFT_Test_Task.git
```

2. Перейдите в директорию проекта и при необходимости измените файл `.env`

3. Установите зависимости (убедитесь, что установлен poetry, иначе воспользуйтесь `pip install poetry`)
```bash
poetry install
```

4. Запустите приложение
```bash
python main.py
```

Перейдите по адресу ` http://127.0.0.1:8000` или откройте интерактивную документацию для удобства `http://127.0.0.1:8000/docs/`

Администратор будет создан автоматически (username: admin, password: admin)

### Endpoints
 * **/users/** - POST запрос для создания пользователя
 * **/users/** - GET запрос для получения информации по всем пользователям
 * **/users/{user_id}** - GET запрос для получения информации по пользователю с определенным **user_id**

 * **/login/** - POST запрос для аутентификации пользователя и получения токена
 * **/salary_info/** - GET запрос, по которому при предъявлении валидного токена выдаются данные о зарплате пользователя

 * **/disable/{username}** - PATCH запрос для дезактивации пользователя с определенным **username**
 * **/salary/{username}** - PATCH запрос для изменения информации о зарплате пользователя с определенным **username**

### Примеры запросов
Сначала авторизуйтесь как администратор. Для этого нажмите кнопку Authorize и введите username: admin, password: admin.


![img.png](img.png)

![img_1.png](img_1.png)

1. Создание пользователя
* Endpoint: /users/
* Permission: admin
* Method: POST
* Response:
```json
{
  "hashed_password": "$2b$12$x08hlZIlwvKbUAsAzVd1WO60xQGn85UPVWkQTRIVIi3kJHDMHTABa",
  "full_name": "Павел Лукашевич",
  "promotion_date": "2024-10-15",
  "role": "user",
  "username": "paluk",
  "id": 2,
  "salary": 50000,
  "is_active": true
}
```

2. Получение информации по всем пользователям
* Endpoint: /users/
* Permission: admin
* Method: GET
* Response:
```json
[
  {
    "username": "admin",
    "full_name": "admin",
    "salary": null,
    "promotion_date": null,
    "id": 1,
    "role": "admin",
    "is_active": true
  },
  {
    "username": "paluk",
    "full_name": "Павел Лукашевич",
    "salary": 50000,
    "promotion_date": "2024-10-15",
    "id": 2,
    "role": "user",
    "is_active": true
  }
]
```

3. Получение информации по определенному пользователю
* Endpoint: /users/{user_id}
* Permission: admin
* Method: GET
* Response:
```json
{
  "username": "paluk",
  "full_name": "Павел Лукашевич",
  "salary": 50000,
  "promotion_date": "2024-10-15",
  "id": 2,
  "role": "user",
  "is_active": true
}
```

4. Получение токена
* Endpoint: /login/
* Method: POST
* Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYWx1ayIsImV4cCI6MTcxNTE5NjQxOX0.r-H1VLp9lwq9NMGJdoNTA2Pst21VQbV2E0ro-D1TSx0",
  "token_type": "Bearer"
}
```

5. Получение информации о зарплате пользователя при предъявлении валидного токена

Теперь аутентифицируемся как пользователь. Снова нажмем на кнопку Authorize и нажмем Logout.
Введем данные созданного пользователя: username: paluk, password: 1234.
* Endpoint: /salary_info/
* Method: GET
* Response:
```json
{
  "username": "paluk",
  "full_name": "Павел Лукашевич",
  "salary": 50000,
  "promotion_date": "2024-10-15"
}
```

6. Изменение информации о зарплате пользователя

Авторизуемся снова как администратор

* Endpoint: /salary/{username}
* Permission: admin
* Method: PATCH
* Response:
```json
{
  "username": "paluk",
  "full_name": "Павел Лукашевич",
  "salary": 100000,
  "promotion_date": "2024-11-22",
  "id": 2,
  "role": "user",
  "is_active": true
}
```

7. Дезактивация пользователя

* Endpoint: /disable/{username}
* Permission: admin
* Method: PATCH
* Response:
```json
{
  "username": "paluk",
  "full_name": "Павел Лукашевич",
  "salary": 100000,
  "promotion_date": "2024-11-22",
  "id": 2,
  "role": "user",
  "is_active": false
}
```

