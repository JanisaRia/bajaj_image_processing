# Lab Test Extractor - Work in Progress

This project represents my ongoing effort to develop a system for automatically extracting lab test results from medical report images using OCR technology. While the implementation is currently incomplete, I wanted to share my approach and progress.

## Project Goal

The goal is to create a system that can:
- Take medical report images as input
- Extract structured data about lab tests
- Identify if test values are outside of reference ranges
- Present the data in a usable format via API

## Current Implementation Approach

I've attempted to parse lab test data using the following approach:

1. **Image Preprocessing**: 
   - Convert to grayscale
   - Apply adaptive thresholding to handle varying lighting conditions
   - Use denoising techniques to clean up the image

2. **Text Extraction**:
   - Utilize EasyOCR for optical character recognition
   - Extract text from the preprocessed images

3. **Lab Test Pattern Matching**:
   - Apply regular expression patterns to identify lab test entries
   - Current regex patterns look for text structures like:
     ```
     [TEST NAME] [VALUE] [UNIT] [REFERENCE RANGE]
     ```
   - The implementation searches for capital-letter test names followed by numeric values, units, and reference ranges
   - Example pattern: `r'([A-Z][A-Za-z\s\(\)]+)[\s:]+(\d+\.?\d*)\s*([a-zA-Z%/]+)[\s\(]+(\d+\.?\d*[-–]\d+\.?\d*)'`

4. **Out-of-Range Detection**:
   - Compare test values with their reference ranges
   - Flag values that fall outside of the min-max range

5. **API Implementation**:
   - FastAPI service to expose the functionality
   - Allow users to upload images and receive structured data

## Limitations and Known Issues

- The current regex patterns may not catch all lab test formats
- OCR accuracy varies depending on image quality
- Some special characters in test names may cause parsing issues
- Reference range detection doesn't handle qualitative ranges (e.g., "Negative", "Positive")
- Implementation is incomplete and requires further refinement

## Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/lab-test-extractor.git
cd lab-test-extractor

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the API

```bash
python app.py
```

The API will be available at http://localhost:8000

### API Endpoints

- `GET /`: Basic information about the API
- `POST /get-lab-tests`: Upload an image and get extracted lab test data

## Future Work

I plan to improve this project by:
- Refining the pattern matching to handle more lab report formats
- Improving preprocessing for better OCR results
- Adding support for multiple languages
- Creating a more robust reference range comparison system
- Implementing machine learning to enhance extraction accuracy
- Building a proper frontend interface

## Dependencies

- FastAPI: Web framework
- EasyOCR: Optical Character Recognition
- OpenCV: Image processing
- NumPy & Pandas: Data manipulation

## Contributing

This is a work in progress, and I welcome any suggestions or contributions to help improve the implementation.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[MIT](LICENSE)
