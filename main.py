import random
def greet():
    greetings = ["Hi!","Hello!","Hey!","Hi there!","What's up?"]
    return random.choice(greetings)
def maths(user_input):
    try:
        ques=user_input.replace("calculate","").replace("what is","").strip()
        ans=eval(ques)
        return f"the answer is {ans}"
    except:
        return "That doesn't look like maths..."
def chatbot():
    return
running=True
print("Bot: " + greet())
while running:
    user_input=input("You: ")
    if "calculate" in user_input.lower():
        print("Bot:", maths(user_input))
    if "exit" in user_input.lower() or "quit" in user_input.lower():
        print("Bot: Goodbye!")
        running=False
        
