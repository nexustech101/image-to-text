# Screenshot Text Extractor

## Description

Screenshot Text Extractor is a versatile Python script designed to streamline the process of capturing screenshots and extracting text from various file types. This tool combines the power of optical character recognition (OCR) with intuitive user controls, making it an invaluable asset for data entry, research, and document processing tasks.

Key capabilities include:
- Hotkey-activated screenshot capture
- Text extraction from screenshots, PDFs, and various image formats
- Seamless integration with system clipboard for quick text access
- Cross-platform compatibility
- Detailed logging for troubleshooting and performance tracking

By leveraging libraries such as `pytesseract`, `pyautogui`, and `PyMuPDF`, this script offers a robust solution for automating text extraction tasks across multiple file types and platforms.

## Features

- **Hotkey-Triggered Screenshot Capture**: 
  - Activate with `Ctrl + Shift + Alt + S`
  - Click and drag to select the desired screen area

- **Comprehensive Text Extraction**:
  - Screenshots: Instantly process newly captured images
  - PDF Files: Extract text from single or multi-page documents
  - Image Files: Support for JPG, PNG, JPEG, TIFF, and BMP formats

- **Flexible Output Options**:
  - Save extracted text to a file for permanent storage
  - Copy text directly to system clipboard for immediate use

- **Cross-Platform Compatibility**:
  - Tested and supported on Windows, Linux, and macOS
  - Configurable paths for Tesseract OCR across different operating systems

- **Robust Logging System**:
  - Detailed logs of operations, warnings, and errors
  - Facilitates easy troubleshooting and performance monitoring

- **Modular Design**:
  - Separate classes for PDF and image processing
  - Easily extendable for additional file types or processing methods

## Requirements

- **Python**: Version 3.6 or higher
- **Tesseract OCR**: Open-source OCR engine
- **Python Libraries**: 
  - pillow: Image processing
  - pynput: Keyboard and mouse control
  - reportlab: PDF generation
  - pytesseract: Python wrapper for Tesseract OCR
  - pyperclip: Clipboard operations
  - pyautogui: GUI automation
  - PyMuPDF: PDF processing

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/screenshot-text-extractor.git
   cd screenshot-text-extractor
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Required Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**:
   - Windows: 
     1. Download the installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
     2. Run the installer and note the installation path
   - macOS:
     ```bash
     brew install tesseract
     ```
   - Linux:
     ```bash
     sudo apt-get update
     sudo apt-get install tesseract-ocr
     ```

5. **Configure Tesseract Path**:
   Open `screenshot_text_extractor.py` and modify the `TESSERACT_PATHS` dictionary if necessary:
   ```python
   TESSERACT_PATHS = {
       'win32': r'C:\Program Files\Tesseract-OCR\tesseract.exe',
       'linux': '/usr/bin/tesseract',
       'darwin': '/usr/local/bin/tesseract'
   }
   ```

## Usage

1. **Start the Script**:
   ```bash
   python screenshot_text_extractor.py
   ```

2. **Capture a Screenshot**:
   - Press `Ctrl + Shift + Alt + S` to activate screenshot mode
   - Click and drag to select the desired area
   - Release to capture

3. **Automatic Processing**:
   The script will:
   - Save the screenshot as `./assets/screenshot.png`
   - Extract text from the image
   - Copy the extracted text to your clipboard
   - Log the operation in `text_extraction.log`

4. **Extracting Text from Existing Files**:
   Modify the script to use the appropriate extraction method:

   ```python
   # For PDF files
   pdf_text = PDFProcessing.extract("path/to/your/file.pdf")
   print(pdf_text)

   # For image files
   image_text = ImageProcessing.extract("path/to/your/image.jpg")
   print(image_text)
   ```

5. **Customizing Text Extraction**:
   - PDF Extraction: Use the `filter` parameter to remove short lines
     ```python
     filtered_text = PDFProcessing.extract("path/to/your/file.pdf", filter=True)
     ```
   - Image Preprocessing: Modify the `ImageProcessing.extract` method to include image preprocessing steps for improved OCR accuracy

## Logging

- **Log File**: `text_extraction.log` in the script's directory
- **Log Format**: `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`
- **Logged Information**:
  - Script start and stop times
  - Screenshot captures
  - Text extraction operations
  - Errors and exceptions
  - Configuration changes

## Customization

- **Hotkey**: Modify the `listen_for_hotkey` function to change the activation key combination
- **Output Directory**: Change the `output_filename` parameter in `capture_screenshot` to alter the screenshot save location
- **OCR Language**: Adjust the `lang` parameter in `pytesseract.image_to_string` for non-English text extraction

## Troubleshooting

- **OCR Accuracy Issues**: 
  - Ensure proper Tesseract installation and configuration
  - Consider image preprocessing (e.g., resizing, contrast adjustment) for better results
- **Hotkey Not Working**: 
  - Check for conflicts with other applications
  - Ensure proper permissions for global hotkey registration

## Author

Charles III

## Date

September 14, 2024

## License

[Specify your chosen license here, e.g., MIT License, GNU GPL v3, etc.]

## Contributing

We welcome contributions to improve Screenshot Text Extractor! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

Please ensure your code adheres to our coding standards and includes appropriate tests.

## Support

For support, please:

1. Check the [GitHub Issues](https://github.com/yourusername/screenshot-text-extractor/issues) for existing problems or solutions
2. Open a new issue if you encounter a bug or have a feature request
3. For urgent matters, contact the maintainer directly at [your-email@example.com]

We appreciate your feedback and contributions to making Screenshot Text Extractor better!