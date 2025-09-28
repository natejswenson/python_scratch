# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a collection of Python utility scripts for various API integrations and automation tasks. Each script is designed to be standalone and demonstrates different API interactions.

## Environment Setup

### Virtual Environment
The project uses a Python virtual environment located in `.venv/`. To activate:
```bash
source .venv/bin/activate
```

### Environment Variables
All scripts rely on API keys and configuration stored in `.env` file with the following variables:
- `github_pat` - GitHub Personal Access Token
- `weather_pat` - WeatherStack API key
- `weather_url` - WeatherStack API URL (http://api.weatherstack.com)
- `zipcode_url` - IP geolocation service URL (http://ip-api.com/json)
- `ip_url` - IP information service URL (https://ipinfo.io)
- `smart_things_pat` - SmartThings API token
- `open_ai_pat` - OpenAI API key

The `decouple` library is used throughout to load environment variables.

## Script Architecture

### Core Utilities
- **reuse_requests.py** - Custom requests wrapper class with session management and base URL handling
- **mathfun.py** - Basic mathematical functions (add, subtract)

### API Integration Scripts
- **weather.py** - Weather data retrieval using WeatherStack API with IP-based location detection
- **github.py** - GitHub repository information fetching using GitHub API
- **smartthings.py** - SmartThings device management using async/await pattern
- **swensonRoku.py** - Roku device control and app launching
- **getips.py** - Network discovery for Roku devices using SSDP multicast
- **garmin/garmin.py** - Comprehensive Garmin Connect API client with session management

### Key Patterns
- Most scripts use the `requests` library for HTTP calls
- Environment variables are consistently loaded using `decouple.config()`
- Error handling includes status code checking and exception handling
- The Garmin script demonstrates session persistence using JSON files
- SmartThings uses async/await for asynchronous operations

## Running Scripts

Individual scripts can be run directly:
```bash
python weather.py
python swensonRoku.py
python garmin/garmin.py
```

The Garmin script includes an interactive menu system for testing different API endpoints.

## Dependencies

All dependencies are managed via `requirements.txt`. Install with:
```bash
pip install -r requirements.txt
```

Key libraries:
- `requests` - HTTP client
- `python-decouple` - Environment variable management
- `roku` - Roku device control
- `pysmartthings` - SmartThings API
- `garminconnect` - Garmin Connect API
- `aiohttp` - Async HTTP client (SmartThings)
- `PyGithub` - GitHub API client

## Project Structure

```
python_fun/
├── utils/           # Shared utility modules
│   ├── __init__.py
│   ├── reuse_requests.py  # Custom requests wrapper
│   └── logger.py    # Logging utilities
├── garmin/         # Garmin Connect scripts
├── github/         # GitHub-related scripts
├── .env.example    # Environment template
└── requirements.txt # Dependencies
```

## Development Notes

- All secrets and API keys are externalized to `.env` file
- Use `.env.example` as a template for configuration
- Shared utilities are organized in the `utils/` directory
- Scripts include proper error handling and type hints where applicable
- No formal testing framework is configured (consider adding pytest for future development)