from g4f.client import Client

client = Client()


def gpt(user_question):
    context = [{"role": "system",
                "content": "Переведи этот код без каких либо комментариев в .tex текстом без documentclass, usepackage и так далее"},
               {"role": "user", "content": user_question}]  # История сообщений

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=context
        )

        bot_answer = response.choices[0].message.content

        print(f"{bot_answer}")

    except Exception as e:
        print(f"Ошибка: {str(e)}")


question = '<div><ol><li><span style="text-align: var(--bs-body-text-align);"><b>Жирный</b></span><br></li><li><span style="text-align: var(--bs-body-text-align);"><i>Курсив</i></span><br></li><li><span style="text-align: var(--bs-body-text-align);"><u>ПОдчеркнутый</u></span><br></li><li><span style="text-align: var(--bs-body-text-align);"><i><u>Общий</u></i></span><br></li></ol></div><div><br></div><div><ul><li><span style="text-align: var(--bs-body-text-align);">Один</span><br></li><li><span style="text-align: var(--bs-body-text-align);">Два</span><br></li><li>Три</li></ul></div>'
