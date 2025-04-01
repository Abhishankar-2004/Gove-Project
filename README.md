# Gove Web Browser

A lightweight, customizable web browser built with PyQt5 and QtWebEngine.

![Gove Logo](logo2.png)

## Features

- **Clean, Modern UI**: Intuitive interface with colorful, responsive design
- **Tab Management**: Create, close, and reopen tabs with ease
- **Bookmarking**: Save and manage your favorite websites
- **Browsing History**: Keep track of visited websites
- **Private Browsing Mode**: Browse without leaving history traces
- **Download Manager**: Monitor and manage file downloads
- **Secure Connection Indicator**: Visual indicator for HTTPS connections
- **Ad Blocking**: Basic ad-blocking functionality built-in
- **PDF Viewer**: Integrated viewer for PDF documents
- **Authentication System**: Secure login system to protect your browsing session

## Screenshots

*[Screenshots to be added]*

## Installation

### Prerequisites

- Python 3.6+
- PyQt5
- PyQtWebEngine

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/gove-browser.git
   cd gove-browser
   ```

2. Install dependencies:
   ```
   pip install PyQt5 PyQtWebEngine
   ```

3. Run the browser:
   ```
   python browser.py
   ```

### Default Login Credentials

For demonstration purposes, the browser uses the following default credentials:
- Username: `admin`
- Password: `password123`

**Note**: This is for development only. In a production environment, implement a proper authentication system.

## Project Structure

- `browser.py`: Main application code
- `browser_session.json`: Saved browsing session
- `logo2.png`: Browser logo
- `icon/`: Directory containing UI icons

## Usage

### Basic Navigation

- Use the navigation bar to enter URLs or search terms
- Click the back, forward, and reload buttons for standard navigation
- Use the home button to return to the default search page (Google)

### Tab Management

- Create new tabs with the "New Tab" button
- Close tabs with the "Close Tab" button or by clicking the X on the tab
- Reopen recently closed tabs with the "Reopen Tab" button

### Bookmarks and History

- Access your bookmarks by clicking the "Bookmarks" button
- View your browsing history by clicking the "History" button

### Private Mode

Toggle private browsing mode to prevent storing history and other browsing data.

### Downloads

The browser will display a download dialog when downloading files, showing progress and allowing you to:
- Cancel downloads
- Open the download folder

## Customization

### Change Default Homepage

To change the default homepage, modify the URL in the `navigate_home()` method:

```python
def navigate_home(self):
    self.tabs.currentWidget().setUrl(QUrl('https://your-preferred-homepage.com'))
```

### Change Download Directory

To change the default download directory, modify the path in the `update_browser_profile()` method:

```python
profile.setDownloadPath("/your/preferred/download/path")
```

## Security Features

- **Password Hashing**: User passwords are hashed using SHA-256
- **HTTPS Indicator**: Visual indication of secure connections
- **Private Browsing**: Option to browse without storing history

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyQt5 team for the excellent GUI framework
- QtWebEngine for the web browsing capabilities
- All contributors who help improve this project
