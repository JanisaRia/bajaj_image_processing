# Lab Test Extractor API

A FastAPI service that extracts lab test data from medical report images.

## Overview

This API allows you to upload lab report images and extract structured data including:
- Test names
- Test values
- Reference ranges
- Units
- Whether tests are out of range

## API Endpoints

- `GET /` - Returns basic information about the API
- `POST /get-lab-tests` - Accepts an image file and returns extracted lab test data

## Example Response

```json
{
  "is_success": true,
  "data": [
    {
      "test_name": "HB ESTIMATION",
      "test_value": "9.4",
      "bio_reference_range": "12.0-15.0",
      "test_unit": "g/dL",
      "lab_test_out_of_range": false
    },
    {
      "test_name": "PCV (PACKED CELL VOLUME)",
      "test_value": "48.7",
      "bio_reference_range": "36.0-46.0",
      "test_unit": "%",
      "lab_test_out_of_range": true
    }
  ]
}
```

## Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the app:
   ```
   uvicorn app:app --reload
   ```

3. Open http://localhost:8000/docs in your browser to see the API documentation.

## Deployment

This API is deployed at: [YOUR-DEPLOYMENT-URL]
