# -*- coding: utf-8 -*-

import sys
import unittest
import gc
import PyQt5
from PyQt5.QtWidgets import QApplication, QMenu
from PyQt5.QtCore import QLocale
from cutecoin.gui.mainwindow import MainWindow
from cutecoin.core.app import Application

# Qapplication cause a core dumped when re-run in setup
# set it as global var
qapplication = QApplication(sys.argv)


class MainWindowMenusTest(unittest.TestCase):
    def setUp(self):
        QLocale.setDefault(QLocale("en_GB"))
#         self.application = Application(sys.argv, qapplication)
#         self.main_window = MainWindow(self.application)
#
#     def tearDown(self):
#         # delete all top widgets from main QApplication
#         lw = qapplication.topLevelWidgets()
#         for w in lw:
#             del w
#         gc.collect()
#
#     def test_menubar(self):
#         children = self.main_window.menubar.children()
#         menus = []
#         """:type: list[QMenu]"""
#         for child in children:
#             if isinstance(child, QMenu):
#                 menus.append(child)
#         self.assertEqual(len(menus), 3)
#         self.assertEqual(menus[0].objectName(), 'menu_account')
#         self.assertEqual(menus[1].objectName(), 'menu_contacts')
#         self.assertEqual(menus[2].objectName(), 'menu_actions')
#
#     def test_menu_account(self):
#         actions = self.main_window.menu_account.actions()
#         """:type: list[QAction]"""
#         self.assertEqual(len(actions), 10)
#         self.assertEqual(actions[0].objectName(), 'action_add_account')
#         self.assertEqual(actions[2].objectName(), 'action_configure_parameters')
#         self.assertEqual(actions[3].objectName(), 'action_set_as_default')
#         self.assertEqual(actions[5].objectName(), 'action_export')
#         self.assertEqual(actions[6].objectName(), 'action_import')
#         self.assertEqual(actions[8].objectName(), 'actionAbout')
#         self.assertEqual(actions[9].objectName(), 'action_quit')
#
#     def test_menu_contacts(self):
#         actions = self.main_window.menu_contacts.actions()
#         """:type: list[QAction]"""
#         self.assertEqual(len(actions), 3)
#         self.assertEqual(actions[1].objectName(), 'action_add_a_contact')
#
#     def test_menu_actions(self):
#         actions = self.main_window.menu_actions.actions()
#         """:type: list[QAction]"""
#         self.assertEqual(len(actions), 2)
#         self.assertEqual(actions[0].objectName(), 'actionTransfer_money')
#         self.assertEqual(actions[1].objectName(), 'actionCertification')
    def test_ignoreme(self):
        return

if __name__ == '__main__':
    unittest.main()
