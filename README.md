# Python Fun - API Integration Scripts

A collection of Python utility scripts for various API integrations and automation tasks.

## Scripts

- **weather.py** - Get current temperature based on your IP location using WeatherStack API
- **github.py** - Fetch GitHub repository information from a CSV list
- **smartthings.py** - List and manage SmartThings devices
- **swensonRoku.py** - Control Roku devices and launch applications
- **getips.py** - Discover Roku devices on your network using SSDP
- **garmin/garmin.py** - Comprehensive Garmin Connect API client with interactive menu
- **mathfun.py** - Basic mathematical utility functions
- **reuse_requests.py** - Custom requests wrapper class

## Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example environment file and configure it:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

   Required variables in `.env`:
   ```
   github_pat=your_github_personal_access_token
   weather_pat=your_weatherstack_api_key
   weather_url=http://api.weatherstack.com
   zipcode_url=http://ip-api.com/json
   ip_url=https://ipinfo.io
   smart_things_pat=your_smartthings_api_token
   open_ai_pat=your_openai_api_key
   roku_ip=192.168.0.8  # Optional: your Roku device IP
   ```

## Usage

Run individual scripts directly:
```bash
python weather.py
python swensonRoku.py
python garmin/garmin.py
```

## API Keys Required

- **GitHub**: Personal Access Token for repository access
- **WeatherStack**: API key for weather data
- **SmartThings**: API token for device management
- **OpenAI**: API key for AI services
- **Garmin Connect**: Username/password (stored securely in session.json)