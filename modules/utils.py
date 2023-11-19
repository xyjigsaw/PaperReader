# Name: utils.py
# Author: Reacubeth
# Time: 2023/3/2 14:15
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import os
import openai
import requests

# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = ''


def get_item_package(role, content):
    return {"role": role, "content": content}


def get_response(messages):
    resp = requests.post(
        url="https://api.openai.com/v1/chat/completions",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {openai.api_key}"},
        json={
            "model": "gpt-3.5-turbo",
            "messages": messages,
        },
        proxies={
            "http": "http://10.10.1.3:10000",
            "https": "http://10.10.1.3:10000",
        }
    )
    return resp.json()


def main_session():
    messages = [
        get_item_package("system", "You are a helpful assistant."),
    ]
    while True:
        user_input = input("User: ")
        messages.append(get_item_package("user", user_input))
        # res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        res = get_response(messages)
        cur_content = res['choices'][0]['message']['content']
        print(cur_content)
        messages.append(get_item_package("assistant", cur_content))


def single_chat_portal(system_text, input_text):
    messages = [
        get_item_package("system", system_text),
    ]
    messages.append(get_item_package("user", input_text))
    res = get_response(messages)
    if 'error' in res:
        return res['error']['message']
    else:
        cur_content = res['choices'][0]['message']['content']
        return cur_content
