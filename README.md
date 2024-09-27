# OCR Text Extraction and Annotation

This project utilizes OCR technology to extract text from PDF files, merging text extraction results from different language models, and then annotating the text on images converted from PDF pages.

## Description

The `pytesseract` library is used for text extraction from images. The models used are:

- **ISOCP.traineddata**: A model for the German language
- **ISOCP1.traineddata**: A model for the English language

The extracted texts are merged, and rectangles are drawn around the text on the converted image.

## How to Use

1. **Install the required libraries**

   Ensure that the required libraries are installed using `pip`:

   ```bash
   pip install -r requirements.txt

## Language and Libraries Used


![Python](https://img.shields.io/badge/Language-Python-blue)

### 🚀 Features
- **Language:** Python
- **Dependencies:** `pytesseract`, `PIL`, `PDF2Image`
- **License:** MIT

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ghonim0007/OCR-Text-Extraction-Annotation.git
