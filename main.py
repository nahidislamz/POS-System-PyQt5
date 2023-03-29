import sys
import sqlite3
from PyQt5.QtWidgets import QApplication,QListWidget,QTableWidget,QComboBox, QTableView,QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QLabel, QTextEdit, QLineEdit, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.init_db()

    def initUI(self):
        self.setFixedSize(1280, 700)
        sidebar = QTabWidget(self)
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()


        # Add content to tab 1
        tab1_layout = QVBoxLayout()
        # Add a QGridLayout to the first tab
        grid_layout = QGridLayout()

        # Add 20 buttons to the grid layout
        for i in range(20):
            button = QPushButton(f"Table {i+1}")
            button.setFixedSize(200, 200)
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
        sidebar.addTab(tab3, "Add Category")
        sidebar.addTab(tab4,  'Add Menus')

        #content for tab 3
        tab3_layout = QHBoxLayout()
        # Add a QGridLayout to the first tab
        grid_layout = QGridLayout()

        # Add widgets to the grid layout
        label1 = QLabel("Category Name")
        label2 = QLabel("Range")
        text_field1 = QLineEdit()
        text_field2 = QLineEdit()
        grid_layout.addWidget(label1, 0, 0)
        grid_layout.addWidget(text_field1, 0, 1)
        grid_layout.addWidget(label2, 1, 0)
        grid_layout.addWidget(text_field2, 1, 1)

        save_button = QPushButton("Save Category")
        save_button.clicked.connect(lambda: self.add_categories(text_field1.text(), text_field2.text()))

        grid_layout.addWidget(save_button, 3, 0, 1, 2)

        # create database connection
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydatabase.db')
        #db.setConnectOptions('QSQLITE_OPEN_URI;QSQLITE_BUSY_TIMEOUT=5000')
        if not db.open():
            print('Unable to open database')
            exit(1)
        # Create a query to select all records from the 'people' table
        query = QSqlQuery()
        query.exec_("SELECT * FROM categories")

        # Create a table model to hold the query results
        model = QSqlTableModel()
        model.setQuery(query)

        # Create a table view to display the model
        table = QTableView(tab3)
        table.setModel(model)
        tab3_layout.addWidget(table)

        tab3_layout.addLayout(grid_layout)
        tab3.setLayout(tab3_layout)

        # Create the layout
        hbox = QHBoxLayout()
        hbox.addWidget(sidebar)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setWindowTitle('GPOS')
        self.show()


        # content for tab layout 4
        tab4_layout = QVBoxLayout()

        # Create the input fields
        input_layout = QHBoxLayout()
        # create parent combo box
        cat_label = QLabel('Category:')
        self.cat_combo = QComboBox()
        cat_query = QSqlQuery('SELECT * FROM categories')
        while cat_query.next():
            self.cat_combo.addItem(cat_query.value('name'))
        db.close()
        
        menu_item_input = QLineEdit()
        number_input = QLineEdit()
        price_input = QLineEdit()
        input_layout.addWidget(QLabel("Menu Item: "))
        input_layout.addWidget(menu_item_input)
        input_layout.addWidget(QLabel("Menu Number: "))
        input_layout.addWidget(number_input)
        input_layout.addWidget(cat_label)
        input_layout.addWidget(self.cat_combo)
        input_layout.addWidget(QLabel("Price: "))
        input_layout.addWidget(price_input)
        # Create the add button
        add_button = QPushButton("Add Item")
        add_button.clicked.connect(lambda: self.add_item(menu_item_input.text(),number_input.text(), price_input.text()))

        # Add the input fields and add button to the layout
        tab4_layout.addLayout(input_layout)
        tab4_layout.addWidget(add_button)
        # Create the table to display the data
        table_widget = QTableWidget()
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["Menu Item", "Number","Cat_ID" ,"Price"])
        tab4_layout.addWidget(table_widget)
        # Retrieve the data from the database and populate the table
        query = QSqlQuery("SELECT * FROM menus")
        while query.next():
            menu_item = QTableWidgetItem(query.value(2))
            number = QTableWidgetItem(str(query.value(3)))
            categories = QTableWidgetItem(str(query.value(1)))
            price = QTableWidgetItem(str(query.value(4)))

            row = table_widget.rowCount()
            table_widget.insertRow(row)
            table_widget.setItem(row, 0, menu_item)
            table_widget.setItem(row, 1, menu_number)
            table_widget.setItem(row, 2, categories)
            table_widget.setItem(row, 3, price)
        tab4.setLayout(tab4_layout)


    def init_db(self):
        # Create a connection to the database
        self.conn = sqlite3.connect('mydatabase.db')
        # Create a cursor object
        self.cursor = self.conn.cursor()
        # Create a table to store data (if it doesn't exist already)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                range TEXT
            )
        ''')

        # create child table with foreign key to parent table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS menus (
                category_id INTEGER,
                menu_number INTEGER,
                menu_item TEXT,
                price REAL,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            );
        ''')

    def add_categories(self, name, range):
        self.cursor.execute('''
            INSERT INTO categories (name, range)
            VALUES (?, ?)
        ''', (name, range))
        #self.cursor.execute("INSERT INTO categories (id,name,range) VALUES (? ,?, ?)")
        self.conn.commit()
        # Show a message box indicating success
        QMessageBox.information(self, "Success", "Data saved to catgories")

    def add_item(self, menu_item, menu_number, price):
        # Insert the new item into the database
                # get selected parent id
        cat_name = self.cat_combo.currentText()
        cat_query = QSqlQuery(f"SELECT * FROM categories WHERE name = '{cat_name}'")
        cat_query.first()
        category_id = cat_query.value(0)

        # insert record into child table
        self.cursor.execute('''
            INSERT INTO menus (category_id,menu_item, menu_number, price) 
            VALUES (?, ?, ?,?)
        ''', (category_id, menu_item, menu_number,price))
        
        self.conn.commit()
        

        QMessageBox.information(self, "Success", "Data saved to catgories")
        
        # clear inputs
        #self.cat_combo.setCurrentIndex(0)
        #self.value_input.clear()
    def open_new_window(self,button_index):
        # Create a new window
        self.hide()
        self.new_window = QWidget()
        #self.new_window.setFixedSize(1280, 700)
        self.new_window.setWindowTitle(f"Table {button_index+1}")
        self.new_window.setGeometry(50, 50, 1280, 700)

        # Create a list widget
        self.list_widget = QListWidget(self.new_window)

        # Add items to the list widget from the database
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydatabase.db')
        if not db.open():
            print("Could not open database")
            sys.exit(-1)
        query = QSqlQuery('SELECT * FROM categories')
        while query.next():
            name = query.value(1)
            range = query.value(2)
            self.list_widget.addItem(f'{name} \n {range}')

        # Set the central widget of the new window to the list widget
        #self.new_window.setCentralWidget(self.list_widget)

        # Create a vertical layout and add the list widget to it
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_widget)

        # Set the layout of the new window to the vertical layout
        self.new_window.setLayout(self.layout)

        # Show the new window
        self.new_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
