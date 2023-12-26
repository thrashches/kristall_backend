# kristall_backend

Бэкенд для сайта кондитерской "Кристалл".

## Развертывание приложения

Клонируем репозиторий:
```bash
git clone git@github.com:thrashches/kristall_backend.git
cd kristall_backend/kristall_infra
```

Создаем файл с настройками и запускаем сервисы:
```bash
cp .env.example .env
docker-compose up -d
```

Смотрим как называется сервис с бэком:
```bash
user@host kristall_infra % docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS                    NAMES
5909cc162a53   nginx:alpine             "/docker-entrypoint.…"   4 minutes ago   Up 4 minutes   0.0.0.0:80->80/tcp       kristall_infra-nginx-1
e324d7179c8e   kristall_infra-backend   "gunicorn backend.ws…"   4 minutes ago   Up 4 minutes   0.0.0.0:8000->8000/tcp   kristall_infra-backend-1
58dd82d82338   postgres:16-alpine       "docker-entrypoint.s…"   4 minutes ago   Up 4 minutes   5432/tcp                 kristall_infra-db-1
```

Выполняем миграции и собираем статику:
```bash
docker exec -it kristall_infra-backend-1 python manage.py migrate
docker exec -it kristall_infra-backend-1 python manage.py collectstatic --no-input
docker exec -it kristall_infra-backend-1 python manage.py createsuperuser
```

## Требования к оформлению кода и коммитов

1. Каждый разработчик работает над отдельной фичей в отдельной ветке.
2. Перед началом работы обязательно стянуть текущую master.
3. Ветки под фичи я стараюсь создавать в `Issues` заранее. Принцип именования веток следующий:
    ```
    feature/<название_фичи_на_английском>
    bug/<краткая_суть_бага>
    ```
4. После окончания работы над фичей создаем `pull request`. В названии должно быть понятно что реализовано.
5. При коммите в комментарии должно быть понятно, что сделано в коммите.
6. При закрытии `PullRequest` `Issue` закроется сама. В нее можно отписывать комментарии, как и в задачах проекта.
7. Код должен соответствовать требованиям `pep8`. Длиной строк можно в принципе пренебрегать, используя автонастройку в `pycharm` в 120 символов.
8. Не забывать добавлять зависимости в `requirements.txt`.

## Написание моделей

1. Обязательно унаследовать модель пользователя, чтобы ее можно было изменять, а не расширять (`AbstractUser`).
2. Модули с моделями описаны в задачах.
3. В админку можно заводить по простому, я потом настрою.

## Написание API

1. Крайне желательно использовать `ModelViewSet`.
2. Соблюдать принципы `REST`. Если объект добавлен, то код ответа 201, изменен/данные получены - 200, клиент шлет кривой запрос - 400 и тд.
3. Использовать `swagger`, документация должна быть актуальной. Вести файл с тестами для `postman`.
4. Авторизацию можно сделать в конце.

## Проверка оформления кода `flake8`

```bash
# Из папки backend
flake8
```

Желательно настроить ide для автопроверки, чтобы подчеркивала косяки. Как это натсроить можно почитать [тут](https://melevir.medium.com/pycharm-loves-flake-671c7fac4f52)