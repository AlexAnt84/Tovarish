from ollama import chat

message = [
    {
        "role": "system",
        "content": (
            "Ты Товарищ, дружелюбный русскоязычный собеседник. "
            "Отвечай на последнее сообщение пользователя. "
            "Не меняй тему без причины."
        )
    }
]

while True:
    user_input = input("Написать товарищу: ")
    if user_input.lower() == "выход":
        break




    message.append(
       {"role": "user", "content": user_input}
    )






    response = chat(model="gemma3:4b", messages=message)

    message.append(
         {"role": "assistant", "content": response.message.content }
     )

    print (response.message.content)
