import os
import requests
import telegram


def main():
    chat_id = os.getenv('CHAT_ID')
    bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    headers = {'Authorization': f'Token {os.getenv("DEVMAN_TOKEN")}'}
    params = {'timestamp': None}
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=headers, params=params, timeout=6)
            response.raise_for_status()
            devman_response_data = response.json()
            if devman_response_data['status'] == 'found':
                params['timestamp'] = devman_response_data['last_attempt_timestamp']
                lesson_title = devman_response_data['new_attempts'][0]['lesson_title']
                lesson_url = devman_response_data['new_attempts'][0]['lesson_url']
                bot.send_message(chat_id=chat_id, text=f"""У Вас проверили работу "{lesson_title}".
                                                           Cсылка на работу: {lesson_url}""")
            else:
                params['timestamp'] = devman_response_data['timestamp_to_request']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            pass


if __name__ == '__main__':
    main()
