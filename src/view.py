from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import (
	QAbstractItemView,
	QDialog,
	QDialogButtonBox,
	QFormLayout,
	QHBoxLayout,
	QLineEdit,
	QMainWindow,
	QMessageBox,
	QPushButton,
	QTableView,
	QVBoxLayout,
	QWidget,
	QFileDialog
)

from .model import AgendaModel

class Window(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("Agenda")
		self.resize(550, 250)
		self.centralWidget = QWidget()
		self.setCentralWidget(self.centralWidget)
		self.layout = QHBoxLayout()
		self.centralWidget.setLayout(self.layout)
		self.agendaModel = AgendaModel()
		self.setupUI()

	def setupUI(self):
		self.table = QTableView(self)
		self.table.setModel(self.agendaModel.model)
		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.resizeColumnsToContents()

		self.addButton = QPushButton("Adicionar")
		self.addButton.clicked.connect(self.openAddDialog)
		self.deleteButton = QPushButton("Deletar")
		self.deleteButton.clicked.connect(self.delete_agenda)
		self.importButton = QPushButton("Importar")
		self.importButton.clicked.connect(self.import_agenda)
		self.exportButton = QPushButton("Exportar")
		self.exportButton.clicked.connect(self.export_agenda)
		self.clearAllButton = QPushButton("Remover Tudo")
		self.clearAllButton.clicked.connect(self.clear_agenda)

		layout = QVBoxLayout()
		layout.addWidget(self.addButton)
		layout.addWidget(self.deleteButton)
		layout.addWidget(self.importButton)
		layout.addWidget(self.exportButton)
		layout.addStretch()
		layout.addWidget(self.clearAllButton)
		self.layout.addWidget(self.table)
		self.layout.addLayout(layout)
	
	def openAddDialog(self):
		dialog = AddDialog(self)
		if dialog.exec() == QDialog.Accepted:
			self.agendaModel.add_agenda(dialog.data)
			self.table.resizeColumnsToContents()

	def delete_agenda(self):
		row = self.table.currentIndex().row()
		if row < 0:
			return
		message_box = QMessageBox.warning(
			self,
			"Remover Contato",
			"Tem certeza que deseja remover este contato?",
			QMessageBox.Ok | QMessageBox.Cancel
		)

		if message_box == QMessageBox.Ok:
			self.agendaModel.delete_agenda(row)

	def clear_agenda(self):
		message_box = QMessageBox.warning(
			self,
			"Remover Todos os Contatos",
			"Tem certeza que deseja remover todos os contatos?",
			QMessageBox.Ok | QMessageBox.Cancel
		)

		if message_box == QMessageBox.Ok:
			self.agendaModel.clear_agenda()
	
	def import_agenda(self):
		#import data csv
		message_box = QMessageBox.warning(
			self,
			"Importar Dados da Agenda",
			"Deseja importar os dados",
			QMessageBox.Ok | QMessageBox.Cancel
		)

		if message_box == QMessageBox.Ok:
			path = QFileDialog.getOpenFileName(self, 'Salvar Arquivo', QDir.homePath(), 'CSV Files(*.csv)')
			self.agendaModel.import_agenda(path[0])

	def export_agenda(self):
		#export data to csv
		message_box = QMessageBox.warning(
			self,
			"Exportar Dados da Agenda",
			"Deseja exportar os dados",
			QMessageBox.Ok | QMessageBox.Cancel
		)

		if message_box == QMessageBox.Ok:
			path = QFileDialog.getSaveFileName(self, 'Salvar Arquivo', QDir.homePath()+'/agenda.csv', 'CSV Files(*.csv)')
			self.agendaModel.export_agenda(path[0])


class AddDialog(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("Adicionar Contato")
		self.resize(250, 150)
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		self.data = None

		self.setupUI()

	def setupUI(self):
		self.nameField = QLineEdit()
		self.phoneField = QLineEdit()
		self.emailField = QLineEdit()
		self.instagram = QLineEdit()
		self.twitter = QLineEdit()
		self.facebook = QLineEdit()

		self.nameField.setObjectName("Nome")
		self.phoneField.setObjectName("Telefone")
		self.emailField.setObjectName("Email")
		self.instagram.setObjectName("Instagram")
		self.twitter.setObjectName("Twitter")
		self.facebook.setObjectName("Facebook")

		layout = QFormLayout()
		layout.addRow("Nome: ", self.nameField)
		layout.addRow("Telefone: ", self.phoneField)
		layout.addRow("Email: ", self.emailField)
		layout.addRow("Instagram: ", self.instagram)
		layout.addRow("Twitter: ", self.twitter)
		layout.addRow("Facebook: ", self.facebook)

		self.layout.addLayout(layout)
		self.buttonsBox = QDialogButtonBox(self)
		self.buttonsBox.setOrientation(Qt.Horizontal)
		self.buttonsBox.setStandardButtons(
			 QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		)
		self.buttonsBox.accepted.connect(self.accept)
		self.buttonsBox.rejected.connect(self.reject)
		self.layout.addWidget(self.buttonsBox)
	
	def accept(self):
		self.data = []
		for field in (self.nameField, self.phoneField, self.emailField, self.instagram, self.twitter, self.facebook):
			if not field.text():
				QMessageBox.critical(
					self,
					"Erro",
					f"Campo {field.objectName()} não pode ser vazio"
				)
				self.data = None
				return
			self.data.append(field.text())
		if not self.data:
			return
		super().accept()
	
	def reject(self):
		self.data = None
		super().reject()