# Получение уведомлений о проверке работ Devman

Данный проект состоит из двух ботов. Бот умеет распознавать речь с помощью агента из [DialogFlow](https://dialogflow.cloud.google.com/#/getStarted) и отвечает на вопросы, задаваемы пользователю.
Один бот выполнен в телеграмме(@FisklessSpeechRecognitionBot), другой во [ВКонтакте](https://vk.com/im?sel=-207767994) 
Данный проект запущен на сервере [Heroku](https://id.heroku.com/login)

## Запуск

Для запуска скрипта у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой 
    ```sh
    pip install -r requirements.txt
    ```
- Запуск бота в ВК производится командой: 
    ```sh
    python3 vk_bot.py
    ```
- Запуск бота в телеграмме производится командой: 
    ```sh
    python3 tg_bot.py
    ```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. 
Чтобы их определить, создайте файл `.env` рядом с `main.py` 
и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Используются следующие переменные окружения: 
- `TELEGRAM_BOT_TOKEN` - токен, созданного вами Telegram-бота для оповещений о проверке работ. Чтобы его получить, необходимо написать Отцу ботов в Telegram(@BotFather). 
Отец ботов попросит ввести два имени. Первое — как он будет отображаться в списке контактов, можно написать на русском. Второе — имя, по которому бота можно будет найти в поиске. Должно быть английском и заканчиваться на bot (например, notification_bot)
- `DIALOG_FLOW_PROJECT_ID` - id проекта DialogFlow, который вы получили, когда создавали проект. 
Для создания проекта DialogFlow, перейдите по [ссылке](https://cloud.google.com/dialogflow/es/docs/quick/setup)
Для создания агента DialogFlow, перейдите по [ссылке](https://cloud.google.com/dialogflow/es/docs/quick/build-agent), причем при создании агента, необходимо ввести индентификатор только что созданного проекта DialogFlow.
- `VK_GROUP_TOKEN` - это ваш персональный токен созданной вами группы ВКонтакте.  Для его получения зайдите в вашу группу ВК -> вкладка Управление в правой части страницы -> Настройки -> Работа с API -> Создать ключ.
- `GOOGLE_APPLICATION_CREDENTIALS` - переменная, где лежит путь до файла с вашим JSON-ключом. Для получения JSON-клоюча перейдите по [ссылке](https://cloud.google.com/docs/authentication/getting-started)


## Функционал проекта

### Возможности скрипта creating_indent

В разделе про переменные окружения, было показано, как создать агента DialogFlow через сайт. На сайте есть возможность создать intent для обучения бота. 
Данный скрипт позволяет обучать бота, с помощью кода. Скрипт считывает данные из файла `requests.json` и на их основе обучается отвечать на определенные вопросы.
Для добавления своих фраз, необходимо в файл requests.json поместить данные вида:
  ```sh
    {
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
      },
    }
  ```


## Инструкция по запуску на сервере

- Зарегистрироваться на [Heroku](https://id.heroku.com/login) и создать приложение
- Привязать аккаунт Github к аккаунту Heroku на вкладке Deploy. Потом найдите свой репозиторий с помощью поиска и подключите его к Heroku.
- Отредактировать файл Procfile в репозитории, чтобы он был следующего вида:
  ```sh
      bot-vk: python3 название_бота_вконтакте.py
      bot-tg: python3 название_бота_телеграмм.py
  ```
- На вкладке Settings вашего приложения в графе Config Vars добавить переменные окружения из вашего ранее созданного .env файла.
Способ поместить `GOOGLE_APPLICATION_CREDENTIALS` хорошо описан [здесь](https://stackoverflow.com/questions/47446480/how-to-use-google-api-credentials-json-on-heroku#:~:text=I%20spent%20an%20entire%20day%20to%20find%20the%20solution%20because%20it%27s%20tricky.%20No%20matter%20your%20language%2C%20the%20solution%20will%20be%20the%20same). 
Обратите внимание, что билдпак, указанный в ответе устарел. 
Замените его на билдпак, представленный в описании
- Установите себе консольный клиент [Heroku LCI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install). Он покажет, есть ли какие-либо ошибки, мешающие запуску скрипта на сервере
- На вкладке Deploy вашего приложения в графе Manual Deploy нажмите Deploy Branch. 
- Наслаждайтесь работой скрипта. В случае каких-либо ошибок загляните в Heroku LCI.


## Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).