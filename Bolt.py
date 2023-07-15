import sys
from PyQt5.QtCore import QUrl, QFileInfo, Qt, QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QLabel, QAction, QMenu, QFileDialog, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QContextMenuEvent, QCursor
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem
from PyQt5.QtCore import QUrl, QFileInfo, Qt, QDate
from PyQt5.QtGui import QDesktopServices

class DownloadsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bolt - ჩამოტვირთვები")
        self.setGeometry(100, 100, 600, 400)  # Set the window size

        # Create a layout for the downloads window
        layout = QVBoxLayout()

        # Create a label for the downloads page
        label = QLabel("Downloads")
        label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Add the label to the layout
        layout.addWidget(label)

        # Create a list widget to show downloaded items
        self.downloads_list = QListWidget()
        self.downloads_list.itemDoubleClicked.connect(self.open_downloaded_file)

        # Add the list widget to the layout
        layout.addWidget(self.downloads_list)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_download_item(self, file_path, name, date):
        item = QListWidgetItem()
        item.setText(f"Name: {name}\nLocation: {file_path}\nDate: {date}")
        self.downloads_list.addItem(item)

    def open_downloaded_file(self, item):
        file_path = item.text().split("\n")[1].split(": ")[1]
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bolt - ქართული ბრაუზერი")
        self.setGeometry(100, 100, 800, 600)  # Set a larger window size

        # Create the address bar and go button
        self.address_bar = QLineEdit()
        self.go_button = QPushButton("ძებნა")
        self.go_button.setFixedWidth(50)  # Adjust the width of the Go button

        # Create the web view
        self.webview = QWebEngineView()

        # Create the tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Create the button to add new tabs
        self.new_tab_button = QPushButton()
        self.new_tab_button_label = QLabel("ახალი ფანჯარა")
        self.new_tab_button_label.setStyleSheet("font-size: 15px; font-weight: italic;")
        self.new_tab_button.setFixedSize(40, 45)  # Adjust the size of the button
        self.new_tab_button_layout = QHBoxLayout()
        self.new_tab_button_layout.addWidget(self.new_tab_button_label)
        self.new_tab_button_layout.setContentsMargins(0, 0, 0, 0)
        self.new_tab_button_layout.setAlignment(self.new_tab_button_label.alignment())
        self.new_tab_button.setLayout(self.new_tab_button_layout)
        self.new_tab_button.setToolTip("ახალი ფანჯარა")  # Add a tooltip for the button

        # Create the downloads button
        self.downloads_button = QPushButton("...")
        self.downloads_button.setFixedWidth(25)  # Adjust the width of the button

        # Create the downloads menu
        self.downloads_menu = QMenu()
        self.downloads_action = QAction("ჩამოტვირთვები", self)
        self.downloads_menu.addAction(self.downloads_action)
        self.downloads_button.setMenu(self.downloads_menu)

        # Set up the layout
        layout = QVBoxLayout()
        address_layout = QHBoxLayout()  # Separate layout for the address bar and Go button
        address_layout.addWidget(self.address_bar)
        address_layout.addWidget(self.go_button)
        address_layout.addWidget(self.new_tab_button)  # Add the new tab button to the address layout
        address_layout.addWidget(self.downloads_button)  # Add the downloads button to the address layout

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
        self.downloads_action.triggered.connect(self.show_downloads_window)
        self.webview.page().profile().downloadRequested.connect(self.download_requested)

    def add_tab(self):
        webview = QWebEngineView()
        webview.loadFinished.connect(self.update_tab_title)
        tab_index = self.tab_widget.addTab(webview, "ახალი ფანჯარა")
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

    def show_downloads_window(self):
        downloads_window = DownloadsWindow()
        downloads_window.show()

    def download_requested(self, download_item):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.png)", options=options)
        if file_path:
            download_item.setPath(file_path)
            download_item.accept()
            QMessageBox.information(self, "Download", f"File downloaded and saved to:\n{file_path}")
            name = QFileInfo(file_path).fileName()
            date = QDate.currentDate().toString(Qt.DefaultLocaleLongDate)
            downloads_window = self.findChild(DownloadsWindow)
            if downloads_window:
                downloads_window.add_download_item(file_path, name, date)

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = QMenu(self)
        save_image_action = menu.addAction("Save Image")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == save_image_action:
            self.save_image(event.pos())

    def save_image(self, position):
        webview = self.tab_widget.currentWidget()
        context_menu = webview.page().createContextMenu()
        action = context_menu.exec_(QCursor.pos())
        if action and action.is_valid():
            request = action.toWebEngineDownloadRequest()
            request.finished.connect(self.image_download_finished)

    def image_download_finished(self):
        download_item = self.sender()
        if download_item.state() == QWebEngineDownloadItem.DownloadCompleted:
            file_path = download_item.path()
            QMessageBox.information(self, "Download", f"Image downloaded and saved to:\n{file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = BrowserWindow()
    browser.show()
    sys.exit(app.exec_())
