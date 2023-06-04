# Бот "Провидение"

## Содержание
1. [О чём проект?](#about)
2. [Структура проекта](#structure)
3. [Подготовка к запуску](#start)

    3.1. [Настройка poetry](#poetry)

    3.2. [Настройка pre-commit](#pre-commit)

    3.3. [Настройка переменных окружения](#env)

4. [Запуск бота](#run-bot)

    4.1. [Запуск проекта локально](#run-local)

    4.2. [Запуск в Docker](#run-docker)

    4.3. [GitHub Actions](#git-actions)

<br><br>

# 1. О чём проект? <a id="about"></a>

#### Проект телеграм-бота, который позволяет разгрузить кураторов/координаторов фонда [“Провидение”](https://fond-providenie.ru/), максимально автоматизировать процессы по взаимодействию с родителями и волонтерами.

...


# 2. Структура проекта <a id="structure"></a>

| Имя               | Описание                               |
|-------------------|----------------------------------------|
| .data             | Директория для хранения логов проекта. |
| bot               | ...                                    |
| bot/conversations | ...                                    |
| core              | ...                                    |
| src               | ...                                    |

# 3. Подготовка к запуску <a id="start"></a>

Примечание: использование Poetry и pre-commit при работе над проектом
обязательно.

## 3.1. Poetry (инструмент для работы с виртуальным окружением и сборки пакетов)<a id="poetry"></a>:

Poetry - это инструмент для управления зависимостями и виртуальными окружениями, также может использоваться для сборки пакетов. В этом проекте Poetry необходим для дальнейшей разработки приложения, его установка <b>обязательна</b>.<br>

<details>
 <summary>
 Как скачать и установить?
 </summary>

### Установка:

Установите poetry следуя [инструкции с официального сайта](https://python-poetry.org/docs/#installation).
<details>
 <summary>
 Команды для установки:
 </summary>
Для UNIX-систем и Bash on Windows вводим в консоль следующую команду:

> *curl -sSL https://install.python-poetry.org | python -*

Для WINDOWS PowerShell:

> *(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -*
</details>
<br>
После установки перезапустите оболочку и введите команду

> poetry --version

Если установка прошла успешно, вы получите ответ в формате

> Poetry (version 1.3.1)

Для дальнейшей работы введите команду:

> poetry config virtualenvs.in-project true

Выполнение данной команды необходимо для создания виртуального окружения в
папке проекта.

После предыдущей команды создадим виртуальное окружение нашего проекта с
помощью команды:

> poetry install

Результатом выполнения команды станет создание в корне проекта папки .venv.
Зависимости для создания окружения берутся из файлов poetry.lock (приоритетнее)
и pyproject.toml

Для добавления новой зависимости в окружение необходимо выполнить команду

> poetry add <package_name>

_Пример использования:_

> poetry add starlette

Также poetry позволяет разделять зависимости необходимые для разработки, от
основных.
Для добавления зависимости необходимой для разработки и тестирования необходимо
добавить флаг ***--dev***

> poetry add <package_name> --dev

_Пример использования:_

> poetry add pytest --dev

</details>

<details>
 <summary>
 Порядок работы после настройки
 </summary>

<br>

Чтобы активировать виртуальное окружение, введите команду:

> poetry shell

Существует возможность запуска скриптов и команд с помощью команды без
активации окружения:

> poetry run <script_name>.py

_Примеры:_

> poetry run python script_name>.py
>
> poetry run pytest
>
> poetry run black

Порядок работы в оболочке не меняется. Пример команды для Win:

> python src\run_bot.py

Доступен стандартный метод работы с активацией окружения в терминале с помощью команд:

Для WINDOWS:

> source .venv/Scripts/activate

Для UNIX:

> source .venv/bin/activate

</details>

## 3.2. Pre-commit (инструмент автоматического запуска различных проверок перед выполнением коммита)<a id="pre-commit"></a>:

<details>
 <summary>
 Настройка pre-commit
 </summary>
<br>

> pre-commit install

Далее при каждом коммите у вас будет происходить автоматическая проверка
линтером, а так же будет происходить автоматическое приведение к единому стилю.
</details>

## 3.3. Настройка переменных окружения <a id="env"></a>

Перед запуском проекта необходимо создать копию файла
```.env.example```, назвав его ```.env``` и установить значение токена бота

# 4. Запуск бота <a id="run-bot"></a>

### Возможен запуск бота в режимах `polling` или `webhook`.<br>
## 4.1. Запуск проекта локально <a id="run-local"></a>
<details>
 <summary>
 Запуск проекта локально
 </summary>
<br>

### 4.1.1. Запуск в режиме Polling
<br>

```
python src/main.py
```

### 4.1.2. Запуск в режиме Webhook

#### <b>Отладка приложения с ботом в режиме webhook на локальном компьютере требует выполнения дополнительных действий:</b>
<br>
<details>
 <summary>
 Необходимые действия
 </summary><br>

В случае отсутствия сервера с доменным именем и установленным SSL-сертификатом, для отладки приложения можно воспользоваться <a href="https://ngrok.com/">ngrok</a> для построения туннеля до вашего компьютера.<br>
Для этого необходимо:
 - Скачать и установить <a href="https://ngrok.com/">ngrok</a>
 - Зарегистрироваться в сервисе <a href="https://ngrok.com/">ngrok</a> и получить <a href="https://dashboard.ngrok.com/get-started/your-authtoken">токен</a>
 - Зарегистрировать полученный токен на локальном комьютере

 ```
 ngrok config add-authtoken <ваш токен>
 ```
 - Запустить тоннель ngrok
 ```
 ngrok http 8000 --host-header=site.local
 ```
 - Скопировать из консоли адрес (`https`), предоставленный сервисом `ngrok`, в переменную окружения `APPLICATION_URL`:
 ```
 APPLICATION_URL=https://1234-56-78-9.eu.ngrok.io # пример
 ```
 - Запустить приложение с ботом в режиме webhook (см. выше)
  ```
python src/run_webhook_api.py
 ```

Более подробная информация об использовании сервиса ngrok доступна на <a href="https://ngrok.com/">официальном сайте</a>
</details>

<br>


```
python src/run_webhook_api.py
```


</details>

## 4.2. Запуск проекта в Docker <a id="run-docker"></a>
<details>
 <summary>
 Запуск проекта через Docker
 </summary>
<br>
Можно запустить бота через docker-compose в тестовом режиме. Для этого в корневой папке проекта выполнить команду

```
docker-compose up -d --build
```

</details>

## 4.3. GitHub Actions деплой на удаленный сервер <a id="git-actions"></a>
<details>
 <summary>
 Запуск проекта на сервере в docker-контейнере
 </summary>
<br>
Workflow:

  * `tests` - проверка кода на соответствие стандарту PEP8;
  * `deploy` - автоматический деплой проекта на боевой сервер;

Подготовьте сервер:
1. Войдите на свой удаленный сервер в облаке.
2. Установите `docker`:
```
sudo apt install docker.io
```
3. Установите docker-compose, с этим вам поможет официальная [документация](https://docs.docker.com/compose/install/).
4. В репозитории на Гитхабе добавьте данные в `Settings -> Secrets -> Actions -> New repository secret`:
```
DOCKER_USERNAME - ваш username на dockerhub
DOCKER_PASSWORD - ваш пароль на dockerhub

USER - имя пользователя для подключения к серверу
HOST - IP-адрес вашего сервера
SSH_KEY - скопируйте приватный ключ с компьютера, имеющего доступ к боевому серверу (cat ~/.ssh/id_rsa)
PASSPHRASE - если при создании ssh-ключа вы использовали фразу-пароль, то сохраните её в эту переменную

TELEGRAM_TOKEN=5274023561:AAH3lUgvoGvLN51wtMze_ZGrTO0RRHGTuJM
EMAIL_BOT=bot_mail@mail.ru
EMAIL_BOT_PASSWORD=EmailPassword
EMAIL_CURATOR=curator_mail@mail.ru
LOG_LEVEL=INFO
```

</details>
