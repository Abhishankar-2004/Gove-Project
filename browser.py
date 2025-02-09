import sys
import hashlib
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineDownloadItem

# Simple hash function for demonstration
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setFixedSize(400, 200)  # Larger dialog box

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Using hashed password for demo purposes
        self.valid_credentials = {'admin': hash_password('password123')}

    def check_credentials(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Username and password cannot be empty')
            return

        hashed_password = hash_password(password)
        
        if username in self.valid_credentials and self.valid_credentials[username] == hashed_password:
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')

class DownloadDialog(QDialog):
    def __init__(self, download_item, parent=None):
        super().__init__(parent)
        self.download_item = download_item
        self.setWindowTitle('Download')
        self.setFixedSize(400, 100)

        layout = QVBoxLayout()

        self.file_name_label = QLabel(f"Downloading: {download_item.url().fileName()}")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.progress_bar)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_download)
        layout.addWidget(self.cancel_button)

        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.clicked.connect(self.open_download_folder)
        layout.addWidget(self.open_folder_button)

        self.setLayout(layout)

        self.download_item.downloadProgress.connect(self.update_progress)
        self.download_item.finished.connect(self.download_finished)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def download_finished(self):
        QMessageBox.information(self, 'Download Complete', 'Download finished successfully.')
        self.accept()

    def cancel_download(self):
        self.download_item.cancel()
        self.accept()

    def open_download_folder(self):
        file_path = self.download_item.path()
        if os.path.exists(file_path):
            os.startfile(os.path.dirname(file_path))
        else:
            QMessageBox.warning(self, 'Error', 'File not found')

class FullScreenWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fullScreenRequested(self, fullScreen):
        if fullScreen:
            self.showFullScreen()
        else:
            self.showNormal()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome to Gove')
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f4f4;
            }
        """)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)  # Connect to close_tab
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.setCentralWidget(self.tabs)
        self.setWindowIcon(QIcon("logo2.png"))
        # Initialize attributes before calling add_new_tab
        self.last_closed_tab = None
        self.bookmarks = []
        self.history = []
        self.downloads = []
        self.private_mode = False

        self.create_toolbar()
        self.create_statusbar()

        self.add_new_tab(QUrl('https://www.google.com'), 'Google Search')

        # Show colorful welcome message
        self.show_welcome_message()

    def add_new_tab(self, url, label="New Tab"):
        browser = FullScreenWebEngineView()
        self.update_browser_profile(browser)
        browser.setUrl(url)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.urlChanged.connect(self.handle_url_change)
        browser.loadFinished.connect(lambda: self.update_title(browser))
        browser.page().profile().downloadRequested.connect(self.handle_download)
        browser.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        browser.page().runJavaScript(self.get_adblocker_script())
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

    def update_browser_profile(self, browser):
        if self.private_mode:
            profile = QWebEngineProfile()
        else:
            profile = QWebEngineProfile.defaultProfile()
            profile.setDownloadPath("path/to/your/download/directory")  # Set custom download directory
        browser.setPage(QWebEnginePage(profile))

    def close_tab(self, index):
        if self.tabs.count() < 2:
            return
        self.last_closed_tab = (self.tabs.widget(index), self.tabs.tabText(index))
        self.tabs.removeTab(index)

    def reopen_last_closed_tab(self):
        if self.last_closed_tab:
            browser, label = self.last_closed_tab
            self.tabs.addTab(browser, label)
            self.last_closed_tab = None

    def create_toolbar(self):
        navbar = QToolBar(self)
        navbar.setStyleSheet("""
            QToolBar {
                background-color: #007bff;
                border: none;
            }
            QToolButton {
                background-color: #ffffff;
                border: 1px solid #007bff;
                border-radius: 5px;
                padding: 5px;
                margin: 2px;
            }
            QToolButton:hover {
                background-color: #0056b3;
                color: #ffffff;
            }
        """)
        self.addToolBar(navbar)
         # Add logo to the toolbar
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("logo2.png")
        logo_label.setPixmap(logo_pixmap.scaled(30, 30, Qt.KeepAspectRatio))
        navbar.addWidget(logo_label)

        actions = [
            (r'icon/back.png', 'Back', lambda: self.tabs.currentWidget().back()),
            (r'icon/next.png', 'Forward', lambda: self.tabs.currentWidget().forward()),
            (r'icon/reload.png', 'Reload', lambda: self.tabs.currentWidget().reload()),
            (r'icon/home.png', 'Home', self.navigate_home),
            (r'icon/newtab.png', 'New Tab', lambda: self.add_new_tab(QUrl('https://www.google.com'), 'New Tab')),
            (r'icon/closetab.png', 'Close Tab', lambda: self.close_tab(self.tabs.currentIndex())),
            (r'icon/reopentab.png', 'Reopen Tab', self.reopen_last_closed_tab),
            (r'icon/bookmark.png', 'Bookmarks', self.show_bookmarks),
            (r'icon/history.png', 'History', self.show_history),
            (r'icon/private.png', 'Private Mode', self.toggle_private_mode),
        ]

        for icon, name, callback in actions:
            btn = QAction(QIcon(icon), name, self)
            btn.triggered.connect(callback)
            navbar.addAction(btn)

        # URL bar setup
        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #007bff;
                border-radius: 10px;
                padding: 5px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #0056b3;
            }
        """)
        self.url_bar.returnPressed.connect(self.handle_url_or_search)
        self.url_bar.setPlaceholderText("Enter URL or search")
        navbar.addWidget(self.url_bar)

        # Secure connection indicator
        self.secure_indicator = QLabel()
        self.secure_indicator.setStyleSheet("""
            QLabel {
                font-weight: bold;
                padding: 5px;
            }
        """)
        navbar.addWidget(self.secure_indicator)

    def create_statusbar(self):
        self.statusbar = QStatusBar()
        self.statusbar.setStyleSheet("""
            QStatusBar {
                background-color: #007bff;
                color: #ffffff;
                border: none;
                padding: 5px;
            }
        """)
        self.setStatusBar(self.statusbar)

    def handle_url_or_search(self):
        text = self.url_bar.text()
        qurl = QUrl(text)
        if not qurl.isValid() or qurl.scheme() == '':
            qurl = QUrl(f"https://{text}")
        else:
            qurl = QUrl(f"{text}")
        self.tabs.currentWidget().setUrl(qurl)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl('https://www.google.com'))

    def update_url(self, q, browser=None):
        if browser and browser == self.tabs.currentWidget():
            self.url_bar.setText(q.toString())
            self.statusbar.showMessage(q.toString())
            self.update_secure_indicator(q)

    def update_title(self, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            title = browser.page().title()
            self.tabs.setTabText(index, title)
            self.statusbar.showMessage(title)

    def update_url_bar(self, index):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl, self.tabs.currentWidget())

    def update_secure_indicator(self, url):
        if url.scheme() == 'https':
            self.secure_indicator.setText("Secure")
            self.secure_indicator.setStyleSheet("color: green;")
        else:
            self.secure_indicator.setText("Not Secure")
            self.secure_indicator.setStyleSheet("color: red;")

    def add_bookmark(self):
        current_url = self.tabs.currentWidget().url().toString()
        if current_url not in self.bookmarks:
            self.bookmarks.append(current_url)
            self.statusbar.showMessage(f"Bookmarked: {current_url}")
        else:
            self.statusbar.showMessage("URL already bookmarked")

    def show_bookmarks(self):
        bookmarks_dialog = QDialog(self)
        bookmarks_dialog.setWindowTitle("Bookmarks")
        bookmarks_dialog.setFixedSize(400, 300)  # Larger dialog box
        layout = QVBoxLayout(bookmarks_dialog)
        list_widget = QListWidget()
        for url in self.bookmarks:
            list_widget.addItem(url)
        layout.addWidget(list_widget)
        bookmarks_dialog.setLayout(layout)
        bookmarks_dialog.exec_()

    def show_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("Browsing History")
        history_dialog.setFixedSize(400, 300)  # Larger dialog box
        layout = QVBoxLayout(history_dialog)
        list_widget = QListWidget()
        for url in self.history:
            list_widget.addItem(url)
        layout.addWidget(list_widget)
        history_dialog.setLayout(layout)
        history_dialog.exec_()

    def toggle_private_mode(self):
        self.private_mode = not self.private_mode
        self.update_browser_profile(self.tabs.currentWidget())
        self.statusbar.showMessage(f"Private Mode {'On' if self.private_mode else 'Off'}")

    def get_adblocker_script(self):
        return '''
        (function() {
            var style = document.createElement('style');
            style.innerHTML = 'body { display: none !important; }';
            document.head.appendChild(style);
        })();
        '''

    def handle_download(self, download_item: QWebEngineDownloadItem):
        download_dialog = DownloadDialog(download_item, self)
        download_dialog.exec_()
        if download_item.state() == QWebEngineDownloadItem.Cancelled:
            self.statusbar.showMessage(f"Download cancelled: {download_item.url().toString()}")
        else:
            self.downloads.append(download_item)
            self.statusbar.showMessage(f"Downloading: {download_item.url().toString()}")

    def handle_url_change(self, qurl):
        if not self.private_mode:
            self.history.append(qurl.toString())

    def show_welcome_message(self):
        welcome_message = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .welcome { color: #ffffff; background-color: #007bff; padding: 20px; border-radius: 10px; text-align: center; }
                .welcome h1 { margin: 0; font-size: 24px; }
                .welcome p { font-size: 18px; }
            </style>
        </head>
        <body>
            <div class="welcome">
                <h1>Welcome to Our Custom Web Browser!</h1>
                <p>Enjoy a personalized browsing experience.</p>
            </div>
        </body>
        </html>
        """
        msg_box = QDialog(self)
        msg_box.setWindowTitle("Welcome")
        msg_box.setFixedSize(500, 250)  # Larger dialog box
        layout = QVBoxLayout()
        web_view = QWebEngineView()
        web_view.setHtml(welcome_message)
        layout.addWidget(web_view)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(msg_box.accept)
        layout.addWidget(ok_button)

        msg_box.setLayout(layout)
        msg_box.exec_()

    def generate_pdf_viewer_html(self, pdf_url):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>PDF Viewer</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js"></script>
            <style>
                body {{ margin: 0; }}
                #pdf-viewer {{ width: 100vw; height: 100vh; }}
            </style>
        </head>
        <body>
            <div id="pdf-viewer"></div>
            <script>
                var url = '{pdf_url}';
                var pdfjsLib = window['pdfjs-dist/build/pdf'];
                pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';
                
                var loadingTask = pdfjsLib.getDocument(url);
                loadingTask.promise.then(function(pdf) {{
                    console.log('PDF loaded');
                    
                    pdf.getPage(1).then(function(page) {{
                        console.log('Page loaded');
                        
                        var scale = 1.5;
                        var viewport = page.getViewport({{scale: scale}});
                        
                        var canvas = document.createElement('canvas');
                        var context = canvas.getContext('2d');
                        canvas.height = viewport.height;
                        canvas.width = viewport.width;
                        document.getElementById('pdf-viewer').appendChild(canvas);
                        
                        var renderContext = {{
                            canvasContext: context,
                            viewport: viewport
                        }};
                        var renderTask = page.render(renderContext);
                        renderTask.promise.then(function () {{
                            console.log('Page rendered');
                        }});
                    }});
                }}, function (reason) {{
                    console.error(reason);
                }});
            </script>
        </body>
        </html>
        """

def main():
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
