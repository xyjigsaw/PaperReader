# Name: paperreader.app.py
# Author: Reacubeth
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from fastapi import FastAPI
import gradio as gr

# 1. Import your own modules here
from modules import (
    paperreader_interface,
)

app = FastAPI()

# 2. Add your modules here then
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
        <p align="right"> <a href="https://github.com/xyjigsaw">Github</a> <a href="https://idea.acemap.cn/#/">DeepReport</a></p>
                
        # <center>PaperReader By DeepReport</center>  
    """),
    gr.TabbedInterface(
    [
        paperreader_interface,
    ],
    [
        'PaperReader',
    ])


@app.get('/v1/test')
async def connection_test():
    return 'Connect Succeed!'


# demo.queue(concurrency_count=20)

app = gr.mount_gradio_app(app, demo, path='/')
