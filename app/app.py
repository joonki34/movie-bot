import json
import os
import requests


def lambda_handler(event, context):
    # Get information from Megabox API
    url = "https://www.megabox.co.kr/on/oh/oha/Movie/selectMovieList.do"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    result = ""
    movie_list = data.get("movieList", [])
    for index, movie_item in enumerate(movie_list):
        title = movie_item.get("movieNm", "")
        release_date = movie_item.get("rfilmDe", "")
        result += f"{index + 1}. {title} {release_date}\n"

    # Send to telegram
    bot_token = os.environ.get('TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    send_text = (
        f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}'
        f'&parse_mode=HTML&text={result}'
    )
    requests.get(send_text)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from David!')
    }


if __name__ == '__main__':
    lambda_handler(None, None)
