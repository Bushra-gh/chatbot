import random
import datetime
import time
from difflib import get_close_matches

from math_utils import solve_math_expression
from time_utils import get_current_time
from date_utils import get_current_date
from responses import responses, quiz_questions, riddles, stories, definitions, fun_facts

user_memory = {
    "mood": "neutral",
    "quiz_mode": False,
    "quiz_count": 0,
    "quiz_score": 0,
    "quiz_start_time": None
}

mood_responses = {
    "neutral": {
        "default": ["Sorry, I didn't understand that."]
    },
    "friendly": {
        "default": ["Hmm, I'm not sure what you mean, but I appreciate you! 😊"]
    },
    "sarcastic": {
        "default": ["Oh wow, that made *so much* sense... not. 🙄"]
    }
}

intents = {
    "what time is it": "time",
    "what's the time now": "time",
    "can you tell me the time": "time",
    "do you know what time it is": "time",
    "tell me the time": "time",
    "what day is it": "date",
    "what's the date": "date",
    "can you tell me the date": "date",
    "do you know what day it is": "date",
    "umm i forgot": "forgot",
    "what's my name": "name",
    "what is my name": "name",
    "say my name": "name",
    "do you know my name": "name"
}

def detect_intent(user_input, intents):
    match = get_close_matches(user_input, intents.keys(), n=1, cutoff=0.6)
    if match:
        return intents[match[0]]
    return None

def generate_response(user_input):
    original_input = user_input
    user_input = user_input.lower()

    if user_input in ["stop", "end quiz", "quit quiz"]:
        user_memory["quiz_mode"] = False
        summary = f"Quiz ended. You scored {user_memory['quiz_score']} out of {user_memory['quiz_count']} questions."
        if user_memory["quiz_count"] > 0:
            percent = (user_memory['quiz_score'] / user_memory['quiz_count']) * 100
            grade = "A" if percent >= 90 else "B" if percent >= 80 else "C" if percent >= 70 else "D" if percent >= 60 else "F"
            summary += f"\nAccuracy: {percent:.1f}%\nGrade: {grade}"
        if user_memory["quiz_start_time"]:
            elapsed = time.time() - user_memory["quiz_start_time"]
            summary += f"\nTotal time: {int(elapsed)} seconds."
        with open("quiz_results.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()}: {summary}\n")
        user_memory["quiz_count"] = 0
        user_memory["quiz_score"] = 0
        user_memory["quiz_start_time"] = None
        return summary

    if user_input.upper() in ["A", "B", "C", "D"] and "current_quiz" in user_memory:
        correct = user_memory["current_quiz"]["answer"]
        is_correct = user_input.upper() == correct
        if is_correct:
            user_memory["quiz_score"] += 1
        result = "Correct!" if is_correct else f"Wrong. The correct answer was {correct}."
        del user_memory["current_quiz"]
        if user_memory.get("quiz_mode") and user_memory.get("quiz_count", 0) < 50:
            question = random.choice(quiz_questions)
            user_memory["current_quiz"] = question
            user_memory["quiz_count"] += 1
            options = "\n".join(question["options"])
            fact = random.choice(fun_facts)
            return f"{result}\n\n💡 Fun Fact: {fact}\n\n🧠 Next Question:\n{question['question']}\n{options}\n(Type A, B, C, or D)\nType 'stop' to quit."
        return result

    if "quiz" in user_input or "trivia" in user_input:
        user_memory["quiz_mode"] = True
        user_memory["quiz_count"] = 1
        user_memory["quiz_score"] = 0
        user_memory["quiz_start_time"] = time.time()
        question = random.choice(quiz_questions)
        user_memory["current_quiz"] = question
        options = "\n".join(question["options"])
        return f"🧠 Trivia Time!\n{question['question']}\n{options}\n(Type A, B, C, or D)\nType 'stop' to quit."

    if "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip().capitalize()
        user_memory["name"] = name
        return f"Nice to meet you, {name}!"

    intent = detect_intent(user_input, intents)
    if intent == "name":
        if "name" in user_memory:
            return f"Your name is {user_memory['name']}, of course!"
        else:
            return "I don't know your name yet. Tell me by saying 'my name is ...'"
    elif intent == "time":
        return get_current_time()
    elif intent == "date":
        return get_current_date()
    elif intent == "forgot":
        return "It happens! Take your time. 😊"

    if "set mood to" in user_input:
        mood = user_input.split("set mood to")[-1].strip().lower()
        if mood in mood_responses:
            user_memory["mood"] = mood
            return f"Mood set to {mood}."
        else:
            return "I don't recognize that mood. Try 'friendly' or 'sarcastic'."

    if any(op in user_input for op in ["+", "-", "*", "/"]):
        return solve_math_expression(user_input)

    if "riddle" in user_input:
        return random.choice(riddles)

    if "story" in user_input:
        return random.choice(stories)

    if "define" in user_input:
        for word in definitions:
            if word in user_input:
                return f"{word.capitalize()}: {definitions[word]}"
        return "Hmm, I'm not sure about that one. Try 'define AI' or 'define Python'."

    for key in responses:
        if key in user_input:
            return random.choice(responses[key])

    mood = user_memory.get("mood", "neutral")
    return random.choice(mood_responses[mood]["default"])

def log_conversation(speaker, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {speaker}: {message}\n")
