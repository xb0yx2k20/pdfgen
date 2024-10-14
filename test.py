from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import os

class PDFLetter:
    def __init__(self, filename, num, date, subject, object_name, address, recipient, dear, body, sender_position, sender_name, name_send, num_send, email, image_path):
        self.filename = filename
        self.num = num
        self.date = date
        self.subject = subject
        self.object_name = object_name
        self.address = address
        self.recipient = recipient
        self.dear = dear
        self.body = body
        self.sender_position = sender_position
        self.sender_name = sender_name
        self.name_send = name_send
        self.num_send = num_send
        self.email = email
        self.image_path = 'A.jpg'

    def convert_image(self):
        # Путь для сохранения изображения без альфа-канала
        converted_image_path = self.image_path.replace('.png', '_converted.jpg')
        
        # Открытие изображения и его преобразование
        with Image.open(self.image_path) as img:
            img.convert("RGB").save(converted_image_path, "JPEG")
        
        return converted_image_path

    def wrap_text(self, text, max_width, font_name, font_size):
        """Разбивает текст на строки с учетом ширины."""
        from reportlab.pdfbase import pdfmetrics
        
        # pdfmetrics.registerFont(pdfmetrics.getRegisteredFont(font_name))
        # pdfmetrics.setFont(font_name, font_size)

        words = text.split(' ')
        lines = []
        current_line = ''
        
        # Устанавливаем ширину текста
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if pdfmetrics.stringWidth(test_line, font_name, font_size) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)

        return lines

    def generate_pdf(self):
        # Преобразование изображения
        converted_image_path = self.convert_image()

        c = canvas.Canvas(self.filename, pagesize=A4)
        width, height = A4

        # Проверка существования файла изображения
        if not os.path.exists(converted_image_path):
            print(f"Error: The image file {converted_image_path} does not exist.")
            return
        
        # Добавление изображения в верхней части документа
        try:
            c.drawImage(converted_image_path, 1 * inch, height - 1 * inch - 50, width=100, height=100)  # Укажите ширину и высоту изображения
        except Exception as e:
            print(f"Error adding image: {e}")

        # Company header (centered)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1 * inch, height - 1.9 * inch, 'LLC "A Plus"')
        c.setFont("Helvetica", 10)
        c.drawString(1 * inch, height - 2.1 * inch, 'INN 9707030824')
        c.drawString(1 * inch, height - 2.3 * inch, 'KPP 770701001')
        c.drawString(1 * inch, height - 2.5 * inch, f'No {self.num} dated {self.date}')

        # Object information (left aligned)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1 * inch, height - 2.9 * inch, 'Subject:')
        c.setFont("Helvetica", 10)
        c.drawString(1 * inch, height - 3.1 * inch, f'Subject: {self.subject}')
        c.drawString(1 * inch, height - 3.3 * inch, f'Object: {self.object_name}')
        c.drawString(1 * inch, height - 3.5 * inch, f'Address: {self.address}')
        c.drawString(1 * inch, height - 3.7 * inch, f'To: {self.recipient}')

        # Body of the letter (centered)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(width / 2, height - 4.4 * inch, self.dear)
        c.setFont("Helvetica", 10)

        # Установка ширины текста
        text_width = width - 2 * inch  # Ширина области текста
        wrapped_lines = self.wrap_text(self.body, text_width, "Helvetica", 10)

        # Рисуем обернутый текст
        text_y = height - 4.9 * inch
        for line in wrapped_lines:
            c.drawString(1 * inch, text_y, line)
            text_y -= 12  # Отступ между строками

        # Signature (left aligned)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1 * inch, text_y, self.sender_position)
        c.drawString(5.5 * inch, text_y, f'_____________')

        c.setFont("Helvetica-Bold", 10)
        text_y -= 12  # Отступ между строками
        c.drawString(5.5 * inch, text_y, self.sender_name)

        # Contact information (left aligned)
        c.setFont("Helvetica", 9)  
        text_y -= 12  # Отступ между строками
        c.drawString(1 * inch, text_y, f'From: {self.name_send}')
        text_y -= 12
        c.drawString(1 * inch, text_y, self.num_send)
        text_y -= 12
        c.drawString(1 * inch, text_y, self.email)
        
        # Company address (centered)
        text_y -= 12  # Отступ между строками
        c.drawCentredString(width / 2, text_y, '127006, Moscow, Malaya Dmitrovka St., 18A, bldg. 3, e-mail: info@a-pluse.ru')

        # Finish and save PDF
        c.save()

if __name__ == "__main__":
    # Parameters for filling the template
    pdf_letter = PDFLetter(
        filename="letter.pdf",
        num="123",
        date="14.10.2024",
        subject="Information Technology",
        object_name="Project",
        address="Moscow, Sample St., 1",
        recipient="Ivanov I.I.",
        dear="Dear Ivan Ivanovich!",
        body="Letter content. Here you can write the main information. Letter content. Here you can write the main information. Letter content. Here you can write the main information. Letter content. Here you can write the main information. Letter content. Here you can write the main information. Letter content. Here you can write the main information.",
        sender_position="Director",
        sender_name="Ivanov I.I.",
        name_send="Petrov P.P.",
        num_send="89161234567",
        email="petrov@example.com",
        image_path="path/to/your/image.png"  # Укажите путь к вашему изображению
    )

    # Generate PDF
    pdf_letter.generate_pdf()