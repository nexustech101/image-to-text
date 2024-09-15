"""
Description:
This script provides functionality to capture screenshots, extract text from image and PDF files, and save the extracted content to a file or clipboard. It includes hotkey-triggered screenshot capturing and text extraction from various file types (PDF, JPG, PNG, etc.), using libraries like `pytesseract`, `pyautogui`, and `PyMuPDF`.

Usage:

1. Install the required dependencies.
2. Configure Tesseract executable path.
3. Run the script to listen for a hotkey (`Ctrl + Shift + Alt + S`), click and drag to capture a screenshot, and extract text from the captured region or files.

Author:
Charles III

Date:
09-14-2024

"""

from PIL import Image
from pynput import mouse, keyboard
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import utils
from typing import Callable
import pytesseract
import pyperclip
import pyautogui
import threading
import time
import fitz
import os
import logging

# Set up logging
logging.basicConfig(
    filename='text_extraction.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Set the path to the Tesseract executable (cross-platform support)
TESSERACT_PATHS = {
    'win32': r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    'linux': '/usr/bin/tesseract',
    'darwin': '/usr/local/bin/tesseract'
}

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATHS.get(os.name, 'tesseract')

VALID_EXTENSIONS = ["pdf", "jpg", "png", "jpeg", "tiff", "bmp"]

# Global variables for capturing positions and controlling screenshot
start_pos = None
end_pos = None
screenshot_taken = False
macro_triggered = False


class PDFProcessing:
    """Handles text extraction from PDF files using PyMuPDF."""

    @staticmethod
    def extract(pdf_path: str, filter: bool = False) -> str:
        """
        Extracts text from a PDF file directly using PyMuPDF.

        Args:
            pdf_path (str): The path to the PDF file.
            filter (bool): Whether to filter out short lines of text (default: False).

        Returns:
            str: Extracted text from the PDF.
        """
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text += page.get_text()

            if filter:
                lines = text.splitlines()
                filtered_text = "\n".join(
                    line for line in lines if len(line) > 20)
                return filtered_text
            return text
        except Exception as e:
            logging.error(
                f"Failed to extract text from PDF: {pdf_path}. Error: {e}")
            return ""


class ImageProcessing:
    """Handles text extraction from image files using Tesseract."""

    @staticmethod
    def extract(image_path: str) -> str:
        """
        Extracts text from an image file using Tesseract OCR.

        Args:
            image_path (str): The path to the image file.

        Returns:
            str: Extracted text from the image.
        """
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            logging.error(
                f"Failed to extract text from image: {image_path}. Error: {e}")
            return ""


class Extract:
    """Determines the type of file (PDF or image) and extracts text accordingly."""

    @staticmethod
    def extract(file_path: str) -> str:
        """
        Extracts text from the given file based on its type (PDF or image).

        Args:
            file_path (str): The path to the file.

        Returns:
            str: Extracted text from the file.

        Raises:
            ValueError: If the file type is unsupported.
        """
        file_extension = file_path.split('.')[-1].lower()

        if file_extension not in VALID_EXTENSIONS:
            logging.warning(f"Unsupported file type: {file_extension}")
            raise ValueError(f"Unsupported file type: {file_extension}")

        if file_extension == "pdf":
            return PDFProcessing.extract(file_path)
        return ImageProcessing.extract(file_path)


def save_to_txt(text: str, output_filename: str = 'extracted_text.txt') -> None:
    """
    Save the extracted text to a file.

    Args:
        text (str): The extracted text to save.
        output_filename (str): The name of the output file (default: 'extracted_text.txt').
    """
    if text:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(text)

        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.info(f"Text saved to {output_filename} at {formatted_time}")
    else:
        logging.warning("No text to save to file.")


def save_to_clipboard(text: str) -> None:
    """
    Copies the extracted text to the system clipboard.

    Args:
        text (str): The extracted text to copy to the clipboard.
    """
    if text:
        pyperclip.copy(text)
        logging.info("Text copied to clipboard.")
    else:
        logging.warning("No text to copy to clipboard.")


def capture_screenshot(
    left: int, top: int, width: int, height: int, output_filename: str = './assets/screenshot.png'
) -> None:
    """
    Captures a screenshot of the specified bounding box and saves it as an image.

    Args:
        left (int): The x-coordinate of the top-left corner of the screenshot area.
        top (int): The y-coordinate of the top-left corner of the screenshot area.
        width (int): The width of the screenshot area.
        height (int): The height of the screenshot area.
        output_filename (str): The file path where the screenshot will be saved (default: './assets/screenshot.png').
    """
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    try:
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot.save(output_filename)
        logging.info(f"Screenshot saved to {output_filename}")

        text = Extract.extract(output_filename)
        save_to_clipboard(text)
        logging.info(f"Text saved to clipboard")
    except Exception as e:
        logging.error(f"Error capturing screenshot: {e}")


def on_click(x: int, y: int, button, pressed: bool) -> None:
    """
    Handles mouse click events for defining the screenshot region.

    Args:
        x (int): The x-coordinate of the mouse position.
        y (int): The y-coordinate of the mouse position.
        button (pynput.mouse.Button): The mouse button being clicked.
        pressed (bool): Whether the button is pressed or released.
    """
    global start_pos, end_pos, screenshot_taken

    if not macro_triggered:
        return

    if pressed and button == mouse.Button.left:
        start_pos = (x, y)
    elif not pressed and button == mouse.Button.left:
        end_pos = (x, y)

        if start_pos and end_pos:
            left, top = min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1])
            width, height = abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1])

            if not screenshot_taken:
                capture_screenshot(left, top, width, height)
                screenshot_taken = True


def start_mouse_listener() -> None:
    """Starts the mouse listener for capturing screenshot regions."""
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def on_activate() -> None:
    """Activates the screenshot macro trigger."""
    global macro_triggered, screenshot_taken
    macro_triggered = True
    screenshot_taken = False
    logging.info("Macro activated. Click and drag to capture a screenshot.")


def listen_for_hotkey() -> None:
    """Starts the hotkey listener to activate the screenshot macro."""
    with keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+<alt>+s': on_activate,
    }) as h:
        h.join()


def main() -> None:
    """Main function to initiate the hotkey and mouse listeners."""
    hotkey_thread = threading.Thread(target=listen_for_hotkey, daemon=True)
    hotkey_thread.start()

    logging.info("Listening for macro. Press 'Ctrl + Shift + Alt + S' to take a screenshot.")
    start_mouse_listener()


if __name__ == "__main__":
    main()
