# AUTO Marketplace Extension

A browser extension for AUTO marketplace with Shopee integration.

## Features

- Connect to AUTO marketplace API
- Monitor Shopee orders
- Automatically deliver digital products
- Receive notifications for new orders
- Manage orders directly from the extension

## Development

This extension is built with [Plasmo](https://www.plasmo.com/), a browser extension framework.

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Setup

1. Clone the repository
2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Load the extension in your browser:
   - Chrome: Go to `chrome://extensions/`, enable Developer mode, and click "Load unpacked". Select the `build/chrome-mv3-dev` directory.
   - Firefox: Go to `about:debugging#/runtime/this-firefox`, click "Load Temporary Add-on", and select any file in the `build/firefox-mv2-dev` directory.

### Building for Production

```bash
npm run build
```

The built extension will be in the `build` directory.

## Integration with AUTO Marketplace

This extension integrates with the AUTO marketplace backend API to:

1. Fetch orders from the marketplace
2. Deliver digital products automatically
3. Update order status

## Shopee Integration

The extension adds functionality to Shopee order pages:

1. Automatically detects Shopee order pages
2. Extracts order information
3. Provides a button to deliver digital products directly from Shopee

## Configuration

The extension requires the following configuration:

- API URL: The URL of the AUTO marketplace API
- API Key: Your API key for authentication

These settings are stored securely in the browser's local storage.
