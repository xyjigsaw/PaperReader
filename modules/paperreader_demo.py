# Name: paperreader
# Author: Reacubeth
# Mail: noverfitting@gmail.com
# Site: www.omegaxyz.com
# *_*coding:utf-8 *_*

import gradio as gr
from typing import Any, Dict, List
import random

from .utils import single_chat_portal
from .get_paper_from_pdf import Paper

using_local_llm = False

system_text_value = """Hello there! 👋 I am your "Paper Assistant" in the domain of "{domain}", and I'm here to make your academic and professional paper reading smoother."""


PROMPT_DICT = {
    "prompt_input": (
        "{system}\n\n"
        "### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:"
    ),
    "prompt_no_input": (
        "{system}\n\n" 
        "### Instruction:\n{instruction}\n\n### Response:"
    ),
}

def build_inputs(prompts: List[str], **kwargs: Dict[str, Any]) -> Dict[str, List[Any]]:
    """A wrapper for better calling generation function.

    All the parameters except `prompts` can be passed with a single scalar, which will
    be expaned in a list passed into `matx_inference` function. The reason is that a
    batch of prompts should follow the same configuration.
    """
    inputs = {"prompts": prompts}
    batch_size = len(prompts)
    for key, value in kwargs.items():
        inputs.update({key: [value] * batch_size})
    return inputs

def generate_response(system_text, input_text, paper_text, temperature, max_new_tokens):
    if using_local_llm:
        data = {
            "system": system_text,
            "instruction":input_text,
        }
        prompt_input, prompt_no_input = PROMPT_DICT["prompt_input"], PROMPT_DICT["prompt_no_input"]
        prompt = prompt_input.format_map(data) if data.get("input", "") != "" else prompt_no_input.format_map(data)


        prompts = [
            prompt,
        ]

        temperature = float(temperature)
        if temperature <= 0.0:
            temperature = 0.05

        inputs = build_inputs(
            prompts=prompts,
            temperature=temperature,
            top_p=1.0,
            repetition_penalty=1.0,
            do_sample=True,
            max_new_tokens=int(max_new_tokens),
        )

        model_name = "deepreport_llm_demo"
        outputs = ['hello']
        raise NotImplementedError
    else:
        paper_prompt = "Read the paper below:\n {paper_text}".format(paper_text=paper_text) + "\n\nHere is the question:\n"
        return single_chat_portal(system_text, paper_prompt + input_text)

def process_file(file_obj_ls):
    content_ls = []
    file_name_ls = []
    for file_obj in file_obj_ls:
        print('[INFO] file path: ', file_obj)
        if file_obj.endswith('.txt') or file_obj.endswith('.md'):
            with open(file_obj, 'r') as tmp_f:
                data = tmp_f.readlines()[0]
        elif file_obj.endswith('.pdf'):
            abs_only = True
            paper = Paper(path=file_obj)
            paper.parse_pdf()
            data = paper.get_paper_text(abs_only)
        content_ls.append(data)
        file_name_ls.append(file_obj)
    # TODO: add a function to process multiple files
    print('[WARNING]: only process the first file')
    return content_ls[0], file_name_ls

def upload_file(files):
    file_paths = [file.name for file in files]
    return file_paths

def update_systembox(domain_dropdown):
    if domain_dropdown == "general":
        pre_str = system_text_value.format(domain="everything")
    else:
        pre_str = system_text_value.format(domain=domain_dropdown)
    return pre_str


def update_textbox(domain_dropdown, task_example, cot_checkbox):
    if domain_dropdown == "general":
        pre_str = ""
    else:
        pre_str = domain_dropdown
    cur_prompt = ""
    if task_example == "Customize":
        cur_prompt = ""
    elif task_example == "Summarization":
        if cot_checkbox:
            cur_prompt = "Can you distill the main points of this research paper into a concise summary? Your response should be detailed."
        else:
            cur_prompt = "Can you distill the main points of this research paper into a concise summary? Just make a summarization."
    elif task_example == "Dataset Analysis":
        if cot_checkbox:
            cur_prompt = "What datasets were used in this study and how were they used to support the findings? Please check the whole paper carefully and make a detailed response about these datasets with statistics."
        else:
            cur_prompt = "What datasets were used in this study and how were they used to support the findings?"
        # "Identify and describe the datasets used in this paper."
    elif task_example == "Methodology":
        if cot_checkbox:
            cur_prompt = "Provide a summary of the methodology used in this research paper. Please check the whole paper carefully and generate a detailed response."
        else:
            cur_prompt = "Provide a summary of the methodology used in this research paper."
        # "What methods and techniques were employed in this study and why?"
    elif task_example == "Idea Generation":
        if cot_checkbox:
            cur_prompt = "Based on the findings and conclusions of this paper, what new research questions or ideas can be proposed? You should also provide the reason."
        else:
            cur_prompt = "Based on the findings and conclusions of this paper, what new research questions or ideas can be proposed?"
        # "Considering the results and discussions in this paper, what innovative concepts or hypotheses can be generated for future studies?"
    return cur_prompt



with gr.Blocks() as paperreader_interface:
    with gr.Row():
        with gr.Column(scale=2):
            with gr.Row():
                system_text = gr.Textbox(
                    value=system_text_value,
                    label="System",
                    info="We use DeepReport's system prompt.",
                    container=True,
                    lines=2,
                    interactive=False
                )
            with gr.Row():
                input_text = gr.Textbox(
                    value="What are the key findings, arguments, and conclusions presented in this paper?",
                    label="Input",
                    container=True,
                    lines=2,
                    show_copy_button=True,
                )
            with gr.Row():
                paper_text = gr.Textbox(
                    value="",
                    label="Paper Preview",
                    container=True,
                    lines=4,
                    show_copy_button=True,
                )
            with gr.Row():
                response_text = gr.Textbox(
                    value="",
                    label="Response",
                    container=True,
                    lines=2,
                    show_copy_button=True,
                )
            with gr.Row():
                generate_btn = gr.Button("Generate", variant="primary")
                clear_btn = gr.ClearButton(value="Clear", components=[response_text])
        with gr.Column():
            with gr.Tab(label="Advanced Setting"):
                with gr.Blocks():
                    file_output = gr.File()
                    upload_button = gr.UploadButton("Click to Upload Files (txt, md, or pdf)", file_types=[], file_count="multiple")
                    # upload_button.click(upload_file, upload_button, file_output)
                    upload_button.upload(
                        fn=process_file,
                        inputs=[upload_button],
                        outputs=[paper_text, file_output]
                    )

                domain_dropdown = gr.Dropdown(
                    ["general", "computer science", 'geo-science'], 
                    value="general",
                    label="Subject/Domain", 
                    info="Choose your interested subject/domain."
                )

                task_example = gr.Radio(
                    value="Summarization",
                    choices=["Customize", "Summarization", "Dataset Analysis", "Methodology", "Idea Generation"],
                    label="Task Prompt",
                    info="Choose a task prompt (example)."
                )

                cot_checkbox = gr.Checkbox(
                    value=False,
                    label="USING COT", 
                    info="Choose whether to generate a detailed response."
                )

                abs_checkbox = gr.Checkbox(
                    value=True,
                    label="Abstract Only (Beta)", 
                    info="Choose whether to generate response from the abstract only."
                )

                temperature = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.8,
                    step=0.1,
                    interactive=True,
                    label="Temperature",
                    visible=using_local_llm,
                )
                max_new_tokens = gr.Slider(
                    minimum=16,
                    maximum=512,
                    value=300,
                    step=4,
                    interactive=True,
                    label="Max New Tokens",
                    visible=using_local_llm,
                )

    generate_btn.click(
        fn=generate_response,
        inputs=[system_text, input_text, paper_text, temperature, max_new_tokens],
        outputs=[response_text],
    )

    task_example.change(
        fn=update_textbox,
        inputs=[domain_dropdown, task_example, cot_checkbox],
        outputs=[input_text],
    )

    domain_dropdown.change(
        fn=update_textbox,
        inputs=[domain_dropdown, task_example, cot_checkbox],
        outputs=[input_text],
    )

    domain_dropdown.change(
        fn=update_systembox,
        inputs=[domain_dropdown],
        outputs=[system_text],
    )

    cot_checkbox.change(
        fn=update_textbox,
        inputs=[domain_dropdown, task_example, cot_checkbox],
        outputs=[input_text],
    )

if __name__ == "__main__":
    paperreader_interface.launch()
