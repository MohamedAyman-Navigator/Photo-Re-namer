# Photo Renamer

A powerful tool to automatically rename photos by detecting numeric codes embedded in the images using OCR (Optical Character Recognition).

This project provides two ways to use the tool:
1.  **Command Line Interface (CLI)**: For batch processing folders.
2.  **Web Application**: A user-friendly local web interface with drag-and-drop support.

## Features

-   **Automatic Text Detection**: Uses `EasyOCR` to read text from images.
-   **Smart Filtering**: Specifically looks for numeric codes (5+ digits) at the top of the image.
-   **Batch Processing**: Rename hundreds of photos in seconds.
-   **Local Web App**: Modern, dark-mode interface for easy uploading and renaming.
-   **Privacy Focused**: All processing happens locally on your machine. No data is uploaded to the cloud.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/MohamedAyman-Navigator/Photo-Re-namer.git
    cd Photo-Re-namer
    ```

2.  **Install Dependencies**:
    You need Python installed. Then run:
    ```bash
    pip install easyocr opencv-python-headless flask
    ```
    *Note: This will also install PyTorch, which is required for EasyOCR.*

## Usage

### Option 1: Web Application (Recommended)

1.  Run the Flask app:
    ```bash
    python3 app.py
    ```
2.  Open your browser and go to: `http://127.0.0.1:5000`
3.  Drag and drop your images into the upload area.
4.  Click **Process & Rename**.
5.  Download your renamed files individually or as a ZIP archive.

### Option 2: Command Line Script

1.  Place your photos in the same directory as the script (or modify the script to point to your folder).
2.  Run the script:
    ```bash
    python3 rename_photos.py
    ```
3.  **Dry Run** (Preview changes without renaming):
    ```bash
    python3 rename_photos.py --dry-run
    ```

### Option 3: Windows Executable

1.  Double-click `PhotoRenamer.exe` (located in the `dist` folder after building).
2.  The application will start and **automatically open your default web browser**.
3.  Use the web interface to upload and rename your photos.

## How it Works

1.  The tool reads the image using `OpenCV`.
2.  It crops the top 30% of the image (where codes are usually located).
3.  `EasyOCR` scans the cropped area for text.
4.  The script filters the results to find a numeric string with 5 or more digits.
5.  The file is renamed to `[CODE].jpg` (e.g., `5033742.jpg`).

## Dependencies

-   [EasyOCR](https://github.com/JaidedAI/EasyOCR)
-   [Flask](https://flask.palletsprojects.com/)
-   [OpenCV](https://opencv.org/)

## Building the Executable

To create a standalone `.exe` file for Windows:

1.  **On Windows**, open the project folder.
2.  Double-click `build_windows.bat`.
3.  Wait for the build to complete (it may take a few minutes).
4.  The executable will be in the `dist` folder.

