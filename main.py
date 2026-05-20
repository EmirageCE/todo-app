import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget,
    QListWidgetItem, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt

SAVE_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

STYLE = """
    QMainWindow {
        background-color: #f0f4f8;
    }

    QWidget#central {
        background-color: #f0f4f8;
        font-family: Segoe UI;
        font-size: 13px;
    }

    QLineEdit {
        border: 2px solid #c0cfe0;
        border-radius: 6px;
        padding: 6px 10px;
        background-color: white;
        color: #1a1a1a;
        font-size: 13px;
        font-family: Segoe UI;
    }
    QLineEdit:focus {
        border-color: #4a90d9;
    }

    QPushButton {
        background-color: #4a90d9;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 7px 14px;
        font-size: 13px;
        font-family: Segoe UI;
    }
    QPushButton:hover {
        background-color: #357abd;
    }
    QPushButton:pressed {
        background-color: #2a6099;
    }

    QPushButton#delete_btn {
        background-color: #e05c5c;
    }
    QPushButton#delete_btn:hover {
        background-color: #c04444;
    }
    QPushButton#delete_btn:pressed {
        background-color: #a33535;
    }

    QListWidget {
        border: 2px solid #c0cfe0;
        border-radius: 6px;
        background-color: white;
        padding: 4px;
        font-size: 13px;
        font-family: Segoe UI;
        color: #1a1a1a;
        outline: none;
    }
    QListWidget::item {
        padding: 8px 6px;
        border-radius: 4px;
        color: #1a1a1a;
        background-color: white;
    }
    QListWidget::item:hover {
        background-color: #eef4fc;
    }
    QListWidget::item:selected {
        background-color: #dce9f7;
        color: #1a1a1a;
    }

    QLabel {
        color: #555555;
        font-size: 12px;
        font-family: Segoe UI;
        background-color: transparent;
    }
"""


class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setMinimumSize(400, 520)

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(16, 16, 16, 16)
        central.setLayout(main_layout)

        title = QLabel("Görev Listesi")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; background-color: transparent;")
        main_layout.addWidget(title)

        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Yeni görev gir...")
        self.task_input.returnPressed.connect(self.add_task)

        add_btn = QPushButton("Ekle")
        add_btn.clicked.connect(lambda: self.add_task())

        input_layout.addWidget(self.task_input)
        input_layout.addWidget(add_btn)

        self.task_list = QListWidget()
        self.task_list.itemChanged.connect(self.update_counter)

        btn_layout = QHBoxLayout()
        delete_btn = QPushButton("Seçili görevi sil")
        delete_btn.setObjectName("delete_btn")
        delete_btn.clicked.connect(self.delete_task)
        btn_layout.addWidget(delete_btn)

        self.counter_label = QLabel("0/0 tamamlandı")

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.task_list)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.counter_label)

        self.load_tasks()

    def add_task(self, text=None, checked=False):
        if text is None:
            text = self.task_input.text().strip()
        if not text:
            return

        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        item.setCheckState(state)
        self.task_list.addItem(item)

        self.task_input.clear()
        self.update_counter()
        self.save_tasks()

    def delete_task(self):
        selected = self.task_list.currentItem()
        if selected is None:
            QMessageBox.warning(self, "Uyarı", "Silmek için bir görev seç.")
            return
        row = self.task_list.row(selected)
        self.task_list.takeItem(row)
        self.update_counter()
        self.save_tasks()

    def update_counter(self):
        total = self.task_list.count()
        done = sum(
            1 for i in range(total)
            if self.task_list.item(i).checkState() == Qt.CheckState.Checked
        )
        self.counter_label.setText(f"{done}/{total} tamamlandı")
        self.save_tasks()

    def save_tasks(self):
        tasks = []
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            tasks.append({
                "text": item.text(),
                "done": item.checkState() == Qt.CheckState.Checked
            })
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

    def load_tasks(self):
        if not os.path.exists(SAVE_FILE):
            return
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        for task in tasks:
            self.add_task(text=task["text"], checked=task["done"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())