from g4f.client import Client

client = Client()


def gpt(user_question):
    context = [
    {
        "role": "system",
        "content": "Моя цель — чтобы ты взял код, написанный на HTML, и преобразовал его в код LaTeX, но без использования каких-либо внешних команд или настроек, таких как 'documentclass', 'usepackage' или других подобных инструкций. Переведённый текст должен быть на чистом LaTeX, без дополнительных комментариев и структурных элементов, характерных для оформления документа. Содержимое текста, которое ты переводишь, может быть абсолютно любым, тебе не нужно придерживаться исходного содержания, главное — конвертировать HTML в LaTeX."
    },
    {
        "role": "user",
        "content": user_question
    }
]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=context
        )

        bot_answer = response.choices[0].message.content


        return bot_answer

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return (f"Ошибка: {str(e)}")


question = '<ol><li><b style="text-align: var(--bs-body-text-align);">Проверка</b><br></li><li><i style="text-align: var(--bs-body-text-align);">Chat</i><br></li><li><u style="text-align: var(--bs-body-text-align);"><b><i>GPT</i></b></u><br></li></ol>'

print(gpt(question))