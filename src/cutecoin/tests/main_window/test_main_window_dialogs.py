# -*- coding: utf-8 -*-

import sys
import unittest
import gc
import PyQt5
from PyQt5.QtWidgets import QApplication, QMenu
from PyQt5.QtCore import QLocale, QTimer
from cutecoin.gui.mainwindow import MainWindow
from cutecoin.core.app import Application

# Qapplication cause a core dumped when re-run in setup
# set it as global var
qapplication = QApplication(sys.argv)


class MainWindowDialogsTest(unittest.TestCase):
    def setUp(self):
        QLocale.setDefault(QLocale("en_GB"))
        self.application = Application(sys.argv)
        self.main_window = MainWindow(self.application)
        print()
        widgets = qapplication.topLevelWidgets()
        for widget in widgets:
            print(widget.objectName())

    def tearDown(self):
        print('teardown')
        self.main_window.close()
        self.main_window.destroy(True, True)
        del self.main_window
        qapplication.closeAllWindows()

    # def test_action_about(self):
    #     # select menu
    #     self.main_window.actionAbout.trigger()
    #     widgets = qapplication.topLevelWidgets()
    #     for widget in widgets:
    #         if isinstance(widget, PyQt5.QtWidgets.QDialog):
    #             self.assertEqual(widget.objectName(), 'AboutPopup')
    #             self.assertEqual(widget.isVisible(), True)
    #             widget.close()
    #             break

    def test_action_add_account(self):
        # asynchronous test, cause dialog is waiting user response
        QTimer.singleShot(0, self._async_test_action_add_account)
        # select menu
        self.main_window.action_add_account.trigger()

    def _async_test_action_add_account(self):
        print('timer add')
        widgets = qapplication.topLevelWidgets()
        for widget in widgets:
            if isinstance(widget, PyQt5.QtWidgets.QDialog) and widget.objectName() == 'AccountConfigurationDialog':
                print(widget.objectName())
                self.assertEqual(widget.isVisible(), True)
                widget.disconnect()
                widget.close()
                widget.destroy()
                break

    # # fixme: require a app.current_account fixture
    # # def test_action_configure_account(self):
    # #     # asynchronous test, cause dialog is waiting user response
    # #     QTimer.singleShot(0, self._async_test_action_configure_account)
    # #     # select about menu
    # #     self.main_window.action_configure_parameters.trigger()
    # #
    # # def _async_test_action_configure_account(self):
    # #     widgets = qapplication.topLevelWidgets()
    # #     for widget in widgets:
    # #         if isinstance(widget, PyQt5.QtWidgets.QDialog):
    # #             self.assertEqual(widget.objectName(), 'AccountConfigurationDialog')
    # #             self.assertEqual(widget.isVisible(), True)
    # #             widget.close()
    # #             break
    #
    # def test_action_export_account(self):
    #     # select menu
    #     self.main_window.action_export.trigger()
    #
    #     widgets = qapplication.topLevelWidgets()
    #     for widget in widgets:
    #         if isinstance(widget, PyQt5.QtWidgets.QFileDialog):
    #             self.assertEqual(widget.objectName(), 'ExportFileDialog')
    #             self.assertTrue(widget.isVisible())
    #             widget.close()
    #             break

    # fixme: i am tstuck here... impossible to close dialog if another test was done before...???!!!
    def test_action_import_account(self):
        # asynchronous test, cause dialog is waiting user response
        QTimer.singleShot(0, self._async_test_action_import_account)
        # select menu
        self.main_window.action_import.trigger()

    def _async_test_action_import_account(self):
        print('timer')
        widgets = qapplication.topLevelWidgets()
        for widget in widgets:
            if isinstance(widget, PyQt5.QtWidgets.QDialog) and widget.objectName() == 'ImportAccountDialog':
                print(widget.objectName())
                self.assertEqual(widget.isVisible(), True)
                widget.disconnect()
                widget.close()
                widget.destroy()
                break

if __name__ == '__main__':
    unittest.main()
