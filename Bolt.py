import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bolt")
        self.setGeometry(100, 100, 800, 600)  # Set a larger window size

        # Create the address bar and go button
        self.address_bar = QLineEdit()
        self.go_button = QPushButton("Go")
        self.go_button.setFixedWidth(50)  # Adjust the width of the Go button

        # Create the web view
        self.webview = QWebEngineView()

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Create the button to add new tabs
        self.new_tab_button = QPushButton()
        self.new_tab_button_label = QLabel("+")
        self.new_tab_button_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.new_tab_button.setFixedSize(25, 25)  # Adjust the size of the button
        self.new_tab_button_layout = QHBoxLayout()
        self.new_tab_button_layout.addWidget(self.new_tab_button_label)
        self.new_tab_button_layout.setContentsMargins(0, 0, 0, 0)
        self.new_tab_button_layout.setAlignment(self.new_tab_button_label.alignment())
        self.new_tab_button.setLayout(self.new_tab_button_layout)
        self.new_tab_button.setToolTip("New Tab")  # Add a tooltip for the button

        # Set up the layout
        layout = QVBoxLayout()
        address_layout = QHBoxLayout()  # Separate layout for the address bar and Go button
        address_layout.addWidget(self.address_bar)
        address_layout.addWidget(self.go_button)
        address_layout.addWidget(self.new_tab_button)  # Add the new tab button to the address layout

        layout.addLayout(address_layout)
        layout.addWidget(self.tab_widget)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Add the initial tab
        self.add_tab()

        # Connect signals to slots
        self.go_button.clicked.connect(self.load_url)
        self.new_tab_button.clicked.connect(self.add_tab)

    def add_tab(self):
        webview = QWebEngineView()
        webview.loadFinished.connect(self.update_tab_title)
        tab_index = self.tab_widget.addTab(webview, "New Tab")
        self.tab_widget.setCurrentIndex(tab_index)

    def close_tab(self, tab_index):
        widget = self.tab_widget.widget(tab_index)
        widget.deleteLater()
        self.tab_widget.removeTab(tab_index)

    def load_url(self):
        url = self.address_bar.text()

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        self.address_bar.setText(url)
        current_webview = self.tab_widget.currentWidget()
        current_webview.load(QUrl(url))

    def update_tab_title(self):
        index = self.tab_widget.currentIndex()
        title = self.tab_widget.currentWidget().page().title()
        self.tab_widget.setTabText(index, title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = BrowserWindow()
    browser.show()
    sys.exit(app.exec_())
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bolt")
        self.setGeometry(100, 100, 800, 600)  # Set a larger window size

        # Create the address bar and go button
        self.address_bar = QLineEdit()
        self.go_button = QPushButton("Go")
        self.go_button.setFixedWidth(50)  # Adjust the width of the Go button

        # Create the web view
        self.webview = QWebEngineView()

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Create the button to add new tabs
        self.new_tab_button = QPushButton()
        self.new_tab_button_label = QLabel("New Tab")
        self.new_tab_button_label.setStyleSheet("font-size: 15px; font-weight: italic;")
        self.new_tab_button.setFixedSize(40, 45)  # Adjust the size of the button
        self.new_tab_button_layout = QHBoxLayout()
        self.new_tab_button_layout.addWidget(self.new_tab_button_label)
        self.new_tab_button_layout.setContentsMargins(0, 0, 0, 0)
        self.new_tab_button_layout.setAlignment(self.new_tab_button_label.alignment())
        self.new_tab_button.setLayout(self.new_tab_button_layout)
        self.new_tab_button.setToolTip("New Tab")  # Add a tooltip for the button

        # Set up the layout
        layout = QVBoxLayout()
        address_layout = QHBoxLayout()  # Separate layout for the address bar and Go button
        address_layout.addWidget(self.address_bar)
        address_layout.addWidget(self.go_button)
        address_layout.addWidget(self.new_tab_button)  # Add the new tab button to the address layout

        layout.addLayout(address_layout)
        layout.addWidget(self.tab_widget)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Add the initial tab
        self.add_tab()

        # Connect signals to slots
        self.go_button.clicked.connect(self.load_url)
        self.new_tab_button.clicked.connect(self.add_tab)

    def add_tab(self):
        webview = QWebEngineView()
        webview.loadFinished.connect(self.update_tab_title)
        tab_index = self.tab_widget.addTab(webview, "New Tab")
        self.tab_widget.setCurrentIndex(tab_index)

    def close_tab(self, tab_index):
        widget = self.tab_widget.widget(tab_index)
        widget.deleteLater()
        self.tab_widget.removeTab(tab_index)

    def load_url(self):
        url = self.address_bar.text()

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        self.address_bar.setText(url)
        current_webview = self.tab_widget.currentWidget()
        current_webview.load(QUrl(url))

    def update_tab_title(self):
        index = self.tab_widget.currentIndex()
        title = self.tab_widget.currentWidget().page().title()
        self.tab_widget.setTabText(index, title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = BrowserWindow()
    browser.show()
    sys.exit(app.exec_())
