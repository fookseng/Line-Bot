from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from imgurpython import ImgurClient
from config import client_id, client_secret, album_id, access_token, refresh_token
import tempfile, os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('kXstBj4Fw+0w+6kvJB7yY6tyieLT13lgt+A456k3MdC+RaavJav0UWI6STr/CYkOvp36ogy3v5E3eYu9tCmJkPP+LDvWCNv51yse+eaEl+0wFb6nW0LFVoDWevQ0xnRixBjWaUek8VlQPNgCOYqeTQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('63f7a30334c31485223f6dc93525a826')

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 5:
            return content
        link = data['href']
        content += '{}\n\n'.format(link)
    return content


# 處理訊息
#@handler.add(MessageEvent, message=TextMessage)
@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        try:
            client = ImgurClient(client_id, client_secret, access_token, refresh_token)
            config = {
                'album': album_id,
                'name': 'Catastrophe!',
                'title': 'Catastrophe!',
                'description': 'Cute kitten being cute on '
            }
            path = os.path.join('static', 'tmp', dist_name)
            client.upload_from_path(path, config=config, anon=False)
            os.remove(path)
            print(path)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳成功'))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳失敗'))
        return 0

    
    if event.message.text == "大家都吃什麼" or event.message.text == "suggestion":
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(original_content_url=url,preview_image_url=url)
        line_bot_api.reply_message(event.reply_token, image_message)
        return 0
    
    if event.message.text.lower() == "news" or event.message.text.lower() == "新聞" :
        content = apple_news()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0
    
    if event.message.text == "電影" or event.message.text == "movie":
        content = movie()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    
    if event.message.text.lower() == "breakfast":
        content = "eat kXstBj4Fw"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0
    if event.message.text.lower() == "lunch":
        content = "eat lunch"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0
    if event.message.text.lower() == "dinner":
        content = "eatdinner"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0
    if event.message.text.lower() == "sleep":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=1))
    if event.message.text.lower() == "yes":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=2))
    if event.message.text.lower() == "shock":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=3))
    if event.message.text.lower() == "love":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=4))
    if event.message.text.lower() == "narcissism":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=5))
    if event.message.text.lower() == "angry":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=6))
    if event.message.text.lower() == "ugly":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=7))
    if event.message.text.lower() == "scared":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=8))
    if event.message.text.lower() == "cry":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=9))
    if event.message.text.lower() == "smile":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=10))
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
