#!/usr/bin/env python

print('Importing modules...')
import sys
import os
import subprocess
import re
import time
import traceback

import pandas as pd

from functools import partial

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QAction,
    QMenu, QMessageBox, QStyleFactory, QHBoxLayout
)
from PyQt5.QtCore import (
    Qt, QProcess, pyqtSignal, pyqtSlot, QTimer, QSize,
    QSettings, QUrl, QObject
)
from PyQt5.QtGui import QFontDatabase, QIcon, QDesktopServices
from pyqtgraph.Qt import QtGui

# acdc modules
try:
    # We try to import from cellacdc instead of "from ." to check
    # if cellacdc was installed with pip or not
    from cellacdc import (
        dataPrep, segm, gui, dataStruct, utils, help, qrc_resources, myutils,
        cite_url, html_utils, widgets
    )
    from cellacdc.help import about
    from cellacdc.utils import concat as utilsConcat
    from cellacdc.utils import convert as utilsConvert
    from cellacdc.utils import rename as utilsRename
    from cellacdc.utils import align as utilsAlign
    from cellacdc import is_win, is_linux
except ModuleNotFoundError as e:
    src_path = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.dirname(src_path)
    print('----------------------------------------')
    print(e)
    print(
        'Cellacdc NOT INSTALLED. '
        'Run the following command to install: '
        f'pip install -e "{main_path}"'
    )
    print('----------------------------------------')
    exit('Execution aborted due to an error. See above for details.')



if os.name == 'nt':
    try:
        # Set taskbar icon in windows
        import ctypes
        myappid = 'schmollerlab.cellacdc.pyqt.v1' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        pass

class mainWin(QMainWindow):
    def __init__(self, app, parent=None):
        self.app = app
        self.welcomeGuide = None
        super().__init__(parent)
        self.setWindowTitle("Cell-ACDC")
        self.setWindowIcon(QIcon(":assign-motherbud.svg"))

        if not is_linux:
            self.loadFonts()

        self.createActions()
        self.createMenuBar()
        self.connectActions()

        mainContainer = QtGui.QWidget()
        self.setCentralWidget(mainContainer)

        mainLayout = QVBoxLayout()
        mainLayout.addStretch()

        welcomeLabel = QLabel('Welcome to Cell-ACDC!')
        welcomeLabel.setAlignment(Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPixelSize(16)
        font.setBold(True)
        font.setFamily('Ubuntu')
        welcomeLabel.setFont(font)
        # padding: top, left, bottom, right
        welcomeLabel.setStyleSheet("padding:0px 0px 5px 0px;")
        mainLayout.addWidget(welcomeLabel)

        label = QLabel(
            'Press any of the following buttons\n'
            'to launch the respective module')

        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPixelSize(13)
        font.setFamily('Ubuntu')
        label.setFont(font)
        # padding: top, left, bottom, right
        label.setStyleSheet("padding:0px 0px 10px 0px;")
        mainLayout.addWidget(label)

        mainLayout.addStretch()

        dataStructButton = QPushButton(
            '  0. Create data structure from microscopy file(s)...  '
        )
        font = QtGui.QFont()
        font.setPixelSize(13)
        dataStructButton.setFont(font)
        dataStructButton.clicked.connect(self.launchDataStruct)
        self.dataStructButton = dataStructButton
        mainLayout.addWidget(dataStructButton)

        dataPrepButton = QPushButton('1. Launch data prep module...')
        font = QtGui.QFont()
        font.setPixelSize(13)
        dataPrepButton.setFont(font)
        dataPrepButton.clicked.connect(self.launchDataPrep)
        self.dataPrepButton = dataPrepButton
        mainLayout.addWidget(dataPrepButton)

        segmButton = QPushButton('2. Launch segmentation module...')
        segmButton.setFont(font)
        segmButton.clicked.connect(self.launchSegm)
        self.segmButton = segmButton
        mainLayout.addWidget(segmButton)

        guiButton = QPushButton('3. Launch GUI...')
        guiButton.setFont(font)
        guiButton.clicked.connect(self.launchGui)
        self.guiButton = guiButton
        mainLayout.addWidget(guiButton)

        font = QtGui.QFont()
        font.setPixelSize(13)

        closeLayout = QHBoxLayout()
        restartButton = QPushButton(
            QIcon(":reload.svg"),
            '  Restart Cell-ACDC'
        )
        restartButton.setFont(font)
        restartButton.clicked.connect(self.close)
        self.restartButton = restartButton
        closeLayout.addWidget(restartButton)

        closeButton = QPushButton(QIcon(":exit.png"), '  Exit')
        self.closeButton = closeButton
        # closeButton.setIconSize(QSize(24,24))
        closeButton.setFont(font)
        closeButton.clicked.connect(self.close)
        closeLayout.addWidget(closeButton)

        mainLayout.addLayout(closeLayout)
        mainContainer.setLayout(mainLayout)

        self.start_JVM = True

        self.guiWin = None
        self.dataPrepWin = None
        self._version = None

    def setVersion(self, version):
        self._version = version

    def loadFonts(self):
        font = QtGui.QFont()
        font.setFamily('Ubuntu')
        QFontDatabase.addApplicationFont(":Ubuntu-Regular.ttf")
        QFontDatabase.addApplicationFont(":Ubuntu-Bold.ttf")
        QFontDatabase.addApplicationFont(":Ubuntu-Italic.ttf")
        QFontDatabase.addApplicationFont(":Ubuntu-BoldItalic.ttf")
        QFontDatabase.addApplicationFont(":Calibri-Regular.ttf")
        QFontDatabase.addApplicationFont(":Calibri-Bold.ttf")
        QFontDatabase.addApplicationFont(":Calibri-Italic.ttf")
        QFontDatabase.addApplicationFont(":Calibri-BoldItalic.ttf")
        QFontDatabase.addApplicationFont(":ArialMT-Regular.ttf")
        QFontDatabase.addApplicationFont(":ArialMT-Bold.otf")
        QFontDatabase.addApplicationFont(":ArialMT-Italic.otf")
        QFontDatabase.addApplicationFont(":ArialMT-BoldItalic.otf")

    def launchWelcomeGuide(self, checked=False):
        cellacdc_path = os.path.dirname(os.path.realpath(__file__))
        temp_path = os.path.join(cellacdc_path, 'temp')
        csv_path = os.path.join(temp_path, 'settings.csv')
        self.settings_csv_path = csv_path
        if not os.path.exists(csv_path):
            idx = ['showWelcomeGuide']
            values = ['Yes']
            self.df_settings = pd.DataFrame({'setting': idx,
                                             'value': values}
                                           ).set_index('setting')
            self.df_settings.to_csv(csv_path)
        self.df_settings = pd.read_csv(csv_path, index_col='setting')
        if 'showWelcomeGuide' not in self.df_settings.index:
            self.df_settings.at['showWelcomeGuide', 'value'] = 'Yes'
            self.df_settings.to_csv(csv_path)

        show = (
            self.df_settings.at['showWelcomeGuide', 'value'] == 'Yes'
            or self.sender() is not None
        )
        if not show:
            return

        self.welcomeGuide = help.welcome.welcomeWin(mainWin=self)
        self.welcomeGuide.showAndSetSize()
        self.welcomeGuide.showPage(self.welcomeGuide.welcomeItem)

    def setColorsAndText(self):
        self.moduleLaunchedColor = '#ead935'
        defaultColor = self.guiButton.palette().button().color().name()
        self.defaultPushButtonColor = defaultColor
        self.defaultTextDataStructButton = self.dataStructButton.text()
        self.defaultTextGuiButton = self.guiButton.text()
        self.defaultTextDataPrepButton = self.dataPrepButton.text()
        self.defaultTextSegmButton = self.segmButton.text()

    def createMenuBar(self):
        menuBar = self.menuBar()

        utilsMenu = QMenu("&Utilities", self)
        utilsMenu.addAction(self.concatAcdcDfsAction)
        utilsMenu.addAction(self.npzToNpyAction)
        utilsMenu.addAction(self.npzToTiffAction)
        utilsMenu.addAction(self.TiffToNpzAction)
        utilsMenu.addAction(self.h5ToNpzAction)
        utilsMenu.addAction(self.alignAction)
        utilsMenu.addAction(self.renameAction)
        menuBar.addMenu(utilsMenu)

        helpMenu = QMenu("&Help", self)
        helpMenu.addAction(self.welcomeGuideAction)
        helpMenu.addAction(self.userManualAction)
        helpMenu.addAction(self.aboutAction)
        helpMenu.addAction(self.citeAction)
        helpMenu.addAction(self.contributeAction)

        menuBar.addMenu(helpMenu)

    def createActions(self):
        self.npzToNpyAction = QAction('Convert .npz file(s) to .npy...')
        self.npzToTiffAction = QAction('Convert .npz file(s) to .tif...')
        self.TiffToNpzAction = QAction('Convert .tif file(s) to _segm.npz...')
        self.h5ToNpzAction = QAction('Convert .h5 file(s) to _segm.npz...')
        # self.TiffToHDFAction = QAction('Convert .tif file(s) to .h5py...')
        self.concatAcdcDfsAction = QAction(
            'Concatenate acdc output tables from multiple Positions...'
        )
        self.renameAction = QAction('Rename files by appending additional text...')
        self.alignAction = QAction('Align or revert alignment...')

        self.welcomeGuideAction = QAction('Welcome Guide')
        self.userManualAction = QAction('User manual...')
        self.aboutAction = QAction('About Cell-ACDC')
        self.citeAction = QAction('Cite us...')
        self.contributeAction = QAction('Contribute...')

    def connectActions(self):
        self.alignAction.triggered.connect(self.launchAlignUtil)
        self.concatAcdcDfsAction.triggered.connect(self.launchConcatUtil)
        self.npzToNpyAction.triggered.connect(self.launchConvertFormatUtil)
        self.npzToTiffAction.triggered.connect(self.launchConvertFormatUtil)
        self.TiffToNpzAction.triggered.connect(self.launchConvertFormatUtil)
        self.h5ToNpzAction.triggered.connect(self.launchConvertFormatUtil)
        self.welcomeGuideAction.triggered.connect(self.launchWelcomeGuide)
        self.aboutAction.triggered.connect(self.showAbout)
        self.renameAction.triggered.connect(self.launchRenameUtil)
        self.userManualAction.triggered.connect(myutils.showUserManual)
        self.contributeAction.triggered.connect(self.showContribute)
        self.citeAction.triggered.connect(
            partial(QDesktopServices.openUrl, QUrl(cite_url))
        )

    def showContribute(self):
        self.launchWelcomeGuide()
        self.welcomeGuide.showPage(self.welcomeGuide.contributeItem)

    def showAbout(self):
        self.aboutWin = about.QDialogAbout(parent=self)
        self.aboutWin.show()

    def launchRenameUtil(self):
        isUtilnabled = self.sender().isEnabled()
        if isUtilnabled:
            self.sender().setDisabled(True)
            self.renameWin = utilsRename.renameFilesWin(
                parent=self,
                actionToEnable=self.sender(),
                mainWin=self
            )
            self.renameWin.show()
            self.renameWin.main()
        else:
            self.renameWin.setWindowState(Qt.WindowActive)
            self.renameWin.raise_()

    def launchConvertFormatUtil(self, checked=False):
        s = self.sender().text()
        m = re.findall(r'Convert \.(\w+) file\(s\) to (.*)\.(\w+)...', s)
        from_, info, to = m[0]
        isConvertEnabled = self.sender().isEnabled()
        if isConvertEnabled:
            self.sender().setDisabled(True)
            self.convertWin = utilsConvert.convertFileFormatWin(
                parent=self,
                actionToEnable=self.sender(),
                mainWin=self, from_=from_, to=to,
                info=info
            )
            self.convertWin.show()
            self.convertWin.main()
        else:
            # self.convertWin.setWindowState(Qt.WindowNoState)
            self.convertWin.setWindowState(Qt.WindowActive)
            self.convertWin.raise_()

    def launchDataStruct(self, checked=False):
        self.dataStructButton.setStyleSheet(
            f'QPushButton {{background-color: {self.moduleLaunchedColor};}}'
        )
        self.dataStructButton.setText(
            '0. Creating data structure running...'
        )
        # self.dataStructButton.setDisabled(True)

        QTimer.singleShot(100, self._showDataStructWin)

    # def attemptDataStructSeparateProcess(self):
    #     self.dataStructButton.setStyleSheet(
    #         f'QPushButton {{background-color: {self.moduleLaunchedColor};}}'
    #     )
    #     self.dataStructButton.setText(
    #         '0. Creating data structure running...'
    #     )
    #
    #     cellacdc_path = os.path.dirname(os.path.realpath(__file__))
    #     dataStruct_path = os.path.join(cellacdc_path, 'dataStruct.py')
    #
    #     # Due to javabridge limitation only one 'start_vm' can be called in
    #     # each process. To get around with this every data structure conversion
    #     # is launched in a separate process
    #     try:
    #         subprocess.run(
    #             [sys.executable, dataStruct_path], check=True, text=True,
    #             shell=False
    #         )
    #     except Exception as e:
    #         print('=========================================')
    #         traceback.print_exc()
    #         print('=========================================')
    #         err = ("""
    #         <p style="font-size:12px">
    #             Launching data structure module in a separate process failed.<br><br>
    #             Please restart Cell-ACDC if you need to use this module again.
    #         <p>
    #         """)
    #         self.dataStructButton.setStyleSheet(
    #             f'QPushButton {{background-color: {self.defaultPushButtonColor};}}')
    #         self.dataStructButton.setText(
    #             '0. Restart Cell-ACDC to enable module 0 again.')
    #         self.dataStructButton.setToolTip(
    #             'Due to an interal limitation of the Java Virtual Machine\n'
    #             'moduel 0 can be launched only once.\n'
    #             'To use it again close and reopen Cell-ACDC'
    #         )
    #         self.dataStructButton.setDisabled(True)
    #         return
    #
    #     self.dataStructButton.setStyleSheet(
    #         f'QPushButton {{background-color: {self.defaultPushButtonColor};}}')
    #     self.dataStructButton.setText(
    #         '0. Create data structure from microscopy file(s)...')
    #     self.dataStructButton.setDisabled(False)

    def _showDataStructWin(self):
        if self.dataStructButton.isEnabled():
            self.dataStructButton.setText(
                '0. Restart Cell-ACDC to enable module 0 again.')
            self.dataStructButton.setToolTip(
                'Due to an interal limitation of the Java Virtual Machine\n'
                'moduel 0 can be launched only once.\n'
                'To use it again close and reopen Cell-ACDC'
            )
            self.dataStructButton.setDisabled(True)
            self.dataStructWin = dataStruct.createDataStructWin(parent=self)
            self.dataStructWin.show()
            self.dataStructWin.main()


    def launchDataPrep(self, checked=False):
        c = self.dataPrepButton.palette().button().color().name()
        launchedColor = self.moduleLaunchedColor
        defaultColor = self.defaultPushButtonColor
        defaultText = self.defaultTextDataPrepButton
        if c != self.moduleLaunchedColor:
            self.dataPrepButton.setStyleSheet(
                f'QPushButton {{background-color: {launchedColor};}}')
            self.dataPrepButton.setText(
                'DataPrep is running. Click to restore window.'
            )
            self.dataPrepWin = dataPrep.dataPrepWin(
                buttonToRestore=(self.dataPrepButton, defaultColor, defaultText),
                mainWin=self
            )
            self.dataPrepWin.show()
        else:
            # self.dataPrepWin.setWindowState(Qt.WindowNoState)
            self.dataPrepWin.setWindowState(Qt.WindowActive)
            self.dataPrepWin.raise_()

    def launchSegm(self, checked=False):
        c = self.segmButton.palette().button().color().name()
        launchedColor = self.moduleLaunchedColor
        defaultColor = self.defaultPushButtonColor
        defaultText = self.defaultTextSegmButton
        if c != self.moduleLaunchedColor:
            self.segmButton.setStyleSheet(
                f'QPushButton {{background-color: {launchedColor};}}')
            self.segmButton.setText('Segmentation is running. '
                                    'Check progress in the terminal/console')
            self.segmWin = segm.segmWin(
                buttonToRestore=(self.segmButton, defaultColor, defaultText),
                mainWin=self
            )
            self.segmWin.show()
            self.segmWin.main()
        else:
            # self.segmWin.setWindowState(Qt.WindowNoState)
            self.segmWin.setWindowState(Qt.WindowActive)
            self.segmWin.raise_()


    def launchGui(self, checked=False):
        c = self.guiButton.palette().button().color().name()
        launchedColor = self.moduleLaunchedColor
        defaultColor = self.defaultPushButtonColor
        defaultText = self.defaultTextGuiButton
        if c.lower() != launchedColor.lower():
            print('Opening GUI...')
            self.guiButton.setStyleSheet(
                f'QPushButton {{background-color: {launchedColor};}}')
            self.guiButton.setText('GUI is running. Click to restore window.')
            self.guiWin = gui.guiWin(
                self.app,
                buttonToRestore=(self.guiButton, defaultColor, defaultText),
                mainWin=self, version=self._version
            )
            self.guiWin.show()
        else:
            # self.guiWin.setWindowState(Qt.WindowNoState)
            self.guiWin.setWindowState(Qt.WindowActive)
            self.guiWin.raise_()

    def guiClosed(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.deleteGuiReference)
        self.timer.start(100)

    def deleteGuiReference(self):
        try:
            self.guiWin.isVisible()
        except RuntimeError:
            self.timer.stop()

    def launchAlignUtil(self, checked=False):
        if self.alignAction.isEnabled():
            self.alignAction.setDisabled(True)
            self.alignWin = utilsAlign.alignWin(
                parent=self,
                actionToEnable=self.alignAction,
                mainWin=self
            )
            self.alignWin.show()
            self.alignWin.main()
        else:
            # self.concatWin.setWindowState(Qt.WindowNoState)
            self.alignWin.setWindowState(Qt.WindowActive)
            self.alignWin.raise_()


    def launchConcatUtil(self, checked=False):
        isConcatEnabled = self.concatAcdcDfsAction.isEnabled()
        if isConcatEnabled:
            self.concatAcdcDfsAction.setDisabled(True)
            self.concatWin = utilsConcat.concatWin(
                parent=self,
                actionToEnable=self.concatAcdcDfsAction,
                mainWin=self
            )
            self.concatWin.show()
            self.concatWin.main()
        else:
            # self.concatWin.setWindowState(Qt.WindowNoState)
            self.concatWin.setWindowState(Qt.WindowActive)
            self.concatWin.raise_()

    def show(self):
        QMainWindow.show(self)
        h = self.dataPrepButton.geometry().height()
        self.dataStructButton.setMinimumHeight(h*2)
        self.dataPrepButton.setMinimumHeight(h*2)
        self.segmButton.setMinimumHeight(h*2)
        self.guiButton.setMinimumHeight(h*2)
        self.restartButton.setMinimumHeight(int(h*2))
        self.closeButton.setMinimumHeight(int(h*2))
        iconWidth = int(self.closeButton.iconSize().width()*1.3)
        self.closeButton.setIconSize(QSize(iconWidth, iconWidth))
        self.setColorsAndText()
        self.readSettings()

    def saveWindowGeometry(self):
        settings = QSettings('schmollerlab', 'acdc_main')
        settings.setValue("geometry", self.saveGeometry())

    def readSettings(self):
        settings = QSettings('schmollerlab', 'acdc_main')
        if settings.value('geometry') is not None:
            self.restoreGeometry(settings.value("geometry"))

    def checkOpenModules(self):
        c1 = self.dataPrepButton.palette().button().color().name()
        c2 = self.segmButton.palette().button().color().name()
        c3 = self.guiButton.palette().button().color().name()
        launchedColor = self.moduleLaunchedColor

        openModules = []
        if c1 == launchedColor:
            openModules.append(self.dataPrepWin)
        if c2 == launchedColor:
            openModules.append(self.segmWin)
        if c3 == launchedColor:
            openModules.append(self.guiWin)

        if not openModules:
            return True, openModules

        msg = widgets.myMessageBox()
        warn_txt = html_utils.paragraph(
            'There are still <b>other Cell-ACDC windows open</b>.<br><br>'
            'Are you sure you want to close everything?'
        )
        _, yesButton = msg.warning(
           self, 'Modules still open!', warn_txt, buttonsTexts=('Cancel', 'Yes')
        )

        return msg.clickedButton == yesButton, openModules

    def closeEvent(self, event):
        if self.welcomeGuide is not None:
            self.welcomeGuide.close()

        self.saveWindowGeometry()

        acceptClose, openModules = self.checkOpenModules()
        if acceptClose:
            for openModule in openModules:
                openModule.setWindowState(Qt.WindowActive)
                openModule.raise_()
                openModule.close()
                if openModule.isVisible():
                    event.ignore()
                    return
        else:
            event.ignore()
            return

        if self.sender() == self.restartButton:
            print('Restarting Cell-ACDC...')
            try:
                if is_win:
                    os.execv(sys.argv[0], sys.argv)
                    exit()
                else:
                    os.execv(sys.executable, ['python'] + sys.argv)
            except Exception as e:
                traceback.print_exc()
                print('-----------------------------------------')
                print('Failed to restart Cell-ACDC. Please restart manually')
        else:
            print('**********************************************')
            print('Cell-ACDC closed. Have a good day!')
            print('**********************************************')
            exit()

def run():
    from cellacdc.config import parser_args
    print('Launching application...')
    # Handle high resolution displays:
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Create the application
    app = QApplication([])

    app.setStyle(QStyleFactory.create('Fusion'))
    app.setWindowIcon(QIcon(":assign-motherbud.svg"))
    win = mainWin(app)
    version = myutils.read_version()
    win.setVersion(version)
    win.show()
    win.launchWelcomeGuide()
    try:
        win.welcomeGuide.showPage(win.welcomeGuide.welcomeItem)
    except AttributeError:
        pass
    print('**********************************************')
    print(f'Welcome to Cell-ACDC v{version}!')
    print('**********************************************')
    print('----------------------------------------------')
    print('NOTE: If application is not visible, it is probably minimized\n'
          'or behind some other open window.')
    print('----------------------------------------------')
    # win.raise_()
    sys.exit(app.exec_())

def main():
    # Keep compatibility with users that installed older versions
    # when the entry point was main()
    run()

if __name__ == "__main__":
    run()
