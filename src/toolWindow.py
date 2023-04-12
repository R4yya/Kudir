from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget

from databaseOperator import DatabaseOperator

from datetime import datetime


class ToolWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_operator = DatabaseOperator()
        self.db_operator.set_database_model()

        self.setup_ui()

        self.setWindowModality(QtCore.Qt.WindowModality(2))

    def setup_icon(self):
        self.icon_kudir = QtGui.QIcon()
        self.icon_kudir.addPixmap(QtGui.QPixmap('img/kudir.ico'),
                                  QtGui.QIcon.Mode.Normal,
                                  QtGui.QIcon.State.Off)

    def setup_font(self):
        self.font = QtGui.QFont()
        self.font.setPointSize(12)

    def setup_ui(self):
        self.setup_icon()
        self.setup_font()

        self.setObjectName('ToolWindow')
        self.resize(350, 160)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(350, 160))
        self.setMaximumSize(QtCore.QSize(350, 160))
        self.setWindowIcon(self.icon_kudir)

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setObjectName('grid_layout')

        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setFont(self.font)
        self.label_name.setObjectName('label_name')
        self.grid_layout.addWidget(self.label_name, 0, 0, 1, 1)

        self.edit_name = QtWidgets.QLineEdit(self)
        self.edit_name.setObjectName('edit_name')
        self.grid_layout.addWidget(self.edit_name, 0, 1, 1, 1)

        self.label_date = QtWidgets.QLabel(self)
        self.label_date.setFont(self.font)
        self.label_date.setObjectName('label_date')
        self.grid_layout.addWidget(self.label_date, 1, 0, 1, 1)

        self.date_edit = QtWidgets.QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(datetime.now())
        self.date_edit.setObjectName('date_edit')
        self.grid_layout.addWidget(self.date_edit, 1, 1, 1, 1)

        self.label_amount = QtWidgets.QLabel(self)
        self.label_amount.setFont(self.font)
        self.label_amount.setObjectName('label_amount')
        self.grid_layout.addWidget(self.label_amount, 2, 0, 1, 1)

        self.edit_amount = QtWidgets.QLineEdit(self)
        self.edit_amount.setObjectName('edit_amount')
        self.grid_layout.addWidget(self.edit_amount, 2, 1, 1, 1)

        self.label_item = QtWidgets.QLabel(self)
        self.label_item.setFont(self.font)
        self.label_item.setObjectName('label_item')
        self.grid_layout.addWidget(self.label_item, 3, 0, 1, 1)

        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.setObjectName('combo_box')
        self.combo_box.addItem('Доход')
        self.combo_box.addItem('Расход')
        self.grid_layout.addWidget(self.combo_box, 3, 1, 1, 1)

        self.button_submit = QtWidgets.QPushButton(self)
        self.button_submit.setObjectName('button_submit')
        self.button_submit.clicked.connect(lambda: self.add_row_into_table())
        self.grid_layout.addWidget(self.button_submit, 4, 2, 1, 1)

        self.retranslate_ui()

        # QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate('ToolWindow', 'Добавить позицию'))

        self.label_name.setText(_translate('ToolWindow', 'Наименование:'))
        self.label_date.setText(_translate('ToolWindow', 'Дата:'))
        self.label_amount.setText(_translate('ToolWindow', 'Сумма:'))
        self.label_item.setText(_translate('ToolWindow', 'Тип:'))

        self.button_submit.setText(_translate('ToolWindow', 'Добавить'))

    def add_row_into_table(self):
        self.db_operator.add_row_into_model(
            self.edit_name.text(),
            self.date_edit.date().toPyDate().strftime('%d/%m/%Y'),
            self.edit_amount.text(),
            self.combo_box.currentText())


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    tool_window = ToolWindow()
    tool_window.show()
    sys.exit(app.exec())
