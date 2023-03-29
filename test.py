from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Child Record')

        # create connection to database
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydatabase.db')
        db.open()

        # create parent combo box
        parent_label = QLabel('Parent:')
        self.parent_combo = QComboBox()
        parent_query = QSqlQuery('SELECT * FROM categories')
        while parent_query.next():
            self.parent_combo.addItem(parent_query.value('name'))

        # create value input
        value_label = QLabel('Value:')
        self.value_input = QLineEdit()

        # create add button
        add_button = QPushButton('Add')
        add_button.clicked.connect(self.add_child_record)

        # create layout
        layout = QVBoxLayout()
        parent_layout = QHBoxLayout()
        parent_layout.addWidget(parent_label)
        parent_layout.addWidget(self.parent_combo)
        layout.addLayout(parent_layout)
        layout.addWidget(value_label)
        layout.addWidget(self.value_input)
        layout.addWidget(add_button)

        # create widget and set layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_child_record(self):
        # get selected parent id
        parent_name = self.parent_combo.currentText()
        parent_query = QSqlQuery(f"SELECT * FROM categories WHERE name = '{parent_name}'")
        parent_query.first()
        parent_id = parent_query.value('id')

        # get value input
        value = self.value_input.text()

        # insert record into child table
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO child_table (parent_id, value)
            VALUES (:parent_id, :value)
        """)
        query.bindValue(':parent_id', parent_id)
        query.bindValue(':value', value)
        query.exec_()

        # clear inputs
        self.parent_combo.setCurrentIndex(0)
        self.value_input.clear()

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
