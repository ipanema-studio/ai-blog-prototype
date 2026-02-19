import os
import sys
import time
import copy
import random
import requests
import re
from random import shuffle
from datetime import datetime
from threading import Thread, Event
from queue import Queue
from pathlib import Path

import gradio as gr
import numpy as np
import requests
import json
# import torch
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from util.css import css
from util.js import js
from util.svg import svg
from util.chatbot import aim_chatbot_data

title = "SK hynix's AiM"


SAMPLE_TEXT = [
    "What company is SK hynix?",
    "Describe PIM, Processing in Memory",
    "What is grouped query attention?",
    "Is Llama3 better than GPT4?",
    "I am going on a trip to Seoul. Where should I visit?",
    "My favorite color is yellow. My favorite fruit is strawberry.",
    "Can you talk to me? Are you conscious?",
    "I feel great to meet you today!",
    "Describe the feeling of seeing your favorite band perform live in concert.",
    "Imagine walking through a dense forest and finding an ancient, hidden temple.",
    "Write a story about a cat who becomes friends with a magical creature.",
    "What would it be like to live on a spaceship traveling between galaxies?",
    "Describe the most beautiful sunset you have ever witnessed in great detail.",
    "Imagine you could speak any language instantly. How would you use this ability?",
    "Write a poem that captures the essence of a rainy afternoon in the city.",
    "Describe the experience of flying for the first time. What did you see?",
    "What if you woke up with the ability to turn invisible at will?",
    "Imagine a world where animals could speak. What would they say to humans?",
    "Describe the taste and texture of your favorite dessert in vivid detail.",
    "You find a mysterious key in an old bookstore. What does it unlock?",
    "Write about a day in the life of a professional treasure hunter.",
    "Describe an underwater city and the creatures that live there.",
    "Write a letter to your future self, 20 years from now.",
    "Imagine discovering a new color that no one has ever seen before.",
    "Describe the feeling of standing at the edge of a vast canyon.",
    "What if you could travel back in time? Which era would you visit first?",
    "Write a story about a garden where all the plants have unique personalities.",
    "Describe the sights and sounds of a bustling market in a foreign country.",
    "What would you do if you found a time machine hidden in your attic?",
    "Describe a dream where everything is made of candy and sweets.",
    "Imagine meeting a character from your favorite book. What do you talk about?",
    "Write about a world where everyone has a unique superpower.",
    "Describe the experience of being lost in a city you've never been to.",
    "What if you could breathe underwater? How would your life change?",
    "Imagine finding a hidden door in your house that leads to another world.",
    "Describe the sound of a symphony orchestra playing your favorite piece of music.",
    "Write a story about an inventor who creates a machine that can read minds.",
    "Describe the feeling of being at the top of a tall mountain.",
    "Imagine you could control the weather. What would your perfect day look like?",
    "Describe the smell and ambiance of a cozy coffee shop on a rainy day.",
    "What if you were the ruler of your own tiny island? Describe your kingdom.",
    "Write about a day in the life of a detective solving a mysterious case.",
    "Describe the taste of a dish from a country you've always wanted to visit.",
    "Imagine you could talk to trees. What secrets would they share with you?",
    "Write a poem about the changing seasons and their impact on your mood.",
    "Describe the feeling of jumping into a cold lake on a hot summer day.",
    "What if you found a map that leads to a hidden treasure? What do you do?",
    "Imagine you could visit any fictional universe. Where would you go and why?",
    "Describe the sensation of walking barefoot on a sandy beach.",
    "What if you could swap lives with anyone in history for one day?",
    "Write a story about a world where everyone communicates through music.",
    "Describe the excitement of opening a gift you've been eagerly anticipating.",
    "What would you do if you discovered a portal to another dimension?",
    "Imagine you could fly like a bird. Describe your first flight.",
    "Describe the ambiance of a library filled with ancient, dusty books.",
    "What if you had a secret talent that no one else knew about?",
    "Write about a day spent in a bustling, futuristic city.",
    "Describe the feeling of hearing your favorite song on the radio unexpectedly.",
    "Imagine finding a message in a bottle washed ashore. What does it say?",
    "Describe the experience of watching a meteor shower on a clear night.",
    "What would you do if you could visit your dreams while awake?",
    "Imagine discovering a hidden talent for a musical instrument you've never played.",
    "Describe the feeling of riding a bike down a steep hill at high speed.",
    "Write about a world where everyone has wings and can fly at will.",
    "Imagine meeting an alien from another planet. What questions would you ask?",
    "Describe the ambiance of a cozy cabin in the woods during a snowstorm.",
    "What if you could communicate with animals? How would it impact your life?",
    "Write a story about a magical mirror that shows glimpses of the future.",
    "Describe the feeling of seeing a shooting star for the first time.",
    "Imagine you are a famous explorer. Describe your latest discovery.",
    "What would you do if you could read people's thoughts for one day?",
    "Describe the taste and aroma of your favorite meal cooked to perfection.",
    "Imagine you could visit any place in the universe instantly. Where would you go?",
    "Write a poem that captures the essence of a warm summer evening.",
    "Describe the feeling of standing in the middle of a bustling city square.",
    "What if you found a book that always had new stories every time you opened it?",
    "Imagine you could change one historical event. Which would you choose and why?",
    "Describe the feeling of waking up to a beautiful, snow-covered landscape.",
    "Write about a secret garden where mythical creatures roam freely.",
    "What would you do if you could see into the future?",
    "Describe the ambiance of a quiet, secluded beach at sunrise.",
    "Imagine having the ability to talk to any person in history. Who and why?",
    "Write a story about a hidden society living beneath the surface of the Earth.",
    "Describe the feeling of holding a newborn baby for the first time.",
    "What if you could instantly learn any skill you wanted? What would you choose?",
    "Imagine you could visit any moment from your past. Which would it be and why?",
    "Describe the taste of a fruit you've never tried before.",
    "Write a poem about the night sky and the mysteries of the universe.",
    "What would you do if you were granted three wishes? Why?",
    "Imagine finding a pair of shoes that let you walk on air.",
    "Describe the feeling of diving into a crystal-clear swimming pool.",
    "Write a story about a town where everyone can perform small feats of magic.",
    "What if you could visit any planet in our solar system? Which one and why?",
    "Describe the sensation of touching a soft, furry animal.",
    "Imagine you could understand and speak to ghosts. What do they tell you?",
    "Write about a hidden library that only appears to those who seek knowledge.",
    "Describe the taste of a dish made with ingredients from another planet.",
    "What if you could become any character from a movie or book for a day?",
    "Imagine discovering a new species of plant with extraordinary properties.",
    "Describe the ambiance of a carnival at night, with lights and laughter everywhere.",
    "Write a story about a forgotten kingdom hidden in the depths of the ocean.",
    "What would you do if you could control time itself?",
    "Describe the feeling of hearing a hauntingly beautiful melody for the first time.",
    "Imagine finding a hidden door in your city that leads to a secret world.",
    "What if you could bring any fictional character to life? Who would it be and why?",
    "Describe the taste of an exotic dish from a distant land.",
    "Write a poem that captures the beauty of a snowy winter landscape.",
    "Imagine you could journey into people's dreams and explore their subconscious minds."
]
VLLM = 0
STRESS_TEST=0

if VLLM:
    from openai import OpenAI
    openai_api_key = "EMPTY"
    openai_api_base = "http://localhost:8000/v1"
    client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=openai_api_key,
            base_url=openai_api_base,
    )
    models = client.models.list()
    model = models.data[0].id

llama_sample_prompt_list = [
    "Describe Processing in Memory.",
    "What model are you?",
    "What company is SK hynix?",
    "Describe attention in LLMs."
]

initial_llama_auto_mode_batch_input_list = [
    "Describe Processing in Memory.",
    "What model are you?",
    "What company is SK hynix?",
    "Describe attention in LLMs.",
    "I am going on a trip to Seoul. Where should I visit?",
    "Can you talk to me? Are you conscious?",
    "What is grouped query attention?",
    "Write a story about a cat who becomes a dog.",
]*100

initial_auto_mode_llama_greeting_message = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "assistant", "content": "Hello! I'm Llama, powered by AiM."}
]

about_demo = """
# About AiM Demo

## Details
* AiMX Card x 4
* Model: Llama 3 8B
* Batch Size: ~8
* Token Size: 128~2048

## Contact Us
* SKhynix_PIM@skhynix.com
"""

auto_mode_timer_interval = 1  # seconds

initial_batch_num = 8

llama_auto_mode_chatbot_batch_stop_event = Event()
llama_auto_mode_chatbot_batch_stop_event.clear()

gr.set_static_paths(paths=[Path.cwd().absolute()/"assets"])

theme = gr.themes.Soft(
    primary_hue="violet"
).set(
    body_background_fill_dark="#000"
)

def show_llama_mode_info(mode_state, auto_mode_start_state, auto_mode_interval_number):
    if mode_state == "Auto":
        if auto_mode_start_state == "Start":
            gr.Info("AiM starts processing batches automatically.", duration=auto_mode_interval_number)
        else:
            gr.Info("AiM pauses processing batches automatically.", duration=auto_mode_interval_number)

def update_llama_mode(mode_radio, mode_state):
    if str(mode_radio) == str(mode_state):
        return mode_state
    return mode_radio

def reset_llama_auto_mode_chatbot_batch(*llama_auto_mode_chatbot_batch_generation_state_list):
    history_list = []
    for generation_state in llama_auto_mode_chatbot_batch_generation_state_list:
        if generation_state:
            history_list.append(gr.Chatbot(type="messages", elem_classes="my_chatbot_class", elem_id="my_chatbot_auto_mode_batch_chatbot", show_label=False, height="100%", avatar_images=("assets/images/question_avatar.png", "assets/images/llama_avatar.png")))
        else:
            history_list.append(None)
    return history_list

def trigger_llama_auto_mode_chatbot(generation_state, counter_state, auto_mode_batch_number, batch_index_state):
    if generation_state or batch_index_state >= auto_mode_batch_number - 1:
        return counter_state
    return counter_state + 1

def pick_llama_sample_prompt():
    return random.choice(llama_sample_prompt_list)

def lock_before_llm_generation():
    return True

def unlock_after_llm_generation():
    return False

def enable_llama_interaction():
    return [gr.Textbox(interactive=True)] + [gr.Row(visible=False)] * 3

def disable_llama_interaction():
    return [gr.Textbox(interactive=False)] + [gr.Row(visible=True)] * 3

def open_popup():
    return gr.Row(visible=True)

def close_popup():
    return [gr.Row(visible=False)] * 2

def open_admin_setting():
    return gr.Row(visible=True)

def view_llama_chatbot():
    return gr.Row(visible=False), gr.Row(visible=True)

def send_user_llama_prompt(user_message, history):
    # random test !
    # history = []
    # if len(history) == 0:
    #     history += [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    # return "", history + [{"role": "user", "content": str(user_message)}]
    # random test !
    # input_prompt = random.choice(SAMPLE_TEXT)
    return "", history + [{"role": "user", "content": user_message}]
    

def process_user_prompt(user_message, user_prompt_state):
    if user_message.strip() != "":
        user_prompt_state = user_prompt_state + 1
    return user_prompt_state

def click_llama_sample_prompt(sample_prompt, user_prompt_state):
    user_prompt_state = user_prompt_state + 1
    return str(sample_prompt), user_prompt_state

def check_vllm_queue():
    METRICS_URL = "http://localhost:8000/metrics/"
    metrics_text = requests.get(METRICS_URL).text
    # print(metrics_text)
    running = re.search(r'vllm:num_requests_running\{.*?\}\s+(\d+\.\d+)', metrics_text)
    waiting = re.search(r'vllm:num_requests_waiting\{.*?\}\s+(\d+\.\d+)', metrics_text)
    running_request = int(float(running.group(1))) if running else None
    waiting_request = int(float(waiting.group(1))) if waiting else None
    return running_request, waiting_request

req = 0
def receive_llama_chatbot_answer(history, llama_auto_mode_batch):
    global req
    tokens = random.randint(1024, 1500)

    if len(history) == 0:
        history += [{"role": "user", "content": random.choice(llama_sample_prompt_list)}]
    elif llama_auto_mode_batch and len(history) >= 9:
        history = history[-7:]
    history_refined = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        history[-1]
    ]

    if VLLM:
        if STRESS_TEST:
            req += 1
            current_pid = os.getpid()
            filename = f'stress_test_{current_pid}.txt'
            with open(filename, 'a') as file:
                file.write(f'===========Req{req} Gen Token{tokens}=======\n')
                file.write(f'[Req{req} User]  {history} \n')
        try:
            chat_completion = client.chat.completions.create(
                messages=history_refined,
                model=model,
                max_tokens=tokens,
                stream=True,
                temperature=0.9,
                timeout=600
            )
            # print("history :", history)
            history += [{"role": "assistant", "content": ""}]
            for chunk in chat_completion:
                if llama_auto_mode_batch and llama_auto_mode_chatbot_batch_stop_event.is_set():
                    chat_completion.close()
                    return history
                if chunk.choices[0].delta.content:
                    if "assistant" in chunk.choices[0].delta.content or "style" in chunk.choices[0].delta.content: 
                        continue
                    # print(chunk.choices[0].delta.content, end="", flush=True)   
                    history[-1]["content"] += chunk.choices[0].delta.content
                    yield history
        except Exception as e:
            print("AiMX has busy request. Please try again later.")
            chat_completion.close()
            history[-1]["content"] += "AiMX has busy request. Please try again later."
            if STRESS_TEST:
                with open(filename, 'a') as file:
                    file.write(f'Req{req} [Error!!!!!!!]  {e} \n')
                    file.write('================================\n')
            yield history
        
        if STRESS_TEST:
            with open(filename, 'a') as file:
                file.write(f'Req{req} [Answer]  {history[-1]["content"]} \n')
                file.write('================================\n')
    else:
        history += [{"role": "assistant", "content": ""}]
        time.sleep(0)
        for c in "Dummy Text " * random.randint(1, 20):
            if llama_auto_mode_batch and llama_auto_mode_chatbot_batch_stop_event.is_set():
                return history
            time.sleep(0.1)
            history[-1]["content"] += c
            yield history

def update_auto_mode_status_quo(*llama_auto_mode_chatbot_batch_generation_state_list):
    if VLLM:
        running_value, waiting_value = check_vllm_queue()
        if running_value == None:
            running_value = 0
        if waiting_value == None:
            waiting_value = 0
        return f"| {running_value}", f"| {waiting_value}"
    else:
        running_value = 0
        for generation_state in llama_auto_mode_chatbot_batch_generation_state_list:
            if generation_state:
                running_value += 1
        return f"| {running_value}", "| 0"

def exit_auto_mode_batch(auto_mode_start_state):
    if auto_mode_start_state == "Pause":
        llama_auto_mode_chatbot_batch_stop_event.set()
    else:
        llama_auto_mode_chatbot_batch_stop_event.clear()

def plotly_subplot_base_calc(value_list, idx):
    base = [0] * len(value_list[0])
    for i in range(0, idx):
        base = list(np.add(base, value_list[i]))
    return base

def create_llama_plot(llama_chatbot_generation_state, llama_auto_mode_chatbot_generation_state):
    test_legend_list = ["GPU", "AiMX Prototype", "AiMX ASIC", "Next Gen Target"]
    fig_width = 780 if bool(llama_auto_mode_chatbot_generation_state) else 815
    fig_height = 790/2 if bool(llama_auto_mode_chatbot_generation_state) else 790
    token_bar_categories = ['GPU (TP2)','AiMX Prototype', 'AiMX ASIC', 'Next Gen Target']
    test_marker_colors = {
        "GQA": ["#000", "#000", "#000", "#000"],
        "FC": ["#000", "#000", "#000", "#000"]
    }
    test_operation_list = ["GQA", "FC"]
    test_value_switcher = {
        1: { # Batch Num
            "1K": [ # Token Len
                # GPU, AiMX Prototype, AiMX ASIC, Next Gen Target
                [2.5, 1.26, 0.564, 0.030], # GQA
                [30.66, 24, 8.364, 3.996], # FC
            ],
            "16K": [
                [19.77, 9.987, 4.463, 0.171],
                [30.66, 24, 8.378, 3.996],
            ],
            "128K": [
                [148.7, 75.13, 33.570, 0.887],
                [30.66, 24, 8.400, 3.996],
            ],
        }
    }

    batch_num = 1
    fig = make_subplots(
        figure=go.Figure(
            layout=go.Layout(
                {
                    'paper_bgcolor': 'rgba(0,0,0,0)',
                    'plot_bgcolor': 'rgba(0,0,0,0)',
                    'title': ' ',
                }
            )
        ),
        rows=1,
        cols=3,
        shared_yaxes=True,
        # x_title='# of Tokens',
        # x_title='rev5',
        y_title='mSec/Token',
        subplot_titles=list(test_value_switcher[batch_num].keys()),
        # horizontal_spacing=0,
    )

    for i, token_len in enumerate(list(test_value_switcher[batch_num].keys())):
        for j, op in enumerate(test_operation_list):
            fig.add_trace(
                go.Bar(
                    name=op,
                    x=token_bar_categories,
                    y=test_value_switcher[batch_num][token_len][j],
                    base=plotly_subplot_base_calc(test_value_switcher[batch_num][token_len], j),
                    offsetgroup=token_len,
                    marker_color=test_marker_colors[op],
                    width=0.6,
                    marker_pattern_shape="/" if op == "GQA" else "\\",
                    marker_pattern_solidity=0.2,
                    marker_line_width=2,
                    marker_pattern_fgcolor="#fff",
                    marker_pattern_fillmode="overlay",
                    marker_pattern_fgopacity=1,
                    showlegend=False
                ),
                row=1,
                col=i+1,
            )

    # custom legend
    # for i, legend in enumerate(test_legend_list):
    #     fig.add_trace(
    #         go.Bar(
    #             name=legend,
    #             x=[None],
    #             y=[None],
    #             marker_color=test_marker_colors[test_operation_list[0]][i]
    #         )
    #     )
    fig.add_trace(
        go.Bar(
            x=[None],
            y=[None],
            name="FC",
            marker_color=test_marker_colors[test_operation_list[0]][0],
            marker_pattern_shape="\\"
        )
    )
    fig.add_trace(
        go.Bar(
            x=[None],
            y=[None],
            name="GQA",
            marker_color=test_marker_colors[test_operation_list[0]][0],
            marker_pattern_shape="/"
        )
    )

    fig.update_layout(
        width=fig_width,
        height=fig_height,
        font={
            'color': 'ghostwhite',
            'family': 'Noto Sans KR'
        },
        title_font_weight='bold'
    )
    fig.update_yaxes(tickmode="array", tickvals=list(range(0, 180, 20)), range=[0, 180])

    return fig, gr.Row(visible=False), gr.Label(visible=True)

def clear_llama_plot():
    return gr.Plot(value=None), gr.Row(visible=True), gr.Label(visible=False)

def reset_llama_interface():
    return None, gr.Row(visible=True), gr.Row(visible=False)

def send_user_aim_prompt(user_message, history, aim_chatbot_state):
    if aim_chatbot_state == 0:
        return "", history
    return "", history + [{"role": "user", "content": str(user_message)}]

def receive_aim_chatbot_answer(history, aim_chatbot_state, aim_chatbot_quiz_index_state):
    if aim_chatbot_state == 0:
        history += [{"role": "assistant", "content": aim_chatbot_data["greeting"]["bot"]}]
        return history, 1, aim_chatbot_quiz_index_state, gr.Textbox(random.choice(aim_chatbot_data["greeting"]["user"]), interactive=False, placeholder="")
    else:
        time.sleep(0.5)
        if aim_chatbot_state == 1:
            aim_chatbot_quiz_index_state = random.randint(0, len(aim_chatbot_data["quiz_list"]) - 1)
            history += [{"role": "assistant", "content": aim_chatbot_data["quiz_list"][aim_chatbot_quiz_index_state]["bot"]}]
            return history, 2, aim_chatbot_quiz_index_state, gr.Textbox("", interactive=True)
        elif aim_chatbot_state == 2:
            user_answer = history[-1]["content"].lower().replace(' ', '')
            correct_answer = aim_chatbot_data["quiz_list"][aim_chatbot_quiz_index_state]["user"].lower().replace(' ', '')
            if user_answer in correct_answer or correct_answer in user_answer:
                history += [{"role": "assistant", "content": aim_chatbot_data["congrats"]["bot"]}]
                return history, 3, aim_chatbot_quiz_index_state, gr.Textbox(placeholder="Hooray!", interactive=False)
            history += [{"role": "assistant", "content": aim_chatbot_data["hint"]["bot"]}]
            return history, 2, aim_chatbot_quiz_index_state, gr.Textbox("", placeholder=aim_chatbot_data["quiz_list"][aim_chatbot_quiz_index_state]["user"], interactive=True)
        else:
            return history, 3, aim_chatbot_quiz_index_state, gr.Textbox()

def receive_aim_chatbot_answer_2(history, aim_chatbot_state, aim_chatbot_quiz_index_state):
    if aim_chatbot_state == 0:
        aim_chatbot_quiz_index_state = -1
        history += [{"role": "assistant", "content": aim_chatbot_data["greeting"]["bot"]}]
        return history, 1, aim_chatbot_quiz_index_state, gr.Textbox(random.choice(aim_chatbot_data["greeting"]["user"]), interactive=False, placeholder="")
    else:
        time.sleep(0.5)
        if aim_chatbot_state == 1:
            aim_chatbot_quiz_index_state += 1
            history += [{"role": "assistant", "content": aim_chatbot_data["quiz_list"][aim_chatbot_quiz_index_state]["bot"]}]
            return history, 2, aim_chatbot_quiz_index_state, gr.Textbox("", interactive=True)
        elif aim_chatbot_state == 2:
            user_answer = history[-1]["content"].lower().replace(' ', '')
            correct_answer = aim_chatbot_data["quiz_list"][aim_chatbot_quiz_index_state]["user"].lower().replace(' ', '')
            if user_answer in correct_answer or correct_answer in user_answer:
                if aim_chatbot_quiz_index_state == 2:
                    history += [{"role": "assistant", "content": aim_chatbot_data["congrats"]["bot"]}]
                    return history, 3, aim_chatbot_quiz_index_state, gr.Textbox(placeholder="Hooray!", interactive=False)
                else:
                    aim_chatbot_quiz_index_state += 1
                    history += [{"role": "assistant", "content": aim_chatbot_data["quiz_list"][aim_chatbot_quiz_index_state]["bot"]}]
                    return history, 2, aim_chatbot_quiz_index_state, gr.Textbox("", interactive=True, placeholder="")
            history += [{"role": "assistant", "content": aim_chatbot_data["hint"]["bot"]}]
            return history, 2, aim_chatbot_quiz_index_state, gr.Textbox("", placeholder=aim_chatbot_data["quiz_list"][aim_chatbot_quiz_index_state]["user"], interactive=True)
        else:
            return history, 3, aim_chatbot_quiz_index_state, gr.Textbox()

def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

with gr.Blocks(css=css, js=js, title=title, theme=theme) as demo:
    user_llama_prompt_counter_state = gr.State(value=0)
    user_llama_auto_mode_prompt_counter_state = gr.State(value=0)
    user_aim_prompt_counter_state = gr.State(value=0)
    llama_chatbot_generation_state = gr.State(False)
    llama_auto_mode_chatbot_generation_state = gr.State(False)
    aim_chatbot_state = gr.State(value=0)
    aim_chatbot_quiz_index_state = gr.State(value=0)
    auto_mode_timer = gr.Timer(auto_mode_timer_interval, active=False)
    auto_mode_status_quo_timer = gr.Timer(1, active=True)
    llama_auto_mode_chatbot_batch_timer_list = []
    llama_auto_mode_chatbot_batch_counter_state_list = []
    for i in range(initial_batch_num - 1):
        llama_auto_mode_chatbot_batch_timer_list.append(gr.Timer(value=auto_mode_timer_interval, active=False))
        llama_auto_mode_chatbot_batch_counter_state_list.append(gr.State(value=0))
    with gr.Row(elem_classes="my_chatbot_container_row_class", visible=True) as llama_chatbot_container_row:
        with gr.Row(elem_classes="my_chatbot_container_top_row_class"):
            with gr.Row(elem_classes="my_dot_button_row_class"):
                gr.HTML(svg["button_dot"])
                llama_dot_button = gr.Button("", elem_classes="my_dot_button_clickable_class")
            with gr.Row(elem_classes="my_skhynix_aim_logo_row_class"):
                gr.HTML(svg["skhynix_aim_logo"])
            with gr.Row(elem_classes="my_reset_button_row_class"):
                gr.HTML(svg["button_reset"])
                llama_reset_button = gr.Button("", elem_classes="my_reset_button_clickable_class")
            llama_top_row_disabled = gr.Row(elem_classes="my_chatbot_container_top_row_disabled_class", visible=False)
        with gr.Row(elem_classes="my_chatbot_container_mid_row_class"):
            with gr.Row(elem_classes="my_chatbot_row_class", visible=False) as llama_chatbot_row:
                with gr.Row(elem_classes="my_horizontal_line_markdown_top_class"):
                    gr.Markdown("---")
                llama_chatbot = gr.Chatbot(None, type="messages", elem_classes="my_chatbot_class", elem_id="my_llama_chatbot", show_label=False, height="100%", avatar_images=(None, "assets/images/llama_avatar.png"))
                with gr.Row(elem_id="my_aim_chatbot_switch_button_row", elem_classes="my_chatbot_switch_button_row_class") as aim_chatbot_switch_button_row:
                    gr.HTML(svg["button_aim_iso_with_text_bubble"])
                    aim_chatbot_switch_button = gr.Button("", elem_classes="my_chatbot_switch_button_clickable_class", min_width=0)
                with gr.Row(elem_id="my_llama_plot_row"):
                    with gr.Row(elem_id="my_plotly_icon_row") as plotly_icon_row:
                        gr.HTML(svg["plotly_icon"], elem_id="my_plotly_icon_svg")
                    llama_plot_label = gr.Label("Inference Latency of Llama 3 8B", elem_id="my_llama_plot_label", visible=False, min_width=0, show_label=False, container=False)
                    llama_plot = gr.Plot(container=False, elem_id="my_llama_plot")
                with gr.Row(elem_classes="my_horizontal_line_markdown_bottom_class"):
                    gr.Markdown("---")
            with gr.Row(elem_id="my_llama_landing_page_row", visible=True) as llama_landing_page_row:
                with gr.Row(elem_id="my_aim_icon_row"):
                    gr.HTML(svg["icon_aim_iso"], elem_id="my_aim_icon_html", visible=False)
                    aim_chatbot_switch_button_in_landing_page = gr.Button("",elem_id="my_aim_chatbot_switch_button_in_landing_page", min_width=0, visible=False)
                    test_image_input = gr.Image(
                        value=None,
                        elem_classes="my_test_image_class",
                        elem_id="my_test_image_input",
                        format="png",
                        sources=["upload"],
                        show_label=False,
                        show_share_button=False,
                        show_fullscreen_button=False,
                        placeholder="Click to upload!"
                    )
                    test_image_output = gr.Image(
                        value=None,
                        elem_classes="my_test_image_class",
                        elem_id="my_test_image_output",
                        format="png",
                        show_label=False,
                        show_share_button=False,
                        show_fullscreen_button=False,
                        interactive=False,
                        show_download_button=True,
                        visible=False
                    )
                with gr.Row(elem_id="my_llama_sample_prompt_row"):
                    with gr.Row(elem_id="my_llama_sample_prompt_button_row"):
                        llama_sample_prompt_button_list = []
                        for llama_sample_prompt in llama_sample_prompt_list:
                            llama_sample_prompt_button_list.append(gr.Button(llama_sample_prompt, elem_classes="my_llama_sample_prompt_button", size="sm", min_width=0))
                    llama_sample_prompt_row_disabled = gr.Row(elem_id="my_llama_sample_prompt_row_disabled", visible=True)
        with gr.Row(elem_classes="my_chatbot_container_bottom_row_class"):
            user_llama_prompt_textbox = gr.Textbox(interactive=False, elem_classes="my_user_prompt_textbox_class", show_label=False, container=False, lines=1, max_lines=1, placeholder="Ask anything!", min_width=0)
            gr.HTML(svg["button_submit"], elem_classes="my_user_prompt_submit_button_html_class")
            llama_submit_button = gr.Button("", elem_classes="my_user_prompt_submit_button_clickable_class", min_width=0)
            llama_bottom_row_disabled = gr.Row(elem_classes="my_chatbot_container_bottom_row_disabled_class", visible=True)
    with gr.Row(elem_classes="my_chatbot_container_row_class", visible=False) as llama_chatbot_auto_mode_container_row:
        with gr.Row(elem_classes="my_chatbot_auto_mode_container_bottom_row_class"):
            gr.Markdown("# While AiM Processes Other Batches", elem_classes="my_chatbot_auto_mode_heading_markdown_class")
            with gr.Row(elem_id="my_chatbot_auto_mode_bottom_row_button_row"):
                with gr.Row(elem_classes="my_start_button_row_class"):
                    gr.HTML(svg["button_start"])
                    llama_auto_mode_chatbot_batch_start_button = gr.Button("", elem_classes="my_start_button_clickable_class")
                with gr.Row(elem_classes="my_pause_button_row_class"):
                    gr.HTML(svg["button_pause"])
                    llama_auto_mode_chatbot_batch_pause_button = gr.Button("", elem_classes="my_pause_button_clickable_class")
            with gr.Row(elem_id="my_chatbot_auto_mode_bottom_row_status_quo_row"):
                gr.Label("Status Quo", elem_id="my_chatbot_auto_mode_status_quo_title_label", elem_classes="my_chatbot_auto_mode_status_quo_label_class", visible=True, min_width=0, show_label=False, container=False)
                gr.Label("Queue", elem_id="my_chatbot_auto_mode_status_quo_queue_label", elem_classes="my_chatbot_auto_mode_status_quo_label_class", visible=True, min_width=0, show_label=False, container=False)
                chatbot_auto_mode_status_quo_queue_value_label = gr.Label(f"| {initial_batch_num}", elem_id="my_chatbot_auto_mode_status_quo_queue_value_label", elem_classes="my_chatbot_auto_mode_status_quo_label_class", visible=True, min_width=0, show_label=False, container=False)
                gr.Label("Running", elem_id="my_chatbot_auto_mode_status_quo_running_label", elem_classes="my_chatbot_auto_mode_status_quo_label_class", visible=True, min_width=0, show_label=False, container=False)
                chatbot_auto_mode_status_quo_running_value_label = gr.Label("| 0", elem_id="my_chatbot_auto_mode_status_quo_running_value_label", elem_classes="my_chatbot_auto_mode_status_quo_label_class", visible=True, min_width=0, show_label=False, container=False)
                gr.Label("Waiting", elem_id="my_chatbot_auto_mode_status_quo_waiting_label", elem_classes="my_chatbot_auto_mode_status_quo_label_class", visible=True, min_width=0, show_label=False, container=False)
                chatbot_auto_mode_status_quo_waiting_value_label = gr.Label("| 0", elem_id="my_chatbot_auto_mode_status_quo_waiting_value_label", elem_classes="my_chatbot_auto_mode_status_quo_label_class", visible=True, min_width=0, show_label=False, container=False)
            with gr.Row(elem_id="my_chatbot_auto_mode_bottom_row_body_row"):
                with gr.Row(elem_id="my_chatbot_auto_mode_batch_row"):
                    llama_auto_mode_chatbot_batch_list = []
                    llama_auto_mode_chatbot_batch_generation_state_list = []
                    for i in range(initial_batch_num - 1):
                        llama_auto_mode_chatbot_batch_list.append(gr.Chatbot(None, type="messages", elem_classes="my_chatbot_class", elem_id="my_chatbot_auto_mode_batch_chatbot", show_label=False, height="100%", avatar_images=("assets/images/question_avatar.png", "assets/images/llama_avatar.png")))
                        llama_auto_mode_chatbot_batch_generation_state_list.append(gr.State(value=False))
        with gr.Row(elem_classes="my_chatbot_auto_mode_container_mid_row_class"):
            gr.Markdown("# Ask Llama Anything, Boosted by AiM", elem_classes="my_chatbot_auto_mode_heading_markdown_class")
            with gr.Row(elem_id="my_chatbot_auto_mode_mid_row_body_row"):
                with gr.Row(elem_id="my_chatbot_auto_mode_mid_row_chatbot_wrapper"):
                    with gr.Row(elem_id="my_llama_auto_mode_interactive_chatbot_row"):
                        llama_auto_mode_interactive_chatbot = gr.Chatbot(initial_auto_mode_llama_greeting_message, type="messages", elem_classes="my_chatbot_class", elem_id="my_llama_auto_mode_interactive_chatbot", show_label=False, height="100%", avatar_images=(None, "assets/images/llama_avatar.png"))
                    llama_auto_mode_chatbot_textbox = gr.Textbox("", elem_id="my_llama_auto_mode_interactive_chatbot_textbox", show_label=False, container=False, lines=1, max_lines=1, placeholder="Ask anything!", min_width=0)
                    gr.HTML(svg["button_submit"], elem_id="my_llama_auto_mode_interactive_chatbot_prompt_submit_button_html")
                    llama_auto_mode_chatbot_submit_button = gr.Button("", elem_id="my_llama_auto_mode_interactive_chatbot_prompt_submit_button_clickable", min_width=0)
                    llama_auto_mode_chatbot_disabled = gr.Row(elem_id="my_llama_auto_mode_interactive_chatbot_prompt_disabled", visible=False)
                    gr.Markdown("---", elem_id="my_llama_auto_mode_interactive_chatbot_divider")
                    with gr.Row(elem_id="my_aim_chatbot_switch_from_auto_mode_button_row"):
                        gr.HTML(svg["button_aim_iso_with_text_bubble"])
                        aim_chatbot_switch_from_auto_mode_button = gr.Button("", elem_id="my_chatbot_switch_button_clickable", min_width=0)
                with gr.Row(elem_id="my_chatbot_auto_mode_video_graph_switch_button_row", visible=False):
                    chatbot_auto_mode_video_button = gr.Button("Video", elem_classes=["my_chatbot_auto_mode_video_graph_switch_button_class", "clicked"], elem_id="my_chatbot_auto_mode_video_button", min_width=0)
                    chatbot_auto_mode_graph_button = gr.Button("Graph", elem_classes=["my_chatbot_auto_mode_video_graph_switch_button_class"], elem_id="my_chatbot_auto_mode_graph_button", min_width=0)
                with gr.Row(elem_classes="my_chatbot_auto_mode_mid_row_right_elem_wrapper_class", elem_id="my_chatbot_auto_mode_mid_row_video_wrapper", visible=True) as llama_auto_mode_video_wrapper_row:
                    gr.Video(value="assets/video/CES_2025.mp4", visible=True, autoplay=True, loop=True, elem_id="my_chatbot_auto_mode_video", show_download_button=False, container=False)
                with gr.Row(elem_classes="my_chatbot_auto_mode_mid_row_right_elem_wrapper_class", elem_id="my_chatbot_auto_mode_mid_row_plot_wrapper", visible=False) as llama_auto_mode_plot_wrapper_row:
                    with gr.Row(elem_id="my_chatbot_auto_mode_mid_row_plotly_icon_row") as auto_mode_plotly_icon_row:
                        gr.HTML(svg["plotly_icon"], elem_id="my_chatbot_auto_mode_mid_row_plotly_icon_svg")
                    llama_auto_mode_plot_label = gr.Label("Inference Latency of Llama 3 8B", elem_id="my_llama_auto_mode_plot_label", visible=False, min_width=0, show_label=False, container=False)
                    llama_auto_mode_plot = gr.Plot(container=False, elem_id="my_llama_auto_mode_plot")
        with gr.Row(elem_classes="my_chatbot_container_top_row_class"):
            with gr.Row(elem_classes="my_dot_button_row_class"):
                gr.HTML(svg["button_dot"])
                llama_auto_mode_dot_button = gr.Button("", elem_classes="my_dot_button_clickable_class")
            with gr.Row(elem_classes="my_skhynix_aim_logo_row_class"):
                gr.HTML(svg["skhynix_aim_logo"])
            with gr.Row(elem_classes="my_reset_button_row_class"):
                gr.HTML(svg["button_reset"])
                llama_auto_mode_reset_button = gr.Button("", elem_classes="my_reset_button_clickable_class")
            llama_auto_mode_top_row_disabled = gr.Row(elem_classes="my_chatbot_container_top_row_disabled_class", visible=False)
    with gr.Row(elem_classes="my_chatbot_container_row_class", visible=False) as aim_chatbot_container_row:
        gr.Row(elem_id="my_aim_chatbot_container_row_background")
        with gr.Row(elem_classes="my_chatbot_container_top_row_class"):
            with gr.Row(elem_classes="my_dot_button_row_class"):
                gr.HTML(svg["button_dot"])
                aim_dot_button = gr.Button("", elem_classes="my_dot_button_clickable_class")
            with gr.Row(elem_classes="my_skhynix_aim_logo_row_class"):
                gr.HTML(svg["skhynix_aim_logo"])
            with gr.Row(elem_classes="my_reset_button_row_class"):
                gr.HTML(svg["button_reset"])
                aim_reset_button = gr.Button("", elem_classes="my_reset_button_clickable_class")
            aim_top_row_disabled = gr.Row(elem_classes="my_chatbot_container_top_row_disabled_class", visible=False)
        with gr.Row(elem_classes="my_chatbot_container_mid_row_class"):
            with gr.Row(elem_classes="my_chatbot_row_class", visible=True) as aim_chatbot_row:
                with gr.Row(elem_classes="my_horizontal_line_markdown_top_class"):
                    gr.Markdown("---")
                aim_chatbot = gr.Chatbot(None, type="messages", elem_classes="my_chatbot_class", elem_id="my_aim_chatbot", show_label=False, height="100%", avatar_images=(None, "assets/images/aim_avatar_purple.png"))
                aim_chatbot_generation_state = gr.State(False)
                with gr.Row(elem_id="my_llama_chatbot_switch_button_row", elem_classes="my_chatbot_switch_button_row_class") as llama_chatbot_switch_button_row:
                    gr.Image("assets/images/llama_avatar.png", elem_id="my_llama_chatbot_switch_button_image", container=False, min_width=0, interactive=False, show_download_button=False, show_fullscreen_button=False, show_share_button=False, show_label=False)
                    # gr.HTML(svg["button_llama_iso"])
                    llama_chatbot_switch_button = gr.Button("", elem_classes="my_chatbot_switch_button_clickable_class", min_width=0)
                with gr.Row(elem_classes="my_horizontal_line_markdown_bottom_class"):
                    gr.Markdown("---")
        with gr.Row(elem_classes="my_chatbot_container_bottom_row_class"):
            user_aim_prompt_textbox = gr.Textbox(elem_classes="my_user_prompt_textbox_class", elem_id="my_user_aim_prompt_textbox", show_label=False, container=False, lines=1, max_lines=1, placeholder="", min_width=0)
            gr.HTML(svg["button_submit"], elem_classes="my_user_prompt_submit_button_html_class")
            aim_submit_button = gr.Button("", elem_classes="my_user_prompt_submit_button_clickable_class", min_width=0)
            aim_bottom_row_disabled = gr.Row(elem_classes="my_chatbot_container_bottom_row_disabled_class", visible=False)
    with gr.Row(elem_id="my_popup_row", visible=False) as popup_row:
        with gr.Row(elem_id="my_popup_top_row"):
            with gr.Row(elem_id="my_popup_logo_row"):
                gr.HTML(svg["skhynix_aim_logo"], visible=False)
            with gr.Row(elem_id="my_popup_close_button_row"):
                gr.HTML(svg["button_close"])
                close_button = gr.Button("", elem_id="my_popup_close_button_clickable")
        with gr.Row(elem_id="my_information_row"):
            gr.Markdown(about_demo, elem_id="my_information_markdown")
            with gr.Row(elem_id="my_admin_setting_row", visible=False) as admin_setting_row:
                gr.Markdown("# Admin Setting", elem_id="my_admin_setting_title_markdown")
                with gr.Row(elem_id="my_mode_row"):
                    gr.Markdown("## Demo Mode", elem_id="my_mode_title_markdown")
                    mode_radio = gr.Radio(choices=["Interactive", "Auto"], value="Interactive", show_label=False, elem_id="my_mode_radio", interactive=True)
                    auto_mode_start_radio = gr.Radio(choices=["Start", "Pause"], value="Start", show_label=False, elem_id="my_auto_mode_start_radio", interactive=True, visible=False)
                    mode_state = gr.State(value="Interactive")
                    auto_mode_start_state = gr.State(value="Start")
                    auto_mode_interval_number = gr.Number(auto_mode_timer_interval, precision=0, minimum=1, label="Auto Mode Interval", elem_id="my_auto_mode_interval_number", interactive=True)
                    auto_mode_batch_number = gr.Number(initial_batch_num, precision=0, minimum=2, maximum=initial_batch_num, label="Batch Num", elem_id="my_auto_mode_batch_number", interactive=True)
                    llama_auto_mode_batch_input_textbox_list = []
                    with gr.Tabs(elem_id="my_auto_mode_batch_input_tabs") as auto_mode_batch_input_tabs:
                        for i, b in enumerate(initial_llama_auto_mode_batch_input_list[:initial_batch_num - 1]):
                            with gr.TabItem(i+1, id=i):
                                llama_auto_mode_batch_input_textbox_list.append(gr.Textbox(b, container=False, show_label=False))
        with gr.Row(elem_id="my_popup_bottom_row"):
            admin_setting_button = gr.Button("", elem_id="my_admin_setting_button", min_width=0)

    auto_mode_batch_number.change(
        lambda auto_mode_batch_num: [gr.Chatbot(visible=True, type="messages", elem_classes="my_chatbot_class", elem_id="my_chatbot_auto_mode_batch_chatbot", show_label=False, height="100%", avatar_images=("assets/images/question_avatar.png", "assets/images/llama_avatar.png"))] * (auto_mode_batch_num - 1) + [gr.Chatbot(visible=False, type="messages", elem_classes="my_chatbot_class", elem_id="my_chatbot_auto_mode_batch_chatbot", show_label=False, height="100%", avatar_images=("assets/images/question_avatar.png", "assets/images/llama_avatar.png"))] * ((initial_batch_num - 1) - (auto_mode_batch_num - 1)),
        auto_mode_batch_number,
        llama_auto_mode_chatbot_batch_list,
        show_progress="hidden"
    )

    gr.on(
        triggers=[user_llama_prompt_textbox.submit, llama_submit_button.click],
        fn=process_user_prompt,
        inputs=[user_llama_prompt_textbox, user_llama_prompt_counter_state],
        outputs=user_llama_prompt_counter_state,
        show_progress="hidden"
    )

    gr.on(
        triggers=[llama_auto_mode_chatbot_textbox.submit, llama_auto_mode_chatbot_submit_button.click],
        fn=lambda llama_auto_mode_chatbot_textbox: llama_auto_mode_chatbot_textbox if llama_auto_mode_chatbot_textbox != "" else random.choice(SAMPLE_TEXT),
        inputs=llama_auto_mode_chatbot_textbox,
        outputs=llama_auto_mode_chatbot_textbox,
        show_progress="hidden"
    ).then(
        process_user_prompt,
        [llama_auto_mode_chatbot_textbox, user_llama_auto_mode_prompt_counter_state],
        user_llama_auto_mode_prompt_counter_state,
        show_progress="hidden"
    )

    user_llama_auto_mode_prompt_counter_state.change(
        lambda: [gr.Textbox(interactive=False)] + [gr.Row(visible=True)] * 2, None, [llama_auto_mode_chatbot_textbox, llama_auto_mode_top_row_disabled, llama_auto_mode_chatbot_disabled], show_progress="hidden"
    ).then(
        clear_llama_plot, None, [llama_auto_mode_plot, auto_mode_plotly_icon_row, llama_auto_mode_plot_label], show_progress="hidden"
    ).then(
        lambda: True, None, llama_auto_mode_chatbot_generation_state
    ).then(
        send_user_llama_prompt, [llama_auto_mode_chatbot_textbox, llama_auto_mode_interactive_chatbot], [llama_auto_mode_chatbot_textbox, llama_auto_mode_interactive_chatbot], show_progress="hidden"
    ).then(
        receive_llama_chatbot_answer, [llama_auto_mode_interactive_chatbot, gr.State(False)], llama_auto_mode_interactive_chatbot, show_progress="minimal"
    ).then(
        create_llama_plot, [llama_chatbot_generation_state, llama_auto_mode_chatbot_generation_state], [llama_auto_mode_plot, auto_mode_plotly_icon_row, llama_auto_mode_plot_label], show_progress="hidden"
    ).then(
        lambda: False, None, llama_auto_mode_chatbot_generation_state
    ).then(
        lambda: [gr.Textbox(interactive=True)] + [gr.Row(visible=False)] * 2, None, [llama_auto_mode_chatbot_textbox, llama_auto_mode_top_row_disabled, llama_auto_mode_chatbot_disabled], show_progress="hidden"
    )

    llama_auto_mode_reset_button.click(
        lambda: initial_auto_mode_llama_greeting_message, None, llama_auto_mode_interactive_chatbot, show_progress="hidden"
    ).then(
        clear_llama_plot, None, [llama_auto_mode_plot, auto_mode_plotly_icon_row, llama_auto_mode_plot_label], show_progress="hidden"
    ).then(
        pick_llama_sample_prompt, None, llama_auto_mode_chatbot_textbox, show_progress="hidden"
    ).then(
        reset_llama_auto_mode_chatbot_batch, llama_auto_mode_chatbot_batch_generation_state_list, llama_auto_mode_chatbot_batch_list, show_progress="hidden"
    )

    auto_mode_status_quo_timer.tick(
        update_auto_mode_status_quo,
        llama_auto_mode_chatbot_batch_generation_state_list,
        [chatbot_auto_mode_status_quo_running_value_label, chatbot_auto_mode_status_quo_waiting_value_label],
        show_progress="hidden"
    )

    for llama_sample_prompt_button in llama_sample_prompt_button_list:
        llama_sample_prompt_button.click(click_llama_sample_prompt, [llama_sample_prompt_button, user_llama_prompt_counter_state], [user_llama_prompt_textbox, user_llama_prompt_counter_state], show_progress="hidden")

    user_llama_prompt_counter_state.change(
        disable_llama_interaction, None, [user_llama_prompt_textbox, llama_top_row_disabled, llama_sample_prompt_row_disabled, llama_bottom_row_disabled], show_progress="hidden"
    ).then(
        clear_llama_plot, None, [llama_plot, plotly_icon_row, llama_plot_label], show_progress="hidden"
    ).then(
        view_llama_chatbot, None, [llama_landing_page_row, llama_chatbot_row], show_progress="hidden"
    ).then(
        lock_before_llm_generation, None, llama_chatbot_generation_state
    ).then(
        send_user_llama_prompt, [user_llama_prompt_textbox, llama_chatbot], [user_llama_prompt_textbox, llama_chatbot], show_progress="hidden"
    ).then(
        receive_llama_chatbot_answer, [llama_chatbot, gr.State(False)], llama_chatbot, show_progress="minimal"
    ).then(
        create_llama_plot, [llama_chatbot_generation_state, llama_auto_mode_chatbot_generation_state], [llama_plot, plotly_icon_row, llama_plot_label], show_progress="hidden"
    ).then(
        unlock_after_llm_generation, None, llama_chatbot_generation_state
    ).then(
        enable_llama_interaction, None, [user_llama_prompt_textbox, llama_top_row_disabled, llama_sample_prompt_row_disabled, llama_bottom_row_disabled], show_progress="hidden"
    )

    test_image_input.upload(
        lambda: [gr.Image(visible=False), gr.Image(visible=True)], None, [test_image_input, test_image_output], show_progress="hidden"
    ).then(
        sepia, test_image_input, test_image_output
    )

    llama_reset_button.click(
        reset_llama_interface, None, [llama_chatbot, llama_landing_page_row, llama_chatbot_row], show_progress="hidden"
    ).then(
        clear_llama_plot, None, [llama_plot, plotly_icon_row, llama_plot_label], show_progress="hidden"
    ).then(
        lambda: [None, None], None, [test_image_input, test_image_output], show_progress="hidden"
    ).then(
        lambda: [gr.Image(visible=True), gr.Image(visible=False)], None, [test_image_input, test_image_output], show_progress="hidden"
    )

    gr.on(
        triggers=[llama_dot_button.click, aim_dot_button.click, llama_auto_mode_dot_button.click],
        fn=open_popup,
        inputs=None,
        outputs=popup_row,
        show_progress="hidden"
    )

    mode_radio.change(lambda demo_mode: gr.Radio(visible=(False if demo_mode == "Interactive" else True)), mode_radio, auto_mode_start_radio, show_progress="hidden")

    close_button.click(
        close_popup, None, [popup_row, admin_setting_row], show_progress="hidden"
    ).then(
        update_llama_mode, [mode_radio, mode_state], mode_state
    ).then(
        update_llama_mode, [auto_mode_start_radio, auto_mode_start_state], auto_mode_start_state
    )

    chatbot_auto_mode_video_button.click(
        lambda: [
            gr.Row(visible=True),
            gr.Row(visible=False),
            gr.Button(elem_classes=["my_chatbot_auto_mode_video_graph_switch_button_class", "clicked"]),
            gr.Button(elem_classes=["my_chatbot_auto_mode_video_graph_switch_button_class"]),
        ],
        None,
        [llama_auto_mode_video_wrapper_row, llama_auto_mode_plot_wrapper_row, chatbot_auto_mode_video_button, chatbot_auto_mode_graph_button],
        show_progress="hidden"
    )

    chatbot_auto_mode_graph_button.click(
        lambda: [
            gr.Row(visible=False),
            gr.Row(visible=True),
            gr.Button(elem_classes=["my_chatbot_auto_mode_video_graph_switch_button_class"]),
            gr.Button(elem_classes=["my_chatbot_auto_mode_video_graph_switch_button_class", "clicked"]),
        ],
        None,
        [llama_auto_mode_video_wrapper_row, llama_auto_mode_plot_wrapper_row, chatbot_auto_mode_video_button, chatbot_auto_mode_graph_button],
        show_progress="hidden"
    )

    llama_auto_mode_chatbot_batch_start_button.click(
        lambda: ["Start"] * 2, None, [auto_mode_start_radio, auto_mode_start_state]
    )

    llama_auto_mode_chatbot_batch_pause_button.click(
        lambda: ["Pause"] * 2, None, [auto_mode_start_radio, auto_mode_start_state]
    )

    gr.on(
        triggers=[mode_state.change, auto_mode_start_state.change],
        fn=lambda mode_state, auto_mode_start_state, auto_mode_interval_number: [gr.Timer(value=auto_mode_interval_number, active=(mode_state == "Auto" and auto_mode_start_state == "Start"))] * (initial_batch_num - 1),
        inputs=[mode_state, auto_mode_start_state, auto_mode_interval_number],
        outputs=llama_auto_mode_chatbot_batch_timer_list,
        show_progress="hidden"
    ).then(
        exit_auto_mode_batch, auto_mode_start_state, None, show_progress="hidden"
    ).then(
        lambda mode_state: [gr.Row(visible=(mode_state == "Interactive")), gr.Row(visible=(mode_state == "Auto"))],
        mode_state,
        [llama_chatbot_container_row, llama_chatbot_auto_mode_container_row],
        show_progress="hidden"
    ).then(
        show_llama_mode_info, [mode_state, auto_mode_start_state, auto_mode_interval_number], None, show_progress="hidden"
    )

    for i in range(initial_batch_num - 1):
        llama_auto_mode_chatbot_batch_timer_list[i].tick(
            trigger_llama_auto_mode_chatbot,
            [llama_auto_mode_chatbot_batch_generation_state_list[i], llama_auto_mode_chatbot_batch_counter_state_list[i], auto_mode_batch_number, gr.State(i)],
            llama_auto_mode_chatbot_batch_counter_state_list[i]
        )

    for i in range(initial_batch_num - 1):
        llama_auto_mode_chatbot_batch_counter_state_list[i].change(
            lambda: gr.Timer(active=False), None, llama_auto_mode_chatbot_batch_timer_list[i]
        ).then(
            lambda: True, None, llama_auto_mode_chatbot_batch_generation_state_list[i]
        ).then(
            lambda: random.choice(SAMPLE_TEXT), None, llama_auto_mode_batch_input_textbox_list[i]
        ).then(
            send_user_llama_prompt,
            [llama_auto_mode_batch_input_textbox_list[i], llama_auto_mode_chatbot_batch_list[i]],
            [gr.Textbox(visible=False), llama_auto_mode_chatbot_batch_list[i]],
            show_progress="hidden"
        ).then(
            receive_llama_chatbot_answer, [llama_auto_mode_chatbot_batch_list[i], gr.State(True)], llama_auto_mode_chatbot_batch_list[i], show_progress="minimal"
        ).then(
            lambda: False, None, llama_auto_mode_chatbot_batch_generation_state_list[i]
        ).then(
            lambda mode_state, auto_mode_start_state, auto_mode_interval_number: gr.Timer(value=auto_mode_interval_number, active=(mode_state == "Auto" and auto_mode_start_state == "Start")),
            [mode_state, auto_mode_start_state, auto_mode_interval_number],
            llama_auto_mode_chatbot_batch_timer_list[i]
        )

    admin_setting_button.click(open_admin_setting, None, admin_setting_row, show_progress="hidden")

    gr.on(
        triggers=[aim_chatbot_switch_button.click, aim_chatbot_switch_button_in_landing_page.click, aim_chatbot_switch_from_auto_mode_button.click],
        fn=lambda: gr.Row(visible=True),
        inputs=None,
        outputs=aim_chatbot_container_row,
        show_progress="hidden"
    ).then(
        lambda user_aim_prompt_counter, chatbot_state: user_aim_prompt_counter + 1 if chatbot_state == 0 else user_aim_prompt_counter,
        [user_aim_prompt_counter_state, aim_chatbot_state],
        user_aim_prompt_counter_state
    )

    llama_chatbot_switch_button.click(
        lambda: gr.Row(visible=False), None, aim_chatbot_container_row
    )

    aim_reset_button.click(
        lambda: [None, 0], None, [aim_chatbot, aim_chatbot_state], show_progress="hidden"
    ).then(
        lambda user_aim_prompt_counter: user_aim_prompt_counter + 1, user_aim_prompt_counter_state, user_aim_prompt_counter_state
    )

    gr.on(
        triggers=[user_aim_prompt_textbox.submit, aim_submit_button.click],
        fn=process_user_prompt,
        inputs=[user_aim_prompt_textbox, user_aim_prompt_counter_state],
        outputs=user_aim_prompt_counter_state,
        show_progress="hidden"
    )

    user_aim_prompt_counter_state.change(
        send_user_aim_prompt, [user_aim_prompt_textbox, aim_chatbot, aim_chatbot_state], [user_aim_prompt_textbox, aim_chatbot], show_progress="hidden"
    ).then(
        lambda: gr.Textbox(interactive=False), None, user_aim_prompt_textbox, show_progress="hidden"
    ).then(
        receive_aim_chatbot_answer_2,
        [aim_chatbot, aim_chatbot_state, aim_chatbot_quiz_index_state],
        [aim_chatbot, aim_chatbot_state, aim_chatbot_quiz_index_state, user_aim_prompt_textbox],
        show_progress="minimal"
    )

demo.queue(default_concurrency_limit=None).launch(
    max_threads=32,
    server_port=6006,
    server_name="0.0.0.0",
    favicon_path="assets/images/favicon.png",
    share=True
)
