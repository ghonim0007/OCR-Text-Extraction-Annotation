import os
import re
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageOps
from pytesseract import pytesseract
import fitz

def extract_text_with_boxes(image: Image, lang: str):
    custom_config = r'--oem 1 --psm 3'
    gray_image = ImageOps.grayscale(image)
    enhanced_image = ImageOps.autocontrast(gray_image)
    data = pytesseract.image_to_data(enhanced_image, output_type=pytesseract.Output.DICT, config=custom_config, lang=lang)
    text_with_boxes = []
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 0:  #
            text_with_boxes.append({
                'text': data['text'][i],
                'left': data['left'][i],
                'top': data['top'][i],
                'width': data['width'][i],
                'height': data['height'][i]
            })
    return text_with_boxes

def merge_text_boxes(boxes_de, boxes_en):
    merged_boxes = []
    all_boxes = boxes_de + boxes_en
    seen = set()
    for item in all_boxes:
        key = (item['left'], item['top'], item['width'], item['height'])
        if key not in seen:
            seen.add(key)
            merged_boxes.append(item)
    return merged_boxes

def annotate_image(image, text_boxes):
    draw = ImageDraw.Draw(image)
    for item in text_boxes:
        if item['text'].strip():  
            x0 = item['left']
            y0 = item['top']
            x1 = x0 + item['width']
            y1 = y0 + item['height']
            draw.rectangle([(x0, y0), (x1, y1)], outline="red", width=2)

def save_boxes_to_file(text_boxes, output_path):
    with open(output_path, 'w') as file:
        for item in text_boxes:
            if item['text'].strip():  
                file.write(f"{item['text']} {item['left']} {item['top']} {item['left'] + item['width']} {item['top'] + item['height']} 0\n")


def extract_text_and_annotate_pdfs(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(input_folder, filename)
            try:
                doc = fitz.open(file_path)  
            except Exception as e:
                print(f"Failed to open {file_path}: {e}")
                continue

            for page_index in range(len(doc)):
                print('> Extracting page', page_index + 1, 'from pdf:', filename)
                page = doc.load_page(page_index)
                zoom = 2.5
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                print('> Doing OCR with German model...')
                text_with_boxes_de = extract_text_with_boxes(img, lang='ISOCP')

                print('> Doing OCR with English model...')
                text_with_boxes_en = extract_text_with_boxes(img, lang='ISOCP1')

                print('> Merging results...')
                text_with_boxes = merge_text_boxes(text_with_boxes_de, text_with_boxes_en)

                box_file_path = os.path.join(output_folder, os.path.splitext(filename)[0] + f"_page_{page_index + 1}.box")
                try:
                    save_boxes_to_file(text_with_boxes, box_file_path)
                    print(f"Box file saved to {box_file_path}")
                except Exception as e:
                    print(f"Failed to save box file {box_file_path}: {e}")

                print('> Annotating image...')
                annotate_image(img, text_with_boxes)

                annotated_image_path = os.path.join(output_folder, os.path.splitext(filename)[0] + f"_annotated_page_{page_index + 1}.png")
                try:
                    img.save(annotated_image_path)
                    print(f"Annotated image saved to {annotated_image_path}")
                except Exception as e:
                    print(f"Failed to save image file {annotated_image_path}: {e}")

def select_folder_and_extract():
    input_folder = filedialog.askdirectory(title="Select input folder")
    if input_folder:
        output_folder = filedialog.askdirectory(title="Select output folder")  
            extract_text_and_annotate_pdfs(input_folder, output_folder)

if __name__ == '__main__':
    os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    select_folder_and_extract()
