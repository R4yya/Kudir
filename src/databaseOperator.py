from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

from ledgerModel import LedgerModel


class DatabaseOperator(object):
    def __init__(self, selected_table='my_ledger'):
        self.selected_table = selected_table

    def set_database_model(self):
        self.db_model = LedgerModel()

        self.db_model.setTable(self.selected_table)
        self.db_model.setEditStrategy(
            QSqlTableModel.EditStrategy.OnFieldChange)

        self.db_model.select()

    def add_row_into_model(self, name, date, amount, item):
        new_record = self.db_model.record()

        new_record.setValue(1, name)
        new_record.setValue(2, date)
        new_record.setValue(3, amount)
        new_record.setValue(4, item)

        row_position = self.db_model.rowCount()

        self.db_model.insertRecord(row_position, new_record)


def create_connection():
    con = QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName('ledger.db')

    if not con.open():
        return False
    return True


if __name__ == '__main__':
    if create_connection():
        db_operator = DatabaseOperator()
        print(db_operator.get_list_of_tables())
