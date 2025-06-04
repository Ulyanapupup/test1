import json, os

json_path = os.path.join('game_logic', 'questions_1_2.json')

with open(json_path, 'r', encoding='utf-8') as f:
    question_map = json.load(f)

possible_numbers = list(range(101))
asked_questions = set()

# Диапазон для бинарного поиска
min_possible = 0
max_possible = 100

def reset():
    global possible_numbers, asked_questions, min_possible, max_possible
    possible_numbers = list(range(101))
    asked_questions = set()
    min_possible = 0
    max_possible = 100

def is_even(n): return n % 2 == 0
def is_odd(n): return n % 2 == 1
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0: return False
    return True

question_functions = {
    "is_even": is_even,
    "is_odd": is_odd,
    "is_prime": is_prime
}

# Уникальные логические вопросы
unique_questions = {
    "число чётное": is_even,
    "число нечётное": is_odd,
    "число простое": is_prime
}

def next_question():
    global min_possible, max_possible

    # Если остался 1 вариант — угадываем
    if len(possible_numbers) == 1:
        return f"Я знаю! Это число {possible_numbers[0]}", True

    # Сначала — уникальные логические вопросы
    for q in unique_questions:
        if q not in asked_questions:
            asked_questions.add(q)
            return q, False

    # Затем — бинарный поиск
    if min_possible >= max_possible:
        return "Упс, вы меня запутали 🙃", True

    mid = (min_possible + max_possible) // 2
    question = f"больше {mid}"
    asked_questions.add(question)
    return f"Число {question}?", False

def process_answer(user_answer):
    global possible_numbers, min_possible, max_possible

    answer = user_answer.strip().lower()
    if answer not in ["да", "нет"]:
        return "Пожалуйста, отвечайте 'да' или 'нет'", False

    last_question = list(asked_questions)[-1]

    if last_question in unique_questions:
        func = unique_questions[last_question]
        yes = answer == "да"
        possible_numbers = [n for n in possible_numbers if func(n) == yes]
    elif "больше" in last_question:
        number = int(last_question.split()[-1])
        if answer == "да":
            min_possible = number + 1
            possible_numbers = [n for n in possible_numbers if n > number]
        else:
            max_possible = number
            possible_numbers = [n for n in possible_numbers if n <= number]

    if len(possible_numbers) == 1:
        return f"Я знаю! Это число {possible_numbers[0]}", True
    if len(possible_numbers) == 0:
        return "Вы, похоже, ответили не последовательно 🙃", True

    return next_question()
