from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- импортируем
import json
import re
import string

app = Flask(__name__)
CORS(app)  # <-- разрешаем CORS

secret_number = 17  # Загаданное число

# Логика
def is_greater(x): return secret_number > x
def is_less(x): return secret_number < x
def is_equal(x): return secret_number == x
def is_prime(_=None):
    if secret_number < 2: return False
    for i in range(2, int(secret_number ** 0.5) + 1):
        if secret_number % i == 0: return False
    return True

question_functions = {
    "is_greater": is_greater,
    "is_less": is_less,
    "is_equal": is_equal,
    "is_prime": is_prime
}

with open('questions.json', 'r', encoding='utf-8') as f:
    question_map = json.load(f)
    

def process_question(q):
    q = q.lower()
    # Удаляем пунктуацию
    q = q.translate(str.maketrans('', '', string.punctuation))
    print(f"Вопрос: {q}")
    for keyword, func_name in question_map.items():
        print(f"Проверяем ключевое слово: '{keyword}'")
        if keyword in q:
            print(f"Найдено ключевое слово: '{keyword}', вызываем функцию: {func_name}")
            func = question_functions[func_name]
            if func_name == "is_prime":
                return "Да" if func() else "Нет"
            else:
                nums = re.findall(r'\d+', q)
                if not nums:
                    return "Пожалуйста, укажите число в вопросе"
                x = int(nums[0])
                return "Да" if func(x) else "Нет"
    print("Ключевые слова не найдены")
    return "Неизвестный вопрос"


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = process_question(question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
