# Document Scanner

A Python-based document scanner application that automatically detects document edges, applies perspective transformation, and enhances the document for better readability.

## Project Overview

This document scanner uses computer vision techniques to:

- Detect document edges in an image
- Apply perspective transformation to obtain a top-down view
- Enhance document contrast and readability
- Process and save the scanned result

## Technologies Used

- **Python 3.11**
- **OpenCV** (Computer Vision library)
- **NumPy** (Numerical computing)
- **Pillow** (Image processing)
- **imutils** (Image processing utilities)
- **scikit-image** (Image processing algorithms)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TrishamBP/document-scanner.git
   cd document-scanner
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place the document image you want to scan in the project directory or specify the path when running the program.
2. Run the main script:
   ```bash
   python scan.py --image path/to/document.jpg
   ```
3. **Optional arguments:**
   ```bash
   python scan.py --image path/to/document.jpg --output scanned_result.jpg
   ```
4. The program will:
   - Detect document edges
   - Apply perspective transformation
   - Enhance the document
   - Save the processed image

## Implementation Details

The document scanner follows these key steps:

1. **Edge Detection:** Using Canny edge detection to identify document boundaries.
2. **Contour Detection:** Finding the document contour within the image.
3. **Perspective Transform:** Warping the image to get a top-down view of the document.
4. **Enhancement:** Applying adaptive thresholding and other techniques to improve readability.

## Project Structure

```
📂 Document-Scanner
│-- 📂 examples/ (Sample images before and after scanning)
│-- 📜 scan.py (Main script for document scanning)
│-- 📜 requirements.txt (Dependencies)
│-- 📜 README.md (Project documentation)
```

## Examples

| Original Image                     | Scanned Result                   |
| ---------------------------------- | -------------------------------- |
| ![Original] ![image](https://github.com/user-attachments/assets/a482780d-487c-409b-8f21-b346f99bc0e0)| ![Scanned]![image](https://github.com/user-attachments/assets/4315b4d6-1328-4b04-9146-8f9965e689ad)

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## Future Improvements

- Add **OCR (Optical Character Recognition)** functionality
- Implement **batch processing** for multiple documents
- Create a **web interface** for easier usage
- Add **mobile support** through a REST API

## Acknowledgements

- **Adrian Rosebrock's PyImageSearch tutorials**
- **OpenCV documentation and community**
- **All open-source libraries used in this project**
