from typing import Text
from PySide6.QtCore import QAbstractListModel
from PySide6.QtGui import QFontMetrics, QColor, QPalette
from PySide6.QtWidgets import QStyledItemDelegate, QListView

def rgb(r, g, b): return "#{:02x}{:02x}{:02x}".format(r, g, b)


class Delegate(QStyledItemDelegate):
    LIGHT = QColor(rgb(79, 113, 147))
    DARK = QColor(rgb(20, 36, 43))
    FORE = QColor(rgb(234, 183, 78))

    def getFontMetrics(self, option): return QFontMetrics(option.font)

    def textRect(self, text, font):
        fontMetrics = QFontMetrics(font)
        boundingRect = fontMetrics.boundingRect(str(text))
        boundingRect.adjust(0, 0, 1, 1)

        return boundingRect
    
    def paint(self, painter, option, index): ...
    
    def sizeHint(self, option, index): ...

    def item(self, index):
        model = index.model()
        return model.data(index)


class ListModel(QAbstractListModel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects = []
    
    def rowCount(self, index=None): return len(self._objects)

    def addObject(self, obj):
        self._objects.append(obj)
        self.layoutChanged.emit()
    
    def data(self, index, role=0):
        row = index.row()
        if row < self.rowCount(): return self._objects[row]
    
    def clear(self):
        self._objects = []
        self.layoutChanged.emit()



class ListView(QListView):
    delegateClass = Delegate
    modelClass = ListModel
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self._delegate = self.delegateClass(self)
        self._model = self.modelClass(self)

        self.setItemDelegate(self._delegate)
        self.setModel(self._model)
        self.setResizeMode(QListView.Adjust)
        self.setWordWrap(True)
    
    def addObject(self, obj):
        self._model.addObject(obj)
    
    def clear(self): self.model().clear()


# PyQt5.QtCore.QPointF(232.0, 0.0) PyQt5.QtCore.QPointF(247.0, 0.0) PyQt5.QtCore.QPointF(237.0, 10.0)



