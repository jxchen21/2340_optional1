# Google Maps API Setup Instructions

## Quick Setup (Recommended)

Run the setup script to configure your API key automatically:

```bash
python setup_env.py
```

This will guide you through the process and create the necessary `.env` file.

## Manual Setup

### 1. Getting Your API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Maps JavaScript API
   - Geocoding API
4. Go to "Credentials" and create an API key
5. Restrict the API key to your domain for security

### 2. Setting Up the API Key

Create a `.env.local` file in your project root directory with:

```env
# Google Maps API Key
MAPS_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with your actual Google Maps API key.

### 3. Example .env.local file:
```env
MAPS_API_KEY=AIzaSyBvOkBw7cF3jK8L9mN2pQ1rS4tU5vW6xY7z
```

## Security Note
For production, consider:
- Restricting the API key to specific domains
- Using environment variables to store the API key
- Implementing server-side API key management

## Features Included
- Interactive Google Maps display
- User location detection and display
- Location-based markers
- Reverse geocoding for city/country detection
- AJAX location updates to database
- Responsive design with Bootstrap
