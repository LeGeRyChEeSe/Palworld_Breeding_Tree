from PyQt6.QtWidgets import QMenu, QFileDialog
from PyQt6.QtGui import QGuiApplication, QAction, QPixmap, QPainter, QColor
from PyQt6.QtCore import QDir
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .tree_frame import TreeFrame
from core.variables_manager import VariablesManager
from core.tree_manager import TreeManager
from os import path
class PopupMenu(QMenu):
    def __init__(self, parent: Optional["TreeFrame"] = None):
        super().__init__(parent)
        self.tree_frame = parent  # Store typed reference
        self.variablesManager = VariablesManager()
        self.treeManager = TreeManager()
        self.copy = self.variablesManager.getText("copy")
        self.save = self.variablesManager.getText("save")
        self.tree = self.variablesManager.getText("tree")
        self.lock = self.variablesManager.getText("lock")
        self.unlock = self.variablesManager.getText("unlock")
        self.init_menu()
    def init_menu(self):
        copy_action = QAction(self.copy, self)
        copy_action.triggered.connect(self.copy_image)
        self.addAction(copy_action)

        save_action = QAction(self.save, self)
        save_action.triggered.connect(self.save_image)
        self.addAction(save_action)
        
        is_locked = self.tree_frame.locked if self.tree_frame is not None else False
        self.lock_action = QAction(self.unlock if is_locked else self.lock, self)
        self.lock_action.triggered.connect(self.lock_tree)
        self.addAction(self.lock_action)

    def copy_image(self):
        clipboard = QGuiApplication.clipboard()
        if clipboard is not None and self.tree_frame is not None and self.tree_frame.tree is not None:
            tree_pixmap = self.tree_frame.tree.pixmap()
            if tree_pixmap is not None:
                clipboard.setPixmap(self.addBackground(tree_pixmap), clipboard.Mode.Clipboard)
    def addBackground(self, pixmap: QPixmap):
        background = QPixmap(pixmap.size())
        background.fill(QColor(self.variablesManager.getColor("secondaryDarkColor")))
        painter = QPainter(background)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return background
    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, self.save, path.join(QDir.homePath(),self.tree), "Images (*.png)")
        if file_name:
            if self.tree_frame is not None and self.tree_frame.tree is not None:
                tree_pixmap = self.tree_frame.tree.pixmap()
                if tree_pixmap is not None:
                    tree_pixmap.save(file_name)

    def lock_tree(self):
        if self.tree_frame is not None:
            locked = not self.tree_frame.locked
            self.lock_action.setText(self.unlock if locked else self.lock)
            self.tree_frame.setLocked(locked)
        else:
            return
        if (self.tree_frame is not None and 
            self.tree_frame.parentChoice is not None and
            self.tree_frame.childChoice is not None):
            obj = {
                "parent": self.variablesManager.getPalByTranslation(self.tree_frame.parentChoice.currentText()),
                "child": self.variablesManager.getPalByTranslation(self.tree_frame.childChoice.currentText()),
                "number": self.tree_frame.which
            }
        else:
            return
        if locked:
            self.variablesManager.addLockedCombo(obj)
        else:
            self.variablesManager.removeLockedCombo(obj)