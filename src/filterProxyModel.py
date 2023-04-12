from PyQt6.QtCore import QSortFilterProxyModel
from PyQt6.QtCore import Qt


class FilterProxyModel(QSortFilterProxyModel):
    def __init__(self, source_model, parent=None):
        super().__init__(parent)
        self.source_model = source_model

        self.update_model()

        self.setFilterKeyColumn(1)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def change_column_focus(self, value):
        match value:
            case 'Наименование':
                self.setFilterKeyColumn(1)
            case 'Дата':
                self.setFilterKeyColumn(2)
            case 'Сумма':
                self.setFilterKeyColumn(3)
            case 'Статья доходов/расходов':
                self.setFilterKeyColumn(4)

    def update_model(self):
        self.setSourceModel(self.source_model)
