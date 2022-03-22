import os
import requests
import time
import telegram
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    logging.debug('Бот успешно запущен')
    headers = {'Authorization': f'Token {os.getenv("DEVMAN_TOKEN")}'}
    params = {'timestamp': None}
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=params, timeout=60)
            response.raise_for_status()
            devman_api_response = response.json()
            if devman_api_response['status'] == 'found':
                params['timestamp'] = devman_api_response['last_attempt_timestamp']
                last_attempt = devman_api_response['new_attempts'][0]
                lesson_title, lesson_url = last_attempt['lesson_title'], last_attempt['lesson_url']
                bot.send_message(chat_id=chat_id, text=
                f'У Вас проверили работу "{lesson_title}". Cсылка на работу: {lesson_url}')
            else:
                params['timestamp'] = devman_api_response['timestamp_to_request']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(30)
            pass


if __name__ == '__main__':
    main()
