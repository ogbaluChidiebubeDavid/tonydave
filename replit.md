# Tech Savy Tonydave Portfolio

## Overview
A dynamic personal portfolio website for showcasing works including videos, write-ups from X, YouTube, and Medium. Features a content management system for adding and managing portfolio items.

## Project Structure
- `app.py` - Flask backend with API endpoints
- `index.html` - Main landing page
- `project.html` - Dynamic projects showcase with scrollable cards
- `contact.html` - Contact page
- `admin.html` - Admin interface to add/manage portfolio items
- `style.css` - Main stylesheet
- `index.js` - JavaScript for animations
- `media/` - Static images and icons
- `uploads/` - User-uploaded preview images

## Database
PostgreSQL database with `PortfolioItem` model:
- id, title, description, link, category, image_filename, created_at

## API Endpoints
- GET /api/items - Get all portfolio items
- POST /api/items - Create new item (multipart form with image)
- DELETE /api/items/:id - Delete an item

## Running the Project
The site is served using Flask on port 5000.

## Deployment
Configured as autoscale deployment with gunicorn.

## Adding New Works
1. Navigate to /admin
2. Fill in title, description, link (X/YouTube/Medium URL), category
3. Upload a preview image
4. Click "Add Work"
