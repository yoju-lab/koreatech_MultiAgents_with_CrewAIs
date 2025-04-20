# Useful APIs for Services

This directory contains Python wrappers for various external APIs used in the project.

## APIs Included:

### 1. Amadeus APIs (Flight & Hotel Search)

*   **Purpose:** Provides flight offer search and hotel search functionalities.
*   **Developer Portal:** [https://developers.amadeus.com/](https://developers.amadeus.com/)
*   **Files:** `amadeus_flight_api.py`, `amadeus_hotel_api.py`
*   **API Key:** Requires API Key and Secret from the Amadeus developer portal.

### 2. Google Places API

*   **Purpose:** Used to find place information (potentially for locations near hotels or destinations).
*   **Developer Portal:** [https://console.cloud.google.com/](https://console.cloud.google.com/) (Navigate to APIs & Services > Credentials)
*   **File:** `google_places_api.py`
*   **API Key:** Requires an API Key enabled for the Places API from the Google Cloud Console.

### 3. ExchangeRate-API

*   **Purpose:** Fetches real-time currency exchange rates.
*   **Developer Portal:** [https://www.exchangerate-api.com/](https://www.exchangerate-api.com/)
*   **File:** `exchangerate_api.py`
*   **API Key:** Requires an API Key from the ExchangeRate-API website.

## Setup

To use these APIs, you must obtain the necessary API keys from each respective provider and configure them appropriately (e.g., using environment variables or a configuration file). 