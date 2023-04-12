from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtCore import Qt


class LedgerModel(QSqlTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def data(self, item, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.TextAlignmentRole and item.column() != 1:

            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.BackgroundRole:
            if self.data(self.index(item.row(), 4), Qt.ItemDataRole.DisplayRole) == 'Доход':

                return QBrush(QColor.fromRgb(20, 255, 20, 100))

            return QBrush(QColor.fromRgb(255, 20, 0, 100))

        return super(LedgerModel, self).data(item, role)


if __name__ == '__main__':
    pass
