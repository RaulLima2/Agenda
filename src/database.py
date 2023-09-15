from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def _createContactsTable() -> None:
    createTableQuery:str = """
        CREATE TABLE IF NOT EXISTS agenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            nome VARCHAR(40) NOT NULL,
            telefone VARCHAR(40) NOT NULL,
            email VARCHAR(40) NOT NULL,
            instagram VARCHAR(40) NOT NULL,
            twitter VARCHAR(40) NOT NULL,
            facebook VARCHAR(40) NOT NULL
        )
    """
    query:QSqlQuery = QSqlQuery()
    query.exec(createTableQuery)

def connection(database_name:str) -> bool:
    db:QSqlDatabase = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(database_name)
    if not db.open():
        QMessageBox.critical(
            None,
            "App Name - Error!",
            f"Database Error: {db.lastError().text()}"
        )
        return False
    _createContactsTable()
    return True