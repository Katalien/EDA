from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
import io
import numpy as np
from PIL import Image as PILImage



class PdfWriter:
    def create_pdf_report(self, feature_data_list, plots, dataset_count_dict, output_filename):
        doc = SimpleDocTemplate(output_filename, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph("Images report", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Adding dataset count information
        for folder, count in dataset_count_dict.items():
            count_paragraph = Paragraph(f"Folder '{folder}': {count} images", styles['Normal'])
            elements.append(count_paragraph)
            elements.append(Spacer(1, 12))

        num_features = len(feature_data_list)
        num_images_text = Paragraph(f"Amount of features: {num_features}", styles['Normal'])
        elements.append(num_images_text)
        elements.append(Spacer(1, 12))

        self.data = [['Feature name', 'Min', 'Max', 'Mean', 'Std']]

        for feature_data in feature_data_list:
            if feature_data.min is None and feature_data.max is None and feature_data.std is None and feature_data.mean is None:
                continue
            if feature_data.feature_name in ["R", "G", "B"]:
                continue

            row = [
                feature_data.feature_name,
                self.format_value(feature_data.min),
                self.format_value(feature_data.max),
                self.format_value(feature_data.mean),
                self.format_value(feature_data.std)
            ]

            # Добавляем строку в таблицу
            self.data.append(row)


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

            if not feature_data.is_img:
                # Save plot to memory
                img_buffer = io.BytesIO()
                plot.savefig(img_buffer, format='PNG')
                img_buffer.seek(0)
            else:
                img_array = np.uint8(feature_data.data)
                pil_img = PILImage.fromarray(img_array)

                # Save PIL Image to memory
                img_buffer = io.BytesIO()
                pil_img.save(img_buffer, format='PNG')
                img_buffer.seek(0)

            # Insert plot image into PDF
            img = Image(img_buffer)
            img.drawHeight = 6 * 72  # 6 inches height
            img.drawWidth = 6 * 72  # 6 inches width
            elements.append(img)
            elements.append(Spacer(1, 12))


        # Save PDF
        doc.build(elements)

    def format_value(self, value):
        return f"{value:.1f}" if value is not None else ''