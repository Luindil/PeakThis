# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from PyQt4 import QtGui, QtCore
from lmfit import Parameters, Parameter


class ModelWidget(QtGui.QGroupBox):
    model_parameters_changed = QtCore.pyqtSignal(int, Parameters)
    model_selected_changed = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(ModelWidget, self).__init__("Models", parent)

        self.grid_layout = QtGui.QGridLayout()

        self.add_btn = QtGui.QPushButton("Add")
        self.delete_btn = QtGui.QPushButton("Delete")
        self.define_btn = QtGui.QPushButton("Define")

        self.model_list = QtGui.QListWidget()

        self.parameter_table = QtGui.QTableWidget()
        self.parameter_table.verticalHeader().setVisible(False)
        self.parameter_table.setColumnCount(5)

        self.grid_layout.addWidget(self.add_btn, 0, 0)
        self.grid_layout.addWidget(self.delete_btn, 0, 1)
        self.grid_layout.addWidget(self.define_btn, 0, 2)
        self.grid_layout.addWidget(self.model_list, 1, 0, 1, 3)
        self.grid_layout.addWidget(self.parameter_table, 2, 0, 1, 3)

        self.setLayout(self.grid_layout)

        self.model_selector_dialog = ModelSelectorDialog(self.add_btn)

        self.create_signals()

    def show_model_selector_dialog(self):
        self.model_selector_dialog.show()


    def update_parameters(self, parameters):
        self.parameter_table.blockSignals(True)
        self.parameter_table.clear()
        self.parameter_table.setRowCount(len(parameters))
        ind = 0
        for name in parameters:
            self.parameter_table.setItem(ind, 0, QtGui.QTableWidgetItem(name))
            self.parameter_table.setItem(ind, 1, QtGui.QTableWidgetItem(str(parameters[name].value)))
            self.parameter_table.setItem(ind, 2, QtGui.QTableWidgetItem(str(parameters[name].vary)))
            self.parameter_table.setItem(ind, 3, QtGui.QTableWidgetItem(str(parameters[name].min)))
            self.parameter_table.setItem(ind, 4, QtGui.QTableWidgetItem(str(parameters[name].max)))

            ind += 1
        self.parameter_table.resizeColumnsToContents()
        self.parameter_table.blockSignals(False)


    def get_parameters(self):
        parameters = Parameters()
        for row_ind in range(self.parameter_table.rowCount()):
            name = str(self.parameter_table.item(row_ind, 0).text())
            value = convert_qstring_to_float(self.parameter_table.item(row_ind, 1).text())
            vary = convert_qstring_to_float(self.parameter_table.item(row_ind, 2).text())
            min = convert_qstring_to_float(self.parameter_table.item(row_ind, 3).text())
            max = convert_qstring_to_float(self.parameter_table.item(row_ind, 4).text())
            parameters.add(name, value, vary=vary, min=min, max=max)
        return self.model_list.currentRow(), parameters

    def create_signals(self):
        self.model_list.currentRowChanged.connect(self.model_selected_changed)
        self.parameter_table.itemChanged.connect(self.item_changed)

    def item_changed(self):
        self.model_parameters_changed.emit(*self.get_parameters())


def convert_qstring_to_float(text):
    text = str(text)
    if text == "None":
        return None
    elif text == "True":
        return True
    elif text == "False":
        return False
    else:
        return float(text)


class ModelSelectorDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ModelSelectorDialog, self).__init__(parent)

        self.setMaximumSize(50, 250)
        self.setMinimumSize(50, 250)

        self.setWindowTitle("Model Selector")

        self._vertical_layout = QtGui.QVBoxLayout()
        self.model_list = QtGui.QListWidget()
        self.model_list.setMaximumHeight(120)
        self.model_list.setMaximumWidth(180)

        self._ok_cancel_layout = QtGui.QHBoxLayout()
        self.ok_btn = QtGui.QPushButton("OK")
        self.cancel_btn = QtGui.QPushButton("Cancel")

        self._ok_cancel_layout.addSpacerItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                                                               QtGui.QSizePolicy.Fixed))
        self._ok_cancel_layout.addWidget(self.ok_btn)
        self._ok_cancel_layout.addWidget(self.cancel_btn)

        self._vertical_layout.addWidget(self.model_list)
        self._vertical_layout.addLayout(self._ok_cancel_layout)

        self.setLayout(self._vertical_layout)

        self.ok_btn.clicked.connect(self.accept)
        self.model_list.doubleClicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)


    def populate_models(self, model_dict):
        self.model_list.clear()
        for model_key in model_dict:
            self.model_list.addItem(model_key)

    def get_selected_index(self):
        return self.model_list.currentRow()

    def get_selected_item_string(self):
        return str(self.model_list.currentItem().text())

    def show(self):
        QtGui.QWidget.show(self)
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)

        self.activateWindow()
        self.raise_()

