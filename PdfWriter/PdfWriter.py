from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
import io
import numpy as np
from PIL import Image as PILImage
from DatasetProcessor import FeatureSummary
from typing import List



class PdfWriter:
    def __init__(self,  features_summaries, dataset_count_dict, output_filename):
        self.styles = getSampleStyleSheet()
        self.elements = []
        self.features_summaries = features_summaries
        self.feature_data_list = self._set_feature_data_list()
        self.dataset_count_dict = dataset_count_dict
        self.output_filename = output_filename

    def _set_feature_data_list(self):
        data_list = []
        for feature_sum in self.features_summaries:
            if not feature_sum.is_img_feature:
                data_list.extend(feature_sum.features_list)
        return data_list


    def write(self,):
        doc = SimpleDocTemplate(self.output_filename, pagesize=letter)
        self._create_title_block()
        self._create_dataset_info_block()
        self._create_table()
        self.elements.append(PageBreak())
        self._create_plots_block()
        doc.build(self.elements)



    def _create_title_block(self):
        title = Paragraph("Images report", self.styles['Title'])
        self.elements.append(title)
        self.elements.append(Spacer(1, 12))

    def _create_dataset_info_block(self):
        description = Paragraph(f"Dataset folders info", self.styles['Heading1'])
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))

        for folder, count in self.dataset_count_dict.items():
            count_paragraph = Paragraph(f"Folder '{folder}': {count} images", self.styles['Normal'])
            self.elements.append(count_paragraph)
            self.elements.append(Spacer(1, 12))

        num_features = len(self.features_summaries)
        num_images_text = Paragraph(f"Amount of features: {num_features}", self.styles['Normal'])
        self.elements.append(num_images_text)
        self.elements.append(Spacer(1, 12))

    def _create_table(self):
        description = Paragraph(f"Dataset feature table", self.styles['Heading1'])
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))
        head = ['Feature name', 'Min', 'Max', 'Mean', 'Std']
        self.data = []

        for feature_data in self.feature_data_list:
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
            self.data.append(row)

        if len(self.data) == 0:
            return

        self.data.insert(0, head)
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
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def _fill_plots_section_info(self):
        feature_plots_dict = {}
        self.elements.append(Spacer(1, 12))
        for i, feature_sum in enumerate(self.features_summaries):
            description = Paragraph(f"Graphic {i + 1}: {feature_sum.feature_name}", self.styles['Heading2'])
            feature_plots_dict[description] = []
            if feature_sum.is_img_feature:
                for feature_img in feature_sum.features_list:
                    img_array = np.uint8(feature_img.data)  #
                    pil_img = PILImage.fromarray(img_array)

                    img_buffer = io.BytesIO()
                    pil_img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)

                    img = Image(img_buffer)
                    feature_plots_dict[description].append(img)
                    del (img_buffer)

            else:
                for plot in feature_sum.plots:
                    img_buffer = io.BytesIO()
                    plot.savefig(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    img = Image(img_buffer)
                    feature_plots_dict[description].append(img)
                    del (img_buffer)
        return feature_plots_dict

    def _create_plots_block(self):
        feature_plots_dict = self._fill_plots_section_info()

        description = Paragraph(f"Feature graphics", self.styles['Heading1'])
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))

        for desc, images in feature_plots_dict.items():
            self.elements.append(desc)
            for img in images:
                img.drawHeight = 4 * 72  # 6 inches height
                img.drawWidth = 6 * 72  # 6 inches width
                self.elements.append(img)
                self.elements.append(Spacer(1, 12))





    #
    #
    # def create_pdf_report(self, features_summaries: List[FeatureSummary], dataset_count_dict, output_filename):
    #     doc = SimpleDocTemplate(output_filename, pagesize=letter)
    #
    #     styles = getSampleStyleSheet()
    #     title = Paragraph("Images report", styles['Title'])
    #     self.elements.append(title)
    #     self.elements.append(Spacer(1, 12))
    #
    #     # Adding dataset count information
    #     for folder, count in dataset_count_dict.items():
    #         count_paragraph = Paragraph(f"Folder '{folder}': {count} images", styles['Normal'])
    #         elements.append(count_paragraph)
    #         elements.append(Spacer(1, 12))
    #
    #     num_features = len(feature_data_list)
    #     num_images_text = Paragraph(f"Amount of features: {num_features}", styles['Normal'])
    #     elements.append(num_images_text)
    #     elements.append(Spacer(1, 12))
    #
    #     self.data = [['Feature name', 'Min', 'Max', 'Mean', 'Std']]
    #
    #     for feature_data in feature_data_list:
    #         if feature_data.min is None and feature_data.max is None and feature_data.std is None and feature_data.mean is None:
    #             continue
    #         if feature_data.feature_name in ["R", "G", "B"]:
    #             continue
    #
    #         row = [
    #             feature_data.feature_name,
    #             self.format_value(feature_data.min),
    #             self.format_value(feature_data.max),
    #             self.format_value(feature_data.mean),
    #             self.format_value(feature_data.std)
    #         ]
    #
    #         # Добавляем строку в таблицу
    #         self.data.append(row)
    #
    #
    #     table = Table(self.data)
    #     table.setStyle(TableStyle([
    #         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #         ('GRID', (0, 0), (-1, -1), 1, colors.black),
    #     ]))
    #     elements.append(table)
    #     elements.append(Spacer(1, 12))
    #
    #     # Добавление описаний и графиков
    #     for i, (feature_data, plot) in enumerate(zip(feature_data_list, plots)):
    #         # description = Paragraph(f"Graphic {i + 1}: {feature_data.feature_name}", styles['Normal'])
    #         # elements.append(description)
    #         elements.append(Spacer(1, 12))
    #
    #         if not feature_data.is_img:
    #             # Save plot to memory
    #             img_buffer = io.BytesIO()
    #             plot.savefig(img_buffer, format='PNG')
    #             img_buffer.seek(0)
    #         else:
    #             img_array = np.uint8(feature_data.data)
    #             pil_img = PILImage.fromarray(img_array)
    #
    #             # Save PIL Image to memory
    #             img_buffer = io.BytesIO()
    #             pil_img.save(img_buffer, format='PNG')
    #             img_buffer.seek(0)
    #
    #         # Insert plot image into PDF
    #         img = Image(img_buffer)
    #         img.drawHeight = 6 * 72  # 6 inches height
    #         img.drawWidth = 6 * 72  # 6 inches width
    #         elements.append(img)
    #         elements.append(Spacer(1, 12))


        # Save PDF
        # doc.build(elements)

    def format_value(self, value):
        return f"{value:.1f}" if value is not None else ''