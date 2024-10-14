from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)
from reportlab.lib import colors
import io
import numpy as np
from PIL import Image as PILImage
from DatasetProcessor import DatasetInfo
from reportlab.lib.units import inch
from utils.FeatureMetadata import FeatureClasses


class PdfWriter:
    def __init__(self, features_summaries, dataset_info: DatasetInfo, output_filename):
        self.styles = getSampleStyleSheet()
        self.elements = []
        self.features_summaries = features_summaries
        self.feature_data_list = self._set_feature_data_list()
        self.dataset_info = dataset_info
        self.output_filename = output_filename
        self._init_styles()
        self.feature_classes_dict = {feature_class_name: [] for feature_class_name in FeatureClasses}
        self._fill_feature_classes_dict()

    def _fill_feature_classes_dict(self):
        for feature_sum in self.features_summaries:
            print(feature_sum.feature_name, feature_sum.feature_tag)
            self.feature_classes_dict[feature_sum.feature_tag].append(feature_sum)


    def _init_styles(self):
        style = getSampleStyleSheet()
        self.enum_styles = ParagraphStyle("name1", fontName='Times-Roman', fontSize=16, leftIndent=inch)
        self.dataset_info_style = ParagraphStyle("name2", fontName='Times-Roman', fontSize=16)


    def _set_feature_data_list(self, cur_feature_summaries=None):
        if cur_feature_summaries is None:
            cur_feature_summaries = self.features_summaries
        data_list = []
        for feature_sum in cur_feature_summaries:
            if not feature_sum.is_img_feature:
                data_list.extend(feature_sum.features_list)
        return data_list


    def write(self,):
        doc = SimpleDocTemplate(self.output_filename, pagesize=letter)
        self._create_title_block()
        self._create_dataset_info_block()
        self._create_features_list()
        for feature_class in self.feature_classes_dict.keys():
            self._create_table(feature_class)
            self._create_plots_block(feature_class)


        print(self.output_filename)
        doc.build(self.elements)



    def _create_title_block(self):
        title = Paragraph("Images report", self.styles['Title'])
        self.elements.append(title)
        self.elements.append(Spacer(1, 12))

    def _create_dataset_info_block(self):
        description = Paragraph(f"Dataset info", self.styles['Title'])
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))

        description = Paragraph(f"Dataset path : {self.dataset_info.dataset_path}", self.dataset_info_style)
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))

        description = Paragraph(f"Amount of images : {self.dataset_info.images_count}", self.dataset_info_style)
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))

        description = Paragraph(f"Amount of masks : ", self.dataset_info_style)
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))
        for key, val in self.dataset_info.masks_count.items():
            desc = Paragraph(f"{key} : {val}", self.enum_styles)
            self.elements.append(desc)
            self.elements.append(Spacer(1, 12))
        self.elements.append(Spacer(1, 12))

        if self.dataset_info.equal_image_sizes:
            image_sizes_str = str(self.dataset_info.image_sizes).strip('{}')
            description = Paragraph(f"All images  are the same size: {image_sizes_str}", self.dataset_info_style)
        else:
            description = Paragraph(f"The images have different sizes (see the plot)",
                                    self.dataset_info_style)
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))

        if self.dataset_info.equal_mask_sizes:
            mask_sizes_str = str(self.dataset_info.mask_sizes).strip('{}')
            description = Paragraph(f"All masks  are the same size: {mask_sizes_str}",
                                    self.dataset_info_style)
        else:
            description = Paragraph(f"The masks have different sizes (see the plot)",
                                    self.dataset_info_style)
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))
        self.elements.append(Spacer(1, 12))
        self.elements.append(Spacer(1, 12))

    def _create_features_list(self):
        description = Paragraph(f"Dataset feature table", self.styles['Title'])
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))

        num_features = len(self.features_summaries)
        num_images_text = Paragraph(f"Amount of analyzed features: {num_features}", self.dataset_info_style)
        self.elements.append(num_images_text)
        self.elements.append(Spacer(1, 12))

        #
        # for feature_class, features in self.feature_classes_dict.items():
        #     num_images_text = Paragraph(f"Amount of {feature_class} features: {len(features)}", self.dataset_info_style)
        #     self.elements.append(num_images_text)
        #     self.elements.append(Spacer(1, 12))


        for feature_class, features in self.feature_classes_dict.items():
            num_images_text = Paragraph(f"{feature_class}:", self.dataset_info_style)
            self.elements.append(num_images_text)
            self.elements.append(Spacer(1, 12))
            for feature_summary in features:
                feature_name = feature_summary.feature_name
                feature_paragraph = Paragraph(f"- {feature_name}", self.enum_styles)
                self.elements.append(feature_paragraph)
                self.elements.append(Spacer(1, 12))


        self.elements.append(PageBreak())


    def _create_table(self, feature_class):
        long_first_column = False

        if feature_class == "Labels":
            return

        table_title = Paragraph(f"Table of {feature_class} features", self.styles['Title'])
        self.elements.append(table_title)
        self.elements.append(Spacer(1, 12))

        # Create table
        head = ['Feature name', 'Min', 'Max', 'Mean', 'Std']
        self.data = []

        for feature_sumary in self.feature_classes_dict[feature_class]:
            for feature_data in feature_sumary.features_list:

                if feature_data.min is None and feature_data.max is None and feature_data.std is None and feature_data.mean is None:
                    continue

                long_first_column = True if (not long_first_column and len(f"{feature_data.feature_name} {feature_data.class_name}") > 33) else False

                if feature_class == "General":
                    row = [
                        feature_data.feature_name if feature_class == "General" else f"{feature_data.feature_name} {feature_data.class_name}",
                        self.format_value(feature_data.min),
                        self.format_value(feature_data.max),
                        self.format_value(feature_data.mean),
                        self.format_value(feature_data.std)
                    ]
                    self.data.append(row)

                else:
                    feature_name = feature_data.feature_name if feature_class == "General" else f"{feature_data.feature_name} {feature_data.class_name}"
                    values = [
                        self.format_value(feature_data.min),
                        self.format_value(feature_data.max),
                        self.format_value(feature_data.mean),
                        self.format_value(feature_data.std)
                    ]

                    # Combine feature name and class-specific values into one row
                    row = [feature_name] + values
                    self.data.append(row)

        if len(self.data) == 0:
            return

        # Format table
        self.data.insert(0, head)

        # Calculate page and margin widths
        page_width = letter[0]
        left_margin = inch  # левый отступ
        right_margin = inch  # правый отступ
        usable_width = page_width - (left_margin + right_margin)

        # Ширина колонок
        num_columns = len(head)

        first_col_width = usable_width * 0.4  if not long_first_column else usable_width * 0.45
        print(long_first_column)
        other_col_width = (usable_width - first_col_width) / (num_columns - 1)

        col_widths = [first_col_width] + [other_col_width for _ in range(num_columns - 1)]

        # Создание таблицы
        table = Table(self.data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # Установите размер шрифта
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 12))
        self.elements.append(PageBreak())

    def _fill_plots_section_info(self, feature_class):
        feature_plots_dict = {}
        self.elements.append(Spacer(1, 12))
        for i, feature_sum in enumerate(self.feature_classes_dict[feature_class]):

            if feature_sum.feature_name == "Aspect Ratio" and self.dataset_info.equal_image_sizes:
                continue

            if feature_sum.description is  None:
                description = Paragraph(f"Graphic {i + 1}: {feature_sum.feature_name}", self.styles['Heading2'])
            else:
                description1 = Paragraph(f"Graphic {i + 1}: {feature_sum.feature_name}", self.styles['Heading2'])
                description2 = Paragraph(feature_sum.description, self.styles['Heading3'])
                description = (description1, description2)
            feature_plots_dict[description] = []

            if feature_sum.is_img_feature:
                for feature_data in feature_sum.features_list:
                    # for name, feature_img in feature_data.data.items():
                    name = feature_data.class_name
                    feature_img = feature_data.data
                    img_array = np.uint8(feature_img)  #
                    pil_img = PILImage.fromarray(img_array)

                    img_buffer = io.BytesIO()
                    pil_img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)

                    img = Image(img_buffer)
                    feature_plots_dict[description].append((img, name))
                    del (img_buffer)

            else:
                for plot in feature_sum.plots:
                    img_buffer = io.BytesIO()
                    plot.savefig(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    img = Image(img_buffer)
                    feature_plots_dict[description].append((img, ""))
                    del (img_buffer)
        return feature_plots_dict

    def _change_im_size(self, img):
        current_height = img.drawHeight
        current_width = img.drawWidth

        # Вычисляем текущее соотношение сторон
        aspect_ratio = current_width / current_height

        # Задаем новые размеры, уменьшая текущие на 20%
        new_height = current_height * 0.4
        new_width = current_width * 0.4

        # Проверяем, какой из размеров больше, чтобы сохранить соотношение сторон
        if new_width / aspect_ratio <= new_height:
            new_height = new_width / aspect_ratio
        else:
            new_width = new_height * aspect_ratio

        # Применяем новые размеры
        img.drawHeight = new_height
        img.drawWidth = new_width
        return img.drawHeight, img.drawWidth

    def _create_plots_block(self, feature_class):

        feature_plots_dict = self._fill_plots_section_info(feature_class)

        description = Paragraph(f"{feature_class} graphics", self.styles['Heading1'])
        self.elements.append(description)
        self.elements.append(Spacer(1, 12))

        for desc, images_names in feature_plots_dict.items():
            if isinstance(desc, tuple):
                self.elements.append(desc[0])
                self.elements.append(desc[1])
            else:
                self.elements.append(desc)
            for img, name in images_names:
                img.drawHeight, img.drawWidth = self._change_im_size(img)
                name = Paragraph(name, self.styles['Heading3'])
                self.elements.append(name)
                self.elements.append(Spacer(1, 12))
                self.elements.append(img)
                self.elements.append(Spacer(1, 12))
                self.elements.append(PageBreak())





    def format_value(self, value):
        if value is None:
            return ''
        elif value == 0.0:
            return '0'
        elif abs(value) < 1e-3:
            return f"{value:.1e}"
        else:
            return f"{value:.3f}"