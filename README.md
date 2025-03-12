
# Reddit Comment Extractor

A web application that extracts and displays comments from Reddit threads, built with Flask and PRAW (Python Reddit API Wrapper).

## Features

- Extract all comments from any Reddit thread
- Display comments in an easily readable format
- Copy all content to clipboard with a single button click
- Simple web interface for easy interaction

## Project Structure

```
├── main.py              # Main application file with Flask routes and Reddit API integration
├── .replit              # Replit configuration file
├── pyproject.toml       # Python project dependencies
└── poetry.lock          # Lock file for dependencies
```

## Prerequisites

- A Reddit developer account with API credentials
- Environment variables set up for Reddit API authentication

## Environment Variables

This project requires the following environment variables:

- `REDDIT_CLIENT_ID`: Your Reddit API client ID
- `REDDIT_CLIENT_SECRET`: Your Reddit API client secret
- `REDDIT_USER_AGENT`: A user agent string for the Reddit API

You can set these in the Replit Secrets tab.

## How to Use

1. Access the web interface
2. Enter a Reddit thread URL in the provided form
3. Click "Submit" to extract the comments
4. View the thread title, post content, and all comments
5. Use the "Copy to Clipboard" button to copy all content
6. Click "Back to form" to extract comments from another thread

## API Details

The application uses PRAW to interact with the Reddit API. The main functionality includes:

- Extracting thread IDs from Reddit URLs using regular expressions
- Fetching submission data including title, body, and comments
- Caching results for improved performance
- Rendering content with proper formatting for easy reading

## Running the Application

The application runs on port 8080 and is configured for Replit deployment.

```
python main.py
```

## Deployment

The project is configured for deployment on Replit Cloud, with the entry point set to `main.py`.

## Limitations

- The application requires proper Reddit API credentials
- Large threads with many comments may take longer to process
- The in-memory cache will be cleared if the application restarts
