from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import QTimer
from ui.widgets.tree_frame import TreeFrame
from core.variables_manager import VariablesManager
from core.observer_manager import ObserverManager, NotificationTypes

class TreeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.variablesManager = VariablesManager()
        self.observerManager = ObserverManager.getInstance()
        self.observerManager.addObserver(self)
        self.visibleFrames = 0
        self.minimumSquareSize = int(self.variablesManager.minScreenSize/2.26)  # Taille minimum fixe pour les frames
        
        # Créer les frames en fonction du paramètre combo
        self.treeFrames = []
        locked = self.variablesManager.getConfig("locked")
        if locked is not None:
            for lock in locked:
                self.treeFrames.append(TreeFrame(self.minimumSquareSize,lock))
            remaining_frames = 3 - len(locked)
        else:
            locked = []
            remaining_frames = 3
        for _ in range(remaining_frames):
            self.treeFrames.append(TreeFrame(self.minimumSquareSize))
        # Cache pour la dernière taille calculée et debouncing
        self.lastCalculatedSize = None
        self.resizeTimer = QTimer()
        self.resizeTimer.setSingleShot(True)
        self.resizeTimer.setInterval(150)  # Délai de 150ms pour debounce
        self.resizeTimer.timeout.connect(self._performResize)
        self.pendingSize = None
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QGridLayout()
        # Réduire les marges au minimum
        self.mainLayout.setContentsMargins(2, 2, 2, 2)
        self.mainLayout.setSpacing(2)  # Réduire l'espacement entre les frames
        self.setLayout(self.mainLayout)
        self.doResize()  # Appeler do_resize après l'initialisation de l'interface utilisateur


    def resizeEvent(self, event):
        _ = event  # Variable utilisée pour éviter l'avertissement
        # Sauvegarder la nouvelle taille
        self.variablesManager.setConfig(
            "windowSize",
            {
                "width": int(self.size().width() * self.variablesManager.dpi),
                "height": int(self.size().height() * self.variablesManager.dpi)
            }
        )
        # Utiliser debouncing pour éviter les recalculs trop fréquents
        self.pendingSize = self.size()
        self.resizeTimer.start()

    def _performResize(self):
        """Méthode interne pour effectuer le redimensionnement après debouncing"""
        if self.pendingSize is not None:
            self.doResize()
            self.pendingSize = None

    def doResize(self):
        size = self.size()
        width = size.width()
        height = size.height()
        
        # Éviter les recalculs inutiles avec cache
        current_size_key = (width, height, self.variablesManager.getConfig("maxTrees"))
        if self.lastCalculatedSize == current_size_key:
            return
        
        self.lastCalculatedSize = current_size_key
        
        # Calcul du nombre optimal de frames
        max_trees = self.variablesManager.getConfig("maxTrees")
        if max_trees is None:
            max_trees = 3
        optimalFrameCount = min(
            max_trees,
            max(1, width // self.minimumSquareSize)
        )
        # Recalculer la taille des frames
        availableWidth = width - (optimalFrameCount + 1) * 2
        widthPerFrame = availableWidth // optimalFrameCount
        squareSize = min(widthPerFrame, height - int(40 / self.variablesManager.dpi))  # Ajuster pour les marges en fonction du DPI
        
        # Mise à jour des frames
        if optimalFrameCount != self.visibleFrames:
            # Nettoyer le layout existant
            for i in reversed(range(self.mainLayout.count())):
                item = self.mainLayout.itemAt(i)
                if item is not None:
                    widget = item.widget()
                    if widget is not None:
                        widget.hide()
                    self.mainLayout.removeItem(item)
            
            # Ajouter les nouveaux frames
            for i in range(optimalFrameCount):
                frame = self.treeFrames[i]
                self.mainLayout.addWidget(frame, 0, i)
                frame.resizeFrame(squareSize, squareSize)
                frame.show()
            
            self.visibleFrames = optimalFrameCount
        else:
            for i in range(optimalFrameCount):
                self.treeFrames[i].resizeFrame(squareSize, squareSize)

    def notify(self, notification_type=NotificationTypes.ALL):
        if notification_type == NotificationTypes.MAXTREES or notification_type == NotificationTypes.ALL:
            self.doResize()


