import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QLabel, QTextEdit, QLineEdit, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create the sidebar
        sidebar = QTabWidget(self)
        tab1 = QWidget()
        tab2 = QWidget()

        # Add content to tab 1
        tab1_layout = QVBoxLayout()
        # Add a QGridLayout to the first tab
        grid_layout = QGridLayout()

        # Add 20 buttons to the grid layout
        for i in range(20):
            button = QPushButton(f"Table {i+1}")
            button.setFixedSize(100, 100)
            button.clicked.connect(lambda checked, index=i: self.open_new_window(index))
            grid_layout.addWidget(button, i//5, i%5)

        tab1_layout.addLayout(grid_layout)
        tab1.setLayout(tab1_layout)

        # Add content to tab 2
        tab2_layout = QVBoxLayout()
        tab2_label = QLabel("This is the content of Tab 2")
        tab2_textarea = QTextEdit()
        tab2_textarea.setReadOnly(True)

        tab2_layout.addWidget(tab2_label)
        tab2_layout.addWidget(tab2_textarea)
        tab2.setLayout(tab2_layout)

        sidebar.addTab(tab1, "Restaurant")
        sidebar.addTab(tab2, "Takeaway")



        # Create the layout
        hbox = QHBoxLayout()
        hbox.addWidget(sidebar)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setWindowTitle('GPOS')
        self.show()

        # Create a connection to the database
        self.conn = sqlite3.connect('pos.db')

        # Create a cursor object
        self.cursor = self.conn.cursor()

        # Create a table to store data (if it doesn't exist already)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                name TEXT,
                range TEXT
            )
        ''')

    def open_new_window(self, button_index):
        # Create a new window
        new_window = QWidget(self)
        new_window.setWindowTitle(f"Button {button_index+1} clicked")
        new_window.setGeometry(100, 100, 300, 200)

        # Add a label to the new window
        label = QLabel(f"You clicked Button {button_index+1}!")
        label.setAlignment(Qt.AlignCenter)

        # Add a layout to the new window and add the label to it
        layout = QVBoxLayout()
        layout.addWidget(label)

        # Set the layout for the new window and show it
        new_window.setLayout(layout)
        new_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
