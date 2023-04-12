from PyQt6.QtSql import QSqlQuery

from databaseOperator import create_connection


class Database(object):
    def __init__(self):
        self.selected_table = 'my_ledger'

    def create_table(self):
        create_table_query = QSqlQuery()
        create_table_query.exec(
            f'''
            CREATE TABLE {self.selected_table}(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                Наименование VARCHAR(40) NOT NULL,
                Дата VARCHAR(11) NOT NULL,
                Сумма INTEGER NOT NULL,
                `Статья доходов/расходов` VARCHAR(6) NOT NULL
            )
            '''
        )

    def fill_table(self):
        fill_table_query = QSqlQuery()
        fill_table_query.prepare(
            f'''
            INSERT INTO {self.selected_table}(
                Наименование,
                Дата,
                Сумма,
                `Статья доходов/расходов`
                )
            VALUES (?, ?, ?, ?)
            '''
        )

        data = [
            ('Продукты', '22/12/2022', 2000, 'Расход'),
            ('Кредит', '22/12/2022', 3000, 'Расход'),
            ('Хозтовары', '22/12/2022', 600, 'Расход'),
            ('Зарплата', '22/12/2022', 6000, 'Доход'),
            ('Продукты', '23/12/2022', 1000, 'Расход'),
            ('Зарплата', '23/12/2022', 6000, 'Доход'),
            ('Рестран', '24/12/2022', 4200, 'Расход'),
            ('Аптека', '24/12/2022', 300, 'Расход'),
            ('Зарплата', '24/12/2022', 6000, 'Доход'),
            ('Продукты', '25/12/2022', 1700, 'Расход'),
            ('Зарплата', '25/12/2022', 6000, 'Доход'),
            ('Премия', '25/12/2022', 1000, 'Доход'),
            ('Подарки', '25/12/2022', 5000, 'Расход'),
            ('Лотерейный билет', '25/12/2022', 100, 'Расход'),
            ('Бензин', '25/12/2022', 1000, 'Расход'),
            ('Зарплата', '26/12/2022', 6000, 'Доход'),
            ('Парикмахерская', '26/12/2022', 700, 'Расход'),
            ('Одежда', '26/12/2022', 7000, 'Расход')

        ]

        for name, date, amount, item in data:
            fill_table_query.addBindValue(name)
            fill_table_query.addBindValue(date)
            fill_table_query.addBindValue(amount)
            fill_table_query.addBindValue(item)

            fill_table_query.exec()


if __name__ == '__main__':
    if create_connection():
        db = Database()
        db.create_table()
        db.fill_table()
