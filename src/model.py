import csv
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class AgendaModel():
    __headers: tuple = ()
    __model: QSqlTableModel = None

    def __init__(self):
        self.__model = self._createModel()

    def _createModel(self) -> QSqlTableModel:
        model = QSqlTableModel()
        model.setTable("agenda")
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()
        self.__headers = ("ID", "Nome", "Telefone", "Email", "Instagram", "Twitter", "Facebook")
        
        for index, header in enumerate(self.__headers):
            model.setHeaderData(index, Qt.Horizontal, header)
        return model

    @property
    def model(self) -> QSqlTableModel:
        return self.__model
        
    def add_agenda(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()
    
    def delete_agenda(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
    
    def  clear_agenda(self):
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

    def import_agenda(self, path:str)->None:
        #import data from csv file, using QtSql
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)

        if path:
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row, data in enumerate(reader):
                    self.model.insertRows(row, 1)
                    for column, field in enumerate(data):
                        self.model.setData(self.model.index(row, column + 1), field)
                self.model.submitAll()
                self.model.select()

    def export_agenda(self, path:str) -> None:
        #export data to csv file, using QtSql
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)

        
        if path:
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(self.__headers)
                for row in range(self.model.rowCount()):
                    fields = []
                    for column in range(1, self.model.columnCount()):
                        field = self.model.index(row, column).data()
                        fields.append(field)
                    writer.writerow(fields)