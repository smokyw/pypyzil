# PyPyzil Project Context

## Overview
PyPyzil is a Python library for scraping real estate data from the Zillow website. The library allows users to extract information about properties including houses, apartments, rental listings, sales, and recently sold properties. It uses web scraping with proxy support to bypass restrictions and collect detailed real estate information.

## Project Structure
```
pypyzil/
├── src/
│   └── pyzill/
│       ├── __init__.py
│       ├── details.py
│       ├── parse.py
│       ├── search.py
│       └── utils.py
├── test.py
├── README.md
├── .gitignore
└── .gitattributes
```

## Architecture
The project is organized into 5 main modules:

1. **details.py**: Contains functions for retrieving information about specific properties by ID or URL
2. **search.py**: Contains functions for searching real estate by various criteria (sale, rent, sold)
3. **parse.py**: Contains logic for parsing HTML content and extracting JSON data
4. **utils.py**: Contains utility functions for data processing and proxy management
5. **__init__.py**: Exports the main functions for access from external code

## Key Features
- **Property Information Retrieval**: Get property details by ID or URL
  - `get_from_home_id(property_id, proxy_url=None)`: Get house information by ID
  - `get_from_home_url(home_url, proxy_url=None)`: Get house information by URL
  - `get_from_department_id(department_id, proxy_url=None)`: Get apartment information by ID
  - `get_from_department_url(department_url, proxy_url=None)`: Get apartment information by URL

- **Real Estate Search**: Search for properties by various filters
  - `for_sale(...)`: Search for properties for sale
  - `for_rent(...)`: Search for properties for rent
  - `sold(...)`: Search for recently sold properties

- **Proxy Support**: All functions support proxy usage to avoid IP blocking

- **Geographic Search**: Support for searching within specific geographic bounds using coordinates

## Dependencies
- `curl_cffi`: For making HTTP requests with browser impersonation support
- `beautifulsoup4`: For parsing HTML documents
- `typing`: For type annotations

## Usage Example
```python
import pyzill
import json

# Generate proxy URL
proxy_url = pyzill.parse_proxy("premium.residential.proxyrack.net", "9000", "masamasa-country-US", "G7NR8PY-6UUOGDK-B3KHXDU-JLMUNR7-IXHHRVL-0N0MR6S-AX0ESBN")

# Define geographic boundaries
ne_lat = 38.602951833355434
ne_long = -87.22283859375
sw_lat = 23.42674607019482
sw_long = -112.93084640625

# Search for rentals
results_rent = pyzill.for_rent(pagination=1,
              search_value="",
              is_entire_place=False,
              is_room=True,
              min_beds=1,
              max_beds=None,
              min_bathrooms=None,
              max_bathrooms=None,
              min_price=10000,
              max_price=None,
              ne_lat=ne_lat,
              ne_long=ne_long,
              sw_lat=sw_lat,
              sw_long=sw_long,
              zoom_value=15,
              proxy_url=proxy_url)

# Save results to JSON file
with open("./jsondata_rent2.json", "w") as f:
    json.dump(results_rent, f)
```

## Important Notes
- **Result Limit**: Maximum size of `mapResults` is 500. Even if you paginate through all results, you won't get more than 500 results.
- **Proxy Usage**: Recommended to use proxies to avoid IP blocking from Zillow
- **Browser Impersonation**: Library uses `impersonate="chrome124"` to mimic Chrome browser requests
- **Geographic Filtering**: Use coordinate bounds (NE/SW lat/long) for location-based searches

## Development Conventions
- All functions include type hints
- Russian comments have been added throughout the codebase
- Functions are organized by purpose (property details vs. search functionality)
- Code follows Python best practices with clear function separation