import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QDialog, QVBoxLayout, QGridLayout, QPushButton, QLabel,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtGui import QPixmap

class DBHelper():
    def __init__(self):
        self.conn = sqlite3.connect("sdms.db")
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS student(sid INTEGER, Sname TEXT, dept INTEGER, "
                       "year INTEGER, course_a INTEGER, course_b INTEGER, course_c INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS faculty(fid INTEGER, f_name TEXT, course INTEGER, "
                       "dept INTEGER, class_room INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS Course(cid INTEGER, c_name INTEGER, faculty TEXT, "
                       "credit INTEGER, type INTEGER, slot INTEGER, No_enrolled INTEGER)")

    def add_student(self, sid, Sname, dept, year, course_a, course_b, course_c):
        try:
            self.c.execute("INSERT INTO student(sid, Sname, dept, year, course_a, course_b, course_c) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?)", (sid, Sname, dept, year, course_a, course_b, course_c))
            self.conn.commit()
            QMessageBox.information(None, 'Successful', 'Student added successfully to the database.')
        except Exception as e:
            QMessageBox.warning(None, 'Error', f'Could not add student to the database. Error: {str(e)}')

    def search_student(self, sid):
        self.c.execute("SELECT * FROM student WHERE sid=?", (sid,))
        data = self.c.fetchone()

        if not data:
            QMessageBox.warning(None, 'Error', f'Could not find any student with roll no {sid}')
            return None

        student_info = list(data)
        self.conn.close()
        show_student(student_info)

    def delete_record(self, sid):
        try:
            self.c.execute("DELETE FROM student WHERE sid=?", (sid,))
            self.conn.commit()
            QMessageBox.information(None, 'Successful', 'Student deleted from the database.')
        except Exception as e:
            QMessageBox.warning(None, 'Error', f'Could not delete student from the database. Error: {str(e)}')

def show_student(info):
    sid, sname, dept, year, course_a, course_b, course_c = info

    dept_names = ["Mechanical Engineering", "Chemical Engineering", "Software Engineering",
                  "Biotech Engineering", "Computer Science and Engineering", "Information Technology"]

    year_names = ["1st", "2nd", "3rd", "4th"]

    course_names = ["DBMS", "OS", "CN", "C++", "JAVA", "PYTHON", "THERMO", "MACHINE", "CELLS",
                    "DS", "CRE", "MICROBES", "FERTILIZER", "PLANTS", "MOBILE APP"]

    table = QTableWidget()
    table.setWindowTitle("Student Details")
    table.setRowCount(7)
    table.setColumnCount(2)

    table.setItem(0, 0, QTableWidgetItem("Roll"))
    table.setItem(0, 1, QTableWidgetItem(str(sid)))
    table.setItem(1, 0, QTableWidgetItem("Name"))
    table.setItem(1, 1, QTableWidgetItem(str(sname)))
    table.setItem(2, 0, QTableWidgetItem("Department"))
    table.setItem(2, 1, QTableWidgetItem(str(dept_names[dept])))
    table.setItem(3, 0, QTableWidgetItem("Year"))
    table.setItem(3, 1, QTableWidgetItem(str(year_names[year])))
    table.setItem(4, 0, QTableWidgetItem("Slot A"))
    table.setItem(4, 1, QTableWidgetItem(str(course_names[course_a])))
    table.setItem(5, 0, QTableWidgetItem("Slot B"))
    table.setItem(5, 1, QTableWidgetItem(str(course_names[course_b])))
    table.setItem(6, 0, QTableWidgetItem("Slot C"))
    table.setItem(6, 1, QTableWidgetItem(str(course_names[course_c])))
    table.horizontalHeader().setStretchLastSection(True)
    table.show()

    dialog = QDialog()
    dialog.setWindowTitle("Student Details")
    dialog.resize(500, 300)
    dialog.setLayout(QVBoxLayout())
    dialog.layout().addWidget(table)
    dialog.exec()

class AddStudent(QDialog):
    def __init__(self):
        super().__init__()

        self.dept = -1
        self.year = -1
        self.sid = -1
        self.sname = ""
        self.course_a = -1
        self.course_b = -1
        self.course_c = -1

        self.btnCancel = QPushButton("Cancel", self)
        self.btnReset = QPushButton("Reset", self)
        self.btnAdd = QPushButton("Add", self)

        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.yearCombo = QComboBox(self)
        self.yearCombo.addItems(["1st", "2nd", "3rd", "4th"])

        self.branchCombo = QComboBox(self)
        self.branchCombo.addItems(["Mechanical", "Chemical", "Software", "Biotech",
                                   "Computer Science", "Information Technology"])

        self.cACombo = QComboBox(self)
        self.cACombo.addItems(["DBMS", "OS", "CN", "C++", "JAVA", "PYTHON", "THERMO", "MACHINE",
                               "CELLS", "DS", "CRE", "MICROBES", "FERTILIZER", "PLANTS"])

        self.cBCombo = QComboBox(self)
        self.cBCombo.addItems(["DBMS", "OS", "CN", "C++", "JAVA", "PYTHON", "THERMO", "MACHINE",
                               "CELLS", "DS", "CRE", "MICROBES", "FERTILIZER", "PLANTS"])

        self.cCCombo = QComboBox(self)
        self.cCCombo.addItems(["DBMS", "OS", "CN", "C++", "JAVA", "PYTHON", "THERMO", "MACHINE",
                               "CELLS", "DS", "CRE", "MICROBES", "FERTILIZER", "PLANTS", "MOBILE APP"])

        self.rollLabel = QLabel("Roll No")
        self.nameLabel = QLabel("Name")
        self.cALabel = QLabel("Slot A")
        self.yearLabel = QLabel("Current Year")
        self.cBLabel = QLabel("Slot B")
        self.branchLabel = QLabel("Branch")
        self.cCLabel = QLabel("Slot C")

        self.rollText = QLineEdit(self)
        self.nameText = QLineEdit(self)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.rollLabel, 1, 1)
        self.grid.addWidget(self.nameLabel, 2, 1)
        self.grid.addWidget(self.yearLabel, 3, 1)
        self.grid.addWidget(self.branchLabel, 4, 1)
        self.grid.addWidget(self.cALabel, 5, 1)
        self.grid.addWidget(self.cBLabel, 6, 1)
        self.grid.addWidget(self.cCLabel, 7, 1)

        self.grid.addWidget(self.rollText, 1, 2)
        self.grid.addWidget(self.nameText, 2, 2)
        self.grid.addWidget(self.yearCombo, 3, 2)
        self.grid.addWidget(self.branchCombo, 4, 2)
        self.grid.addWidget(self.cACombo, 5, 2)
        self.grid.addWidget(self.cBCombo, 6, 2)
        self.grid.addWidget(self.cCCombo, 7, 2)

        self.grid.addWidget(self.btnReset, 9, 1)
        self.grid.addWidget(self.btnCancel, 9, 3)
        self.grid.addWidget(self.btnAdd, 9, 2)

        self.btnAdd.clicked.connect(self.add_student)
        self.btnCancel.clicked.connect(self.close)
        self.btnReset.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Add Student Details")
        self.resize(500, 300)

    def reset(self):
        self.rollText.setText("")
        self.nameText.setText("")

    def add_student(self):
        self.year = self.yearCombo.currentIndex()
        self.dept = self.branchCombo.currentIndex()
        self.sid = int(self.rollText.text())
        self.sname = self.nameText.text()
        self.course_a = self.cACombo.currentIndex()
        self.course_b = self.cBCombo.currentIndex()
        self.course_c = self.cCCombo.currentIndex()

        db_helper = DBHelper()
        db_helper.add_student(self.sid, self.sname, self.dept, self.year, self.course_a, self.course_b, self.course_c)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        grid_layout = QGridLayout()

        self.btn_enter_student = QPushButton("Enter Student Details", self)
        self.btn_show_student_details = QPushButton("Show Student Details", self)
        self.btn_delete_record = QPushButton("Delete Record", self)

        self.pic_label = QLabel(self)
        self.pic_label.resize(150, 150)
        self.pic_label.move(120, 10)
        self.pic_label.setScaledContents(True)
        self.pic_label.setPixmap(QPixmap("user.png"))

        grid_layout.addWidget(self.pic_label, 0, 0)

        buttons = [self.btn_enter_student, self.btn_delete_record, self.btn_show_student_details]
        button_texts = ["Enter Student Details", "Delete Record", "Show Student Details"]

        for i, btn in enumerate(buttons):
            btn.move(15 + i * 190, 170)
            btn.resize(180, 40)
            btn_font = btn.font()
            btn_font.setPointSize(13)
            btn.setFont(btn_font)
            btn.clicked.connect(self.button_clicked)
            btn.setText(button_texts[i])
            grid_layout.addWidget(btn, 1, i)

        self.setLayout(grid_layout)
        self.setFixedSize(600, 280)
        self.setWindowTitle("Student Database Management System")

    def button_clicked(self):
        sender = self.sender()

        if sender == self.btn_enter_student:
            add_student_dialog = AddStudent()
            add_student_dialog.exec()
        elif sender == self.btn_show_student_details:
            self.show_student_dialog()
        elif sender == self.btn_delete_record:
            self.show_delete_dialog()

    def show_student_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Enter Roll No")

        vbox = QVBoxLayout()
        text = QLabel("Enter the roll no of the student")
        edit_field = QLineEdit()
        btn_search = QPushButton("Search", dialog)
        btn_search.clicked.connect(lambda: self.show_student(edit_field.text()))
        vbox.addWidget(text)
        vbox.addWidget(edit_field)
        vbox.addWidget(btn_search)
        dialog.setLayout(vbox)

        dialog.exec()

    def show_delete_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Delete Record")

        vbox = QVBoxLayout()
        text = QLabel("Enter the roll no of the student")
        edit_field = QLineEdit()
        btn_search_delete = QPushButton("Search", dialog)
        btn_search_delete.clicked.connect(lambda: self.delete_record(edit_field.text()))
        vbox.addWidget(text)
        vbox.addWidget(edit_field)
        vbox.addWidget(btn_search_delete)
        dialog.setLayout(vbox)

        dialog.exec()

    def show_student(self, roll_no):
        if roll_no == "":
            QMessageBox.warning(None, 'Error', 'You must give the roll number to show the results for.')
            return None

        show_student_helper = DBHelper()
        show_student_helper.search_student(int(roll_no))

    def delete_record(self, roll_no):
        if roll_no == "":
            QMessageBox.warning(None, 'Error', 'You must give the roll number to show the results for.')
            return None

        delete_record_helper = DBHelper()
        delete_record_helper.delete_record(int(roll_no))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
