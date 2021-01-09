# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/VoterDataExtractor.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import constants

import utility
import ocr
import text_mining
import generate_excel
import generate_images
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QFileDialog, QDialog, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox

from PyQt5.QtCore import QThread, pyqtSignal


class MainDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        # self.setObjectName("Dialog")
        self.resize(808, 435)
        self.setMinimumSize(QtCore.QSize(808, 435))
        self.setMaximumSize(QtCore.QSize(808, 435))
        self.selectedFiles = QtWidgets.QTextBrowser(self)
        self.selectedFiles.setGeometry(QtCore.QRect(9, 42, 761, 31))
        self.selectedFiles.setObjectName("selectedFiles")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(9, 9, 250, 27))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(10, 160, 761, 248))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        # self.progressBar = QtWidgets.QProgressBar(self.widget)
        # self.progressBar.setProperty("value", 0)
        # self.progressBar.setObjectName("progressBar")
        # self.verticalLayout_3.addWidget(self.progressBar)
        self.logTextArea = QtWidgets.QTextEdit(self.widget)
        self.logTextArea.setObjectName("logTextArea")
        self.verticalLayout_3.addWidget(self.logTextArea)
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setGeometry(QtCore.QRect(10, 90, 198, 29))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.browseButton = QtWidgets.QPushButton(self.splitter)
        self.browseButton.setObjectName("browseButton")
        self.typeComboBox = QtWidgets.QComboBox(self.splitter)
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.setMinimumWidth(105)
        self.splitter_2 = QtWidgets.QSplitter(self)
        self.splitter_2.setGeometry(QtCore.QRect(600, 90, 170, 29))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.startButton = QtWidgets.QPushButton(self.splitter_2)
        self.startButton.setObjectName("startButton")
        self.cancleButton = QtWidgets.QPushButton(self.splitter_2)
        self.cancleButton.setObjectName("cancleButton")

        self.filenames = []

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        # _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("Voters\'s Data Extractor")

        self.selectedFiles.setPlaceholderText("List of PDF files")
        self.label.setText("Converting Pdf files to Xls:")
        self.show()
        self.label_2.setText("Progress :")

        self.logTextArea.setPlaceholderText("Displaying here the progress of conversion")
        self.browseButton.setText("Browse")

        self.typeComboBox.setCurrentText("--Select Type--")
        self.typeComboBox.setItemText(0, "--Select Type--")
        self.typeComboBox.setItemText(1,  constants.PDF_TYPES[0])
        # self.typeComboBox.setItemText(2, constants.PDF_TYPES[1])
        self.startButton.setText("Start")
        self.cancleButton.setText("Cancel")

        # self.show()

        self.browseButton.clicked.connect(self.browseButton_handler)

        self.startButton.clicked.connect(self.startButton_handler)
        self.cancleButton.clicked.connect(self.cancleButton_handler)
        self.voters_extraction_thread = PDFVoterExtractionThread()  # This is the thread object
        # Connect the signal from the thread to the finished method
        self.voters_extraction_thread.signal.connect(self.update_log_text)

    def closeEvent(self, event):
        print("closing PyQtTest")
        # utility.delete_generated_files()

    def startButton_handler(self):
        self.logTextArea.clear()
        if self.selectedFiles.toPlainText() == '':
            self.show_error('Please Select at least one PDF')
        elif self.typeComboBox.currentText() not in constants.PDF_TYPES:
            self.show_error('Please Select the PDF type')
        else:
            self.disable_controls()
            self.logTextArea.clear()
            self.voters_extraction_thread.fileslist = self.filenames
            self.voters_extraction_thread.pdftype = self.typeComboBox.currentText()
            self.logTextArea.append('Voter Data Extraction started:')
            self.voters_extraction_thread.start()

    def cancleButton_handler(self):
        if self.voters_extraction_thread.isRunning():
            self.voters_extraction_thread.terminate()
            self.enable_controls()
            self.logTextArea.clear()

    def browseButton_handler(self):
        self.open_dialog_box()

    def open_dialog_box(self):
        # filenames = QFileDialog.getOpenFileNames(self,"Select pdf files to process",)
        filenames_obj = QFileDialog.getOpenFileNames(self.browseButton, "Starts PDF files to process", '.', '*.pdf')
        self.filenames = filenames_obj[0]
        self.selectedFiles.setText(self.filenames.__str__()[1:-1])

    def enable_controls(self):
        self.typeComboBox.setEnabled(True)
        self.startButton.setEnabled(True)
        self.browseButton.setEnabled(True)

    def disable_controls(self):
        self.typeComboBox.setDisabled(True)
        self.startButton.setDisabled(True)
        self.browseButton.setDisabled(True)

    def show_error(self, error):
        error_popup = QtWidgets.QErrorMessage(self.startButton)
        error_popup.setWindowTitle('Error')
        error_popup.showMessage(error)

    def update_log_text(self, message):
        if message == 'Finish':
            self.enable_controls()
        self.logTextArea.append(message)


class PDFVoterExtractionThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.fileslist = []
        self.pdftype = ''

    # run method gets called when we start the thread
    def run(self):
        for filepath in self.fileslist:
            try:
                utility.delete_files(constants.VOTER_PNG_PATH)
                utility.delete_files(constants.PAGE_PNG_PATH)

                self.signal.emit('Extracting images started for file:'+filepath+' @'+utility.get_time())
                generate_images.pdf_to_png(filepath)
                self.signal.emit('Ocr process started: @'+utility.get_time())
                ocr.generate_text()
                self.signal.emit('Text mining process started: @'+utility.get_time())
                common_voter_data = text_mining.extract_common_detail()
                # print(result)
                voter_list = text_mining.extract_voter_details()
                # print(result)
                # sub_division.add_subdiv(result[1])
                if self.pdftype == constants.PDF_TYPES[0]:
                    excel_name = generate_excel.createExcelForNagarParishad(filepath, common_voter_data, voter_list)
                elif self.pdftype == constants.PDF_TYPES[1]:
                    excel_name = generate_excel.createExcelForPanchayat(filepath, common_voter_data, voter_list)
                self.signal.emit('Text Mining process completed with file:'+excel_name+': @'+utility.get_time()+'\n')

            except Exception as e:
                self.signal.emit('Voter Extraction interrupted for current file.')
                print(traceback.format_exc())
                # print(e)
        self.signal.emit('Finish')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # Dialog = QtWidgets.QDialog()
    dialog = MainDialog()
    dialog.show()
    sys.exit(app.exec_())
