# -*- coding: utf-8 -*-

import threading
import time
import random

from queue import Queue
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import settings

# LINE
line_bot_api = settings.line_bot_api
handler = settings.handler

# QUEUE
print_lock = threading.Lock()
message_queue = Queue()

# Thread
thread_num = 2

app = Flask(__name__)

def worker():
    while True:
        data = message_queue.get()

        if not data is None:
            wait_time = data['wait_time']

            if not wait_time is None:
                time.sleep(60 * wait_time)

            print('name:', threading.current_thread().name)
            line_bot_api.push_message(
                    data['sender_id'],
                    TextSendMessage(text=data['reply_word'])
                    )

            message_queue.task_done()

        time.sleep(60)

def decide_reply_word(text):
    reply_word = ''

    if text == 'ping':
        reply_word = 'pong'
    elif text == 'うにうに':
        reply_word = 'いくら'
    elif 'にゃ' in text:
        reply_word = 'にゃー'
    else:
        reply_word = random.choice(settings.reply_words)

    return reply_word

def decide_wait_time(qsize):
    wait_time = 0

    if qsize == 0:
        # generate random time
        wait_time = random.randint(1, 15)

    print("decide_wait_time: %d" %wait_time)

    return wait_time


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    data = {}

    data['reply_word'] = decide_reply_word(event.message.text)
    data['wait_time'] = decide_wait_time(message_queue.qsize())
    data['message_id'] = event.message.id
    data['sender_id'] = event.source.sender_id

    message_queue.put(data)


if __name__ == '__main__':

    # start threads with worker
    for x in range(thread_num):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    # start api process
    app.run(host='localhost', port=8000, threaded=True, debug=True)

    # waiting for done thread works
    message_queue.join()
