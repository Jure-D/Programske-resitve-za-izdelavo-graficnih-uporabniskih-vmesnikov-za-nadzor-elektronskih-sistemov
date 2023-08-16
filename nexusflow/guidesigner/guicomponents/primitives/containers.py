from typing import Optional
from PySide6.QtWidgets import QGroupBox, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel


class Container(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def add_widget(self, widget: QWidget, row: int, column: int, row_span: int = 1, column_span: int = 1) -> None:
        """Adds a widget to the container.

        :param widget: The widget to add to the container.
        :type widget: QWidget
        :param row: The row to add the widget to.
        :type row: int
        :param column: The column to add the widget to.
        :type column: int
        :param row_span: The number of rows the widget should span.
        :type row_span: int
        :param column_span: The number of columns the widget should span.
        :type column_span: int
        """
        self.layout.addWidget(widget, row, column, row_span, column_span)

    def add_labeled_widget(self, label: str, widget: QWidget, row: int, column: int, row_span: int = 1, column_span: int = 1) -> None:
        """Adds a widget to the container.

        :param label: The label to display next to the widget.
        :type label: str
        :param widget: The widget to add to the container.
        :type widget: QWidget
        :param row: The row to add the widget to.
        :type row: int
        :param column: The column to add the widget to.
        :type column: int
        :param row_span: The number of rows the widget should span.
        :type row_span: int
        :param column_span: The number of columns the widget should span.
        :type column_span: int
        """
        label_widget = QLabel(label)
        self.layout.addWidget(label_widget, row, column)
        self.layout.addWidget(widget, row, column + 1, row_span, column_span)


class GroupContainer(QGroupBox):
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent=parent)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def add_widget(self, widget: QWidget, row: int, column: int, row_span: int = 1, column_span: int = 1) -> None:
        """Adds a widget to the container.

        :param widget: The widget to add to the container.
        :type widget: QWidget
        :param row: The row to add the widget to.
        :type row: int
        :param column: The column to add the widget to.
        :type column: int
        :param row_span: The number of rows the widget should span.
        :type row_span: int
        :param column_span: The number of columns the widget should span.
        :type column_span: int
        """
        self.layout.addWidget(widget, row, column, row_span, column_span)


class LinearContainer(QWidget):
    def __init__(self, layout: str, parent=None):
        """A container widget that is used to hold other widgets.

        :param layout: The layout type to use for the container. Can be "vertical" or "horizontal".
        :type layout: str
        ...
        :raises ValueError: Raised if an invalid layout type is passed.
        """
        super().__init__(parent=parent)
        if layout is None:
            self.layout = None
        elif layout == "vertical":
            self.layout = QVBoxLayout()
        elif layout == "horizontal":
            self.layout = QHBoxLayout()
        else:
            raise ValueError(f"Invalid layout type: {layout}")

        self.setLayout(self.layout)

    def change_layout(self, layout: str) -> None:
        """Changes the layout of the container.

        :param layout: The layout type to use for the container. Can be "vertical" or "horizontal".
        :type layout: str
        ...
        :raises ValueError: Raised if an invalid layout type is passed.
        """
        if layout == "vertical":
            self.layout.deleteLater()
            self.layout = QVBoxLayout()
        elif layout == "horizontal":
            self.layout.deleteLater()
            self.layout = QHBoxLayout()
        else:
            raise ValueError(f"Invalid layout type: {layout}")

        self.setLayout(self.layout)

    def add_widget(self, widget: QWidget) -> None:
        """Adds a widget to the container.

        :param widget: The widget to add to the container.
        :type widget: QWidget
        """
        self.layout.addWidget(widget)


# class GridContainer(QWidget):
#     def __init__(self, parent=None):
#         """A container widget that is used to hold other widgets.
#
#         ...
#         :raises ValueError: Raised if an invalid layout type is passed.
#         """
#         super().__init__(parent=parent)
#         self.layout = QGridLayout()
#         self.setLayout(self.layout)
#
#     def add_widget(self, widget: QWidget, row: int, column: int, row_span: int = 1, column_span: int = 1) -> None:
#         """Adds a widget to the container.
#
#         :param widget: The widget to add to the container.
#         :type widget: QWidget
#         :param row: The row to add the widget to.
#         :type row: int
#         :param column: The column to add the widget to.
#         :type column: int
#         :param row_span: The number of rows the widget should span.
#         :type row_span: int
#         :param column_span: The number of columns the widget should span.
#         :type column_span: int
#         """
#         self.layout.addWidget(widget, row, column, row_span, column_span)
#
#     def add_setting(self, label_text: str, editing_widget: QWidget, row: int, column: int) -> None:
#         """Adds a setting to the container.
#
#         :param label_text: The text to display on the label.
#         :type label_text: str
#         :param editing_widget: The widget to add to the container.
#         :type editing_widget: QWidget
#         :param row: The row to add the widget to.
#         :type row: int
#         :param column: The column to add the widget to.
#         :type column: int
#         :param row_span: The number of rows the widget should span.
#         :type row_span: int
#         :param column_span: The number of columns the widget should span.
#         :type column_span: int
#         """
#         label = QLabel(label_text)
#         label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
#         self.layout.addWidget(label, row, 0)
#         self.layout.addWidget(editing_widget, row, 1)


class GroupContainer(QGroupBox):
    def __init__(self, title: str, layout: str, parent=None):
        """A group box widget that is used to hold other widgets.

        :param title: The title of the group box.
        :type title: str
        :param layout: The layout type to use for the container. Can be "vertical" or "horizontal".
        :type layout: str
        ...
        :raises ValueError: Raised if an invalid layout type is passed.
        """
        super().__init__(parent=parent)

        self.setTitle(title)

        if layout == "vertical":
            self.layout = QVBoxLayout()
        elif layout == "horizontal":
            self.layout = QHBoxLayout()
        else:
            raise ValueError(f"Invalid layout type: {layout}")

        self.setLayout(self.layout)
