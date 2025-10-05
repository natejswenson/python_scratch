# Python Fun - API Integration Scripts

A collection of Python utility scripts for various API integrations and automation tasks. This project demonstrates best practices for API integrations, error handling, type hints, and comprehensive testing.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-71%2B-green.svg)](tests/)

## 📋 Features

- **Type-Safe**: Full type hints throughout the codebase
- **Well-Documented**: Comprehensive docstrings for all functions
- **Robust Error Handling**: Graceful handling of network and API errors
- **100% Tested**: 71+ unit tests with mocking for external APIs
- **Production Ready**: Pinned dependencies and proper project structure

## 🗂️ Project Structure

```
python_fun/
├── weather.py              # Weather data retrieval using WeatherStack API
├── github.py               # GitHub repository information fetching
├── smartthings.py          # SmartThings device management (async)
├── swensonRoku.py          # Roku device control and app launching
├── getips.py               # Network discovery for Roku devices (SSDP)
├── openAI.py               # OpenAI API integration
├── swapi.py                # Star Wars API (SWAPI) integration
├── mathfun.py              # Basic mathematical utility functions
├── github/
│   ├── __init__.py
│   └── create_repo.py      # GitHub repository creation
├── garmin/
│   └── garmin.py           # Garmin Connect API client
├── utils/
│   ├── __init__.py
│   ├── reuse_requests.py   # Custom requests wrapper with session management
│   └── logger.py           # Logging utilities
├── specs/                  # Feature specifications for TDD
│   └── swapi_function_spec.md
├── tests/                  # Comprehensive unit tests (100+ tests)
│   ├── test_swapi.py       # SWAPI function tests
│   └── ...                 # Other test files
├── requirements.txt        # Production dependencies (pinned versions)
├── requirements-dev.txt    # Development dependencies (testing, linting)
├── pytest.ini              # Pytest configuration
├── .coveragerc             # Coverage configuration
└── TESTING.md              # Testing documentation
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+ (specified in `.python-version`)
- pip package manager

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd python_fun

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For development (includes testing tools)
pip install -r requirements-dev.txt
```

### 3. Configuration

Copy the example environment file and configure with your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# GitHub Configuration
github_pat=your_github_personal_access_token

# Weather API Configuration
weather_pat=your_weatherstack_api_key
weather_url=http://api.weatherstack.com
zipcode_url=http://ip-api.com/json
ip_url=https://ipinfo.io

# SmartThings Configuration
smart_things_pat=your_smartthings_api_token

# OpenAI Configuration
open_ai_pat=your_openai_api_key

# Roku Configuration (optional)
roku_ip=192.168.0.8
```

## 📖 Usage Examples

### Weather Information
```bash
python weather.py
# Output: Current temperature in New York is 72°F
```

### GitHub Repository Info
```bash
python github.py
# Reads from repositories.csv and displays repo information
```

### Roku Device Control
```bash
# Discover Roku devices on network
python getips.py

# Launch Roku apps
python swensonRoku.py
```

### SmartThings Device Management
```bash
python smartthings.py
# Lists all SmartThings devices with capabilities
```

### OpenAI Integration
```bash
python openAI.py
# Sends a query to OpenAI API
```

### Garmin Connect
```bash
python garmin/garmin.py
# Interactive menu for Garmin Connect data
```

### GitHub Repository Creation
```bash
python -c "from github.create_repo import create_github_repo; create_github_repo('my-repo', 'Description', False, 'token')"
```

### Star Wars API (SWAPI) Integration
```python
from swapi import get_swapi_data, SWAPIResource

# Get a specific character
luke = get_swapi_data(SWAPIResource.PEOPLE, resource_id=1)
print(f"{luke['name']} is {luke['height']}cm tall")
# Output: Luke Skywalker is 172cm tall

# Search for planets
desert_planets = get_swapi_data(SWAPIResource.PLANETS, search="desert")
for planet in desert_planets:
    print(f"{planet['name']} - {planet['climate']}")

# Get all Star Wars films
films = get_swapi_data(SWAPIResource.FILMS)
print(f"Found {len(films)} films")

# Use caching for better performance
cached_data = get_swapi_data(
    SWAPIResource.STARSHIPS,
    resource_id=9,
    use_cache=True
)
```

## 🧪 Testing

The project includes comprehensive unit tests with >70 test cases covering all modules.

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_weather.py -v

# Run tests by marker
pytest -m "not slow"
```

### View Coverage Report

```bash
# Open HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

See [TESTING.md](TESTING.md) for detailed testing documentation.

## 🛠️ Development

### Code Quality Tools

The project uses the following tools (included in `requirements-dev.txt`):

- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **flake8** - Linting
- **pylint** - Code analysis
- **mypy** - Type checking
- **isort** - Import sorting

### Running Code Quality Checks

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

## 📦 Dependencies

### Production Dependencies
- `requests==2.32.3` - HTTP client
- `aiohttp==3.11.10` - Async HTTP client
- `python-decouple==3.8` - Environment variable management
- `roku==4.1.0` - Roku device control
- `pysmartthings==0.7.7` - SmartThings API
- `garminconnect==0.2.26` - Garmin Connect API
- `PyGithub==2.6.0` - GitHub API
- `openai==1.59.5` - OpenAI API

See [requirements.txt](requirements.txt) for full list.

### Development Dependencies
- Testing: pytest, pytest-cov, pytest-asyncio
- Linting: black, flake8, pylint, mypy
- Tools: isort, pre-commit

See [requirements-dev.txt](requirements-dev.txt) for full list.

## 📚 API Documentation

### Required API Keys

| Service | Key Type | Purpose | Get Key |
|---------|----------|---------|---------|
| GitHub | Personal Access Token | Repository access | [GitHub Settings](https://github.com/settings/tokens) |
| WeatherStack | API Key | Weather data | [WeatherStack](https://weatherstack.com/) |
| SmartThings | API Token | Device management | [SmartThings Developer](https://smartthings.developer.samsung.com/) |
| OpenAI | API Key | AI services | [OpenAI Platform](https://platform.openai.com/) |
| Garmin Connect | Username/Password | Fitness data | [Garmin Connect](https://connect.garmin.com/) |

## 🔒 Security Notes

- All API keys are stored in `.env` file (gitignored)
- Session data (Garmin) is excluded from version control
- Use `.env.example` as a template
- Never commit real credentials

## 📝 Recent Improvements

### Code Quality
- ✅ Added type hints to all functions
- ✅ Comprehensive docstrings (Google style)
- ✅ Improved error handling with specific exceptions
- ✅ Standardized credential naming conventions
- ✅ Removed unused imports and dead code

### Project Structure
- ✅ Created proper package structure with `__init__.py` files
- ✅ Organized tests in dedicated directory
- ✅ Added Python version specification (`.python-version`)
- ✅ Pinned all dependency versions

### Testing
- ✅ 71+ unit tests covering all modules
- ✅ Mocked external API calls for fast, reliable tests
- ✅ pytest configuration with coverage reporting
- ✅ Shared fixtures in `conftest.py`
- ✅ Comprehensive testing documentation

### Documentation
- ✅ Updated README with usage examples
- ✅ Created TESTING.md for test documentation
- ✅ Added CLAUDE.md for AI assistant guidance
- ✅ Inline code documentation

## 🤝 Contributing

1. Install development dependencies: `pip install -r requirements-dev.txt`
2. Run tests before committing: `pytest`
3. Format code: `black .`
4. Sort imports: `isort .`
5. Run linters: `flake8 . && pylint **/*.py`

## 📄 License

This project is for educational and personal use.

## 🔗 Additional Resources

- [Project Testing Guide](TESTING.md)
- [Claude Code Instructions](CLAUDE.md)
- [Test Directory](tests/README.md)