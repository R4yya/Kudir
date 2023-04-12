from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QHeaderView

from databaseOperator import DatabaseOperator, create_connection
from filterProxyModel import FilterProxyModel

from toolWindow import ToolWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_operator = DatabaseOperator()
        self.db_operator.set_database_model()
        self.filter_proxy_model = FilterProxyModel(self.db_operator.db_model)
        self.setup_ui()

    def setup_icons(self):
        self.icon_kudir = QtGui.QIcon()
        self.icon_kudir.addPixmap(QtGui.QPixmap('img/kudir.ico'),
                                  QtGui.QIcon.Mode.Normal,
                                  QtGui.QIcon.State.Off)
        self.icon_add = QtGui.QIcon()
        self.icon_add.addPixmap(QtGui.QPixmap('img/plus.ico'),
                                QtGui.QIcon.Mode.Normal,
                                QtGui.QIcon.State.Off)
        self.icon_delete = QtGui.QIcon()
        self.icon_delete.addPixmap(QtGui.QPixmap('img/delete.ico'),
                                   QtGui.QIcon.Mode.Normal,
                                   QtGui.QIcon.State.Off)
        self.icon_refresh = QtGui.QIcon()
        self.icon_refresh.addPixmap(QtGui.QPixmap('img/refresh.ico'),
                                    QtGui.QIcon.Mode.Normal,
                                    QtGui.QIcon.State.Off)
        self.icon_new_table = QtGui.QIcon()
        self.icon_new_table.addPixmap(QtGui.QPixmap('img/new-table.ico'),
                                      QtGui.QIcon.Mode.Normal,
                                      QtGui.QIcon.State.Off)
        self.icon_sct_tbl = QtGui.QIcon()
        self.icon_sct_tbl.addPixmap(QtGui.QPixmap('img/select-table.ico'),
                                    QtGui.QIcon.Mode.Normal,
                                    QtGui.QIcon.State.Off)

    def setup_stylesheets(self):
        self.table_hheader_stylesheet = '''
            QHeaderView {
                border: none;
                border-bottom: 2px solid black;
                font-size: 12pt
            }
            QHeaderView::section:horizontal {
                border: none;
                border-right: 1px solid #7d7d7d;
            }
            '''
        self.table_view_stylesheet = '''
            QTableView{
                gridline-color: #7d7d7d;
            }
            '''

    def setup_fonts(self):
        self.font_main = QtGui.QFont()
        self.font_main.setFamily('Consolas')
        self.font_main.setPointSize(14)
        self.font_main.setBold(True)
        self.font_main.setWeight(75)

        self.font_table = QtGui.QFont()
        self.font_table.setFamily('Courier')
        self.font_table.setPointSize(12)

    def setup_ui(self):
        self.setup_icons()
        self.setup_fonts()
        self.setup_stylesheets()

        self.setObjectName('MainWindow')
        self.resize(800, 600)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setWindowIcon(self.icon_kudir)

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName('central_widget')
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setObjectName('grid_layout')

        self.label_add = QtWidgets.QLabel(self.central_widget)
        self.label_add.setFont(self.font_main)
        self.label_add.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_add.setObjectName('label_add')
        self.grid_layout.addWidget(self.label_add, 1, 0, 1, 1)

        self.label_delete = QtWidgets.QLabel(self.central_widget)
        self.label_delete.setFont(self.font_main)
        self.label_delete.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_delete.setObjectName('label_delete')
        self.grid_layout.addWidget(self.label_delete, 1, 1, 1, 1)

        self.label_refresh = QtWidgets.QLabel(self.central_widget)
        self.label_refresh.setFont(self.font_main)
        self.label_refresh.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_refresh.setObjectName('label_refresh')
        self.grid_layout.addWidget(self.label_refresh, 1, 2, 1, 1)

        self.button_add = QtWidgets.QPushButton(self.central_widget)
        self.button_add.setIcon(self.icon_add)
        self.button_add.setIconSize(QtCore.QSize(64, 64))
        self.button_add.setFlat(True)
        self.button_add.setObjectName('button_add')
        self.button_add.clicked.connect(self.raise_tool_window)
        self.grid_layout.addWidget(self.button_add, 0, 0, 1, 1)

        self.button_delete = QtWidgets.QPushButton(self.central_widget)
        self.button_delete.setIcon(self.icon_delete)
        self.button_delete.setIconSize(QtCore.QSize(64, 64))
        self.button_delete.setFlat(True)
        self.button_delete.setObjectName('button_elete')
        self.button_delete.clicked.connect(self.delete_row_from_table)
        self.grid_layout.addWidget(self.button_delete, 0, 1, 1, 1)

        self.button_refresh = QtWidgets.QPushButton(self.central_widget)
        self.button_refresh.setIcon(self.icon_refresh)
        self.button_refresh.setIconSize(QtCore.QSize(64, 64))
        self.button_refresh.setFlat(True)
        self.button_refresh.setObjectName('button_refresh')
        self.button_refresh.clicked.connect(self.update_table_view)
        self.grid_layout.addWidget(self.button_refresh, 0, 2, 1, 1)

        self.edit_filter = QtWidgets.QLineEdit(self)
        self.edit_filter.setObjectName('edit_filter')
        self.edit_filter.setPlaceholderText('Введите фильтр здесь...')
        self.edit_filter.textChanged.connect(
            self.set_table_view_model_to_proxy)
        self.grid_layout.addWidget(self.edit_filter, 2, 0, 1, 2)

        self.combo_box_filtered_column = QtWidgets.QComboBox(self)
        self.combo_box_filtered_column.setObjectName(
            'combo_box_filtered_column')
        self.combo_box_filtered_column.addItem('Наименование')
        self.combo_box_filtered_column.addItem('Дата')
        self.combo_box_filtered_column.addItem('Сумма')
        self.combo_box_filtered_column.addItem('Статья доходов/расходов')
        self.combo_box_filtered_column.currentTextChanged.connect(
            self.on_combobox_changed)
        self.grid_layout.addWidget(self.combo_box_filtered_column, 2, 2, 1, 1)

        self.table_view = QtWidgets.QTableView(self.central_widget)
        self.table_view.setFont(self.font_table)
        self.table_view.setObjectName('table_view')
        self.table_view.setSortingEnabled(True)
        self.table_view.setStyleSheet(self.table_view_stylesheet)
        self.table_hheader = self.table_view.horizontalHeader()
        self.table_hheader.setStyleSheet(self.table_hheader_stylesheet)
        self.table_vheader = self.table_view.verticalHeader()
        self.table_vheader.setVisible(False)
        self.grid_layout.addWidget(self.table_view, 3, 0, 1, 3)

        self.update_table_view()

        self.table_hheader.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents)
        self.table_hheader.setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch)
        self.table_hheader.setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_hheader.setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents)
        self.table_hheader.setSectionResizeMode(
            4, QHeaderView.ResizeMode.ResizeToContents)

        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate(
            'MainWindow', 'Книга учета доходов и расходов'))

        self.label_delete.setText(_translate(
            'MainWindow', 'Удалить позицию'))
        self.label_add.setText(_translate(
            'MainWindow', 'Добавить позицию'))
        self.label_refresh.setText(_translate(
            'MainWindow', 'Обновить'))

    def update_table_view(self):
        self.edit_filter.clear()

        self.db_operator.set_database_model()

        self.table_view.setModel(self.db_operator.db_model)
        self.table_view.update()

    def set_table_view_model_to_proxy(self):
        self.filter_proxy_model = FilterProxyModel(self.db_operator.db_model)

        self.table_view.setModel(self.filter_proxy_model)

        self.filter_proxy_model.change_column_focus(
            self.combo_box_filtered_column.currentText())
        self.filter_proxy_model.setFilterRegularExpression(
            self.edit_filter.text())

    def raise_tool_window(self):
        self.tool_window = ToolWindow()
        self.tool_window.show()

    def delete_row_from_table(self):
        index_list = []

        for model_index in self.table_view.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)

        for index in index_list:
            self.db_operator.db_model.removeRow(index.row())

        self.update_table_view()

    def on_combobox_changed(self, value):
        self.filter_proxy_model.change_column_focus(value)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    if not create_connection():
        sys.exit(1)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
