from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
import io
from typing import List
from reportlab.pdfgen.canvas import Canvas


class PdfWriter:
    def create_pdf_report(self, feature_data_list, plots, output_filename):
        doc = SimpleDocTemplate(output_filename, pagesize=letter)
        elements = []

        # Заголовка
        styles = getSampleStyleSheet()
        title = Paragraph("Images report", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Добавление строки с количеством изображений
        num_features = len(feature_data_list)
        num_images_text = Paragraph(f"Amount of features: {num_features}", styles['Normal'])
        elements.append(num_images_text)
        elements.append(Spacer(1, 12))

        # Создание таблицы характеристик
        self.data = [['Feature name', 'Value']]
        for feature_data in feature_data_list:
            self.data.append(['Feature Name', feature_data.feature_name])
            self.data.append(['Min', feature_data.min])
            self.data.append(['Max', feature_data.max])
            self.data.append(['Mean', feature_data.mean])
            self.data.append(['Std', feature_data.std])
            self.data.append(['-' * 20, '-' * 20])  # Разделитель для разных FeatureData


        table = Table(self.data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        # Добавление описаний и графиков
        for i, (feature_data, plot) in enumerate(zip(feature_data_list, plots)):
            # description = Paragraph(f"Graphic {i + 1}: {feature_data.feature_name}", styles['Normal'])
            # elements.append(description)
            elements.append(Spacer(1, 12))

            # Save plot to memory
            img_buffer = io.BytesIO()
            plot.savefig(img_buffer, format='PNG')
            img_buffer.seek(0)

            # Insert plot image into PDF
            img = Image(img_buffer)
            img.drawHeight = 4 * 72  # 6 inches height
            img.drawWidth = 4 * 72  # 6 inches width
            elements.append(img)
            elements.append(Spacer(1, 12))

        # Save PDF
        doc.build(elements)


    def _fill_data_table(self, feature_data):
        pass