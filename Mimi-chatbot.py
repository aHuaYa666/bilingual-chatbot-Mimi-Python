# Program: Mimi's Magical Book of Answers 🐾
# Description: 
#   A fun bilingual chatbot that gives random yes/no/maybe style answers 
#   in English or Chinese based on a local answers.txt file.
#   Users ask light-hearted questions, and Mimi responds with a playful twist!
#
# Author: Jinlin Duan
# Date: 05/10/2025
# Revised: 
#   05/18/2025

# import library modules here
import random
import os
from datetime import datetime

# Define global constants (name in ALL_CAPS)
YES_NO_STARTS_EN = ("is", "are", "do", "does", "will", "should", "can", "could", "would", "am")
YES_NO_KEYWORDS_ZH = ('吗', '是不是', '会不会', '能不能', '可不可以', '有没有', '是否', '对不对', '行不行', '好不好', '会不会', '可以吗', '对吗', '是吗')

# Function to load answers from the TXT file
def load_answers(file_path):
    answers = {'English': [], '中文': []}

    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return answers

    with open(file_path, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(' : ', 3)
                if len(parts) == 2:
                    english, chinese = parts
                    answers['English'].append(english.strip())
                    answers['中文'].append(chinese.strip())
                else:
                    print(f"Warning: Skipping improperly formatted line: {line}")
    return answers

# Function to check if the input is a yes/no question
def is_yes_no_question(input_text, language):
    input_text = input_text.strip().lower()
    if language == 'English':
        return input_text.endswith('?') and input_text.split()[0] in YES_NO_STARTS_EN
    else:
        if not input_text.endswith('？'):
            return False
        # 更智能的中文是非问题检测
        return any(keyword in input_text for keyword in YES_NO_KEYWORDS_ZH)

# Function to display language selection menu
def select_language():
    print("\nPlease select your language / 请选择你的语言：")
    print("1. English")
    print("2. 中文")
    choice = input("Enter your choice (1 or 2) / 输入你的选择 (1 或 2)：").strip()

    if choice == '1':
        return 'English'
    elif choice == '2':
        return '中文'
    else:
        print("Invalid choice. Defaulting to English. / 无效选择，默认使用英文。")
        return 'English'

# Function to get a random answer
def get_random_answer(answers, language):
    if answers[language]:
        return random.choice(answers[language])
    else:
        return "I don't have any answers right now. Please check the file." if language == 'English' else "我现在没有答案。请检查文件。"

# Function to save conversation transcript
def save_transcript(transcript, language):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mimi_transcript_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(transcript)
        if language == 'English':
            print(f"\nConversation saved to {filename}")
        else:
            print(f"\n对话已保存到 {filename}")
    except Exception as e:
        if language == 'English':
            print(f"\nFailed to save transcript: {e}")
        else:
            print(f"\n保存对话失败: {e}")

# Main chatbot loop
def chatbot():
    language = select_language()
    file_path = r'answers.txt'  
    answers = load_answers(file_path)
    transcript = ""

    # Add initial greeting to transcript
    if language == 'English':
        greeting = "\nWelcome to the Online Book of Answers!\nI'm Mimi 🐾. Ask me yes/no questions, and type 'quit' or 'q' to exit.\n"
        transcript += greeting
        print(greeting)
    else:
        greeting = "\n欢迎来到在线答案之书！\n我是咪咪 🐾。请用'吗/是不是/会不会'等结尾的是非类问题提问，输入'退出'或'q'结束对话。\n"
        transcript += greeting
        print(greeting)

    while True:
        if language == 'English':
            user_input = input("\nYou: ").strip()
            transcript += f"You: {user_input}\n"
        else:
            user_input = input("\n你：").strip()
            transcript += f"你：{user_input}\n"

        if user_input.lower() in ['quit', 'q', '退出']:
            if language == 'English':
                farewell = "Mimi: Bye! Take care! 🐾"
                print(farewell)
                transcript += farewell + "\n"
            else:
                farewell = "咪咪：再见啦！祝你一切顺利 🐾"
                print(farewell)
                transcript += farewell + "\n"
            
            # Ask to save transcript before exiting
            if language == 'English':
                save = input("\nWould you like to save this conversation? (y/n): ").strip().lower()
            else:
                save = input("\n是否保存本次对话？(y/n): ").strip().lower()
            
            if save == 'y' or save == '是':
                save_transcript(transcript, language)
            break

        if not is_yes_no_question(user_input, language):
            if language == 'English':
                response = "Mimi: I can only answer yes/no style questions! Try again 🐾"
                print(response)
                transcript += response + "\n"
            else:
                response = "咪咪：请用带'吗/是不是/会不会'的是非问句提问哦~ 再试一次吧 🐾"
                print(response)
                transcript += response + "\n"
            continue

        answer = get_random_answer(answers, language)
        if language == 'English':
            response = f"Mimi: {answer}"
            print(response)
            transcript += response + "\n"
        else:
            response = f"咪咪：{answer}"
            print(response)
            transcript += response + "\n"

# Run the chatbot
chatbot()
