from app.chains import get_chain

def run_chat():
    chain = get_chain()

    print("Groq chatbot- Type 'exit' to quit \n")

    while True:
        user_input  = input("Pass tech queries: ")

        if user_input.lower() == "exit":
            break

        response = chain.invoke({"input": user_input})

        print("Bot:", response)

if __name__ == "__main__":
    run_chat()