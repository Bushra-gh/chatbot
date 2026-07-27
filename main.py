from logic import generate_response, log_conversation, user_memory

print(f"Chatbot: Hello! My name is {user_memory['bot_name']}, the terminal chatbot! Ask me anything. Type 'bye' to exit.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "exit", "quit"]:
        farewell = "Goodbye!"
        if "name" in user_memory:
            farewell = f"Goodbye, {user_memory['name']}!"
        print(f"Chatbot: {farewell}")
        log_conversation("You", user_input)
        log_conversation("Bot", farewell)
        break

    response = generate_response(user_input)
    print(f"Chatbot: {response}")

    log_conversation("You", user_input)
    log_conversation("Bot", response)
