# Fun Life Backend

A powerful backend system for managing fashion content, video integration, and scholarship search functionality.

## Features

- Fashion Content Management
  - Create, update, and delete fashion posts
  - Search and filter fashion content
  - Tag-based categorization

- Video Integration
  - Upload and manage video content
  - Google Cloud Storage integration for video storage
  - Video metadata management and search

- Scholarship Search Engine
  - Advanced scholarship search with multiple filters
  - Deadline tracking
  - Amount-based filtering
  - Tag-based categorization

## Tech Stack

- Python 3.8+
- Flask
- MongoDB
- Elasticsearch
- Google Cloud Storage for video storage

## Prerequisites

1. MongoDB installed and running
2. Elasticsearch installed and running
3. Google Cloud Platform account with Cloud Storage enabled
4. Python 3.8 or higher

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Cloud:
   - Create a new project in Google Cloud Console
   - Enable Cloud Storage API
   - Create a service account and download the JSON credentials file
   - Create a Cloud Storage bucket

4. Create a .env file with the following variables:
```
MONGO_URI=mongodb://localhost:27017/fashion_platform
ELASTICSEARCH_URL=http://localhost:9200
GCP_PROJECT_ID=your_project_id
GCP_BUCKET_NAME=your_bucket_name
GCP_CREDENTIALS_FILE=path/to/your/credentials.json
JWT_SECRET_KEY=your_jwt_secret
```

5. Start the server:
```bash
python app.py
```

## API Endpoints

### Fashion

- `POST /api/v1/fashion/` - Create a new fashion post
- `GET /api/v1/fashion/` - List fashion posts
- `GET /api/v1/fashion/<post_id>` - Get a specific fashion post
- `PUT /api/v1/fashion/<post_id>` - Update a fashion post
- `DELETE /api/v1/fashion/<post_id>` - Delete a fashion post

### Videos

- `POST /api/v1/videos/upload` - Upload a new video
- `GET /api/v1/videos/` - List videos
- `GET /api/v1/videos/<video_id>` - Get a specific video
- `PUT /api/v1/videos/<video_id>` - Update video metadata
- `DELETE /api/v1/videos/<video_id>` - Delete a video

### Scholarships

- `POST /api/v1/scholarships/` - Create a new scholarship
- `GET /api/v1/scholarships/search` - Search scholarships
- `GET /api/v1/scholarships/<scholarship_id>` - Get a specific scholarship
- `PUT /api/v1/scholarships/<scholarship_id>` - Update a scholarship
- `DELETE /api/v1/scholarships/<scholarship_id>` - Delete a scholarship

## Development

The project follows a modular structure:

- `routes/` - API route definitions
- `services/` - Business logic implementation
- `utils/` - Utility functions and validators
- `config/` - Configuration management

## License

MIT License
