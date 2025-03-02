
# Bio Page Creator

A visually appealing web app that allows users to create and share customizable bio pages.

## Features

- Create personalized bio pages with custom URLs
- Multiple theme options (Default, Dark, Light, Colorful, Minimal)
- Social media links integration
- Profile image upload
- Custom CSS for advanced customization
- RESTful API for programmatic access

## Getting Started

1. Clone this repository
2. Install dependencies with `pip install -r requirements.txt`
3. Run the app with `python main.py`
4. Visit `http://localhost:8080` in your browser

## API Documentation

The app provides a comprehensive RESTful API for programmatic access to create, read, update, and delete bio pages.

### API Endpoints

#### List All Bios
- **URL:** `/api/bios`
- **Method:** `GET`
- **Response:**
```json
{
  "success": true,
  "count": 2,
  "bios": ["john_doe", "jane_smith"]
}
```

#### Get Bio Details
- **URL:** `/api/bio/{bio_name}`
- **Method:** `GET`
- **Response:**
```json
{
  "success": true,
  "bio_name": "john_doe",
  "bio": {
    "name": "John Doe",
    "tagline": "Web Developer",
    "bio": "Hi, I'm John!",
    "profile_image": "/uploads/1234abcd.jpg",
    "theme": "dark",
    "social_links": {
      "twitter": "johndoe",
      "instagram": "johndoe",
      "linkedin": "johndoe",
      "github": "johndoe"
    },
    "custom_css": ""
  }
}
```

#### Create New Bio
- **URL:** `/api/bio/{bio_name}`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
```json
{
  "name": "John Doe",
  "tagline": "Web Developer",
  "bio": "Hi, I'm John!",
  "profile_image": "/uploads/1234abcd.jpg",
  "theme": "dark",
  "social_links": {
    "twitter": "johndoe",
    "instagram": "johndoe",
    "linkedin": "johndoe",
    "github": "johndoe"
  },
  "custom_css": ""
}
```
- **Response:**
```json
{
  "success": true,
  "message": "Bio created successfully",
  "bio_name": "john_doe"
}
```

#### Update Existing Bio
- **URL:** `/api/bio/{bio_name}`
- **Method:** `PUT`
- **Headers:** `Content-Type: application/json`
- **Request Body:** (only fields to update are required)
```json
{
  "tagline": "Full Stack Developer",
  "bio": "Updated bio information"
}
```
- **Response:**
```json
{
  "success": true,
  "message": "Bio updated successfully",
  "bio_name": "john_doe"
}
```

#### Delete Bio
- **URL:** `/api/bio/{bio_name}`
- **Method:** `DELETE`
- **Response:**
```json
{
  "success": true,
  "message": "Bio deleted successfully",
  "bio_name": "john_doe"
}
```

#### Get Available Themes
- **URL:** `/api/themes`
- **Method:** `GET`
- **Response:**
```json
{
  "success": true,
  "count": 5,
  "themes": ["default", "dark", "light", "colorful", "minimal"]
}
```

### Example Usage with cURL

#### Get all bios
```bash
curl -X GET http://your-url/api/bios
```

#### Create a new bio
```bash
curl -X POST http://your-url/api/bio/john_doe \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","bio":"Hello World!","tagline":"Developer"}'
```

#### Update a bio
```bash
curl -X PUT http://your-url/api/bio/john_doe \
  -H "Content-Type: application/json" \
  -d '{"tagline":"Full Stack Developer"}'
```

#### Delete a bio
```bash
curl -X DELETE http://your-url/api/bio/john_doe
```

## Deployment

This app is designed to be easily deployed on your hosting platform of choice.

## Requirements Fulfilled

- **GET Requests (4)**: `/api/bios`, `/api/bio/{bio_name}`, `/api/themes`, and the web interface routes
- **POST Requests (1+)**: `/api/bio/{bio_name}` for creating bios, and the web interface form submissions
- **PUT Request (1)**: `/api/bio/{bio_name}` for updating bios
- **DELETE Request (1)**: `/api/bio/{bio_name}` for deleting bios
- **Detailed API Documentation**: Both in-app at `/api/docs` and in this README
