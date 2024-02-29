import cv2
import numpy as np
import pyautogui
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QIcon

class ZoomIn(QWidget):
    exit_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.scale_factor = 1 #default scale factor
        self.zoom_increment = .5 #zoom increment for each step.
        
        
    def update_magnifier(self):
        #this updates the magnifier everytime a button is pressed.
        mouse_x, mouse_y = pyautogui.position()
        
        #capture the screen
        screen = pyautogui.screenshot()
    
        #convert the screenshot to a numpy array
        frame = np.array(screen)
        
        #calculate the region to magnify (so getting the area around the mouse location)
        magnify_x1, magnify_y1 = max(0, mouse_x - 70), max(0, mouse_y - 100)
        magnify_x2, magnify_y2 = min(frame.shape[1], mouse_x + 60), min(frame.shape[0], mouse_y + 40)
        
        #magnify the region
        magnified_frame = frame[magnify_y1:magnify_y2, magnify_x1:magnify_x2]
        magnified_frame = cv2.resize(magnified_frame, (0, 0), fx=self.scale_factor, fy=self.scale_factor)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.zoom_in()
        elif event.key() == Qt.Key_Minus:
            self.zoom_out()
    
    def zoom_in(self):
        """method for zooming out"""
        self.scale_factor = min(self.scale_factor + self.zoom_increment, 5) 
        self.update()
        
    def zoom_out(self):
        """method for zooming in"""
        self.scale_factor = max(2.5, self.scale_factor - self.zoom_increment)
        self.update()
        
    def closeEvent(self, event):
        self.exit_signal.emit()

        
    pass

if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    zoomer = ZoomIn()
    
    #Connect the exit singal to the QApplication quit method
    zoomer.exit_signal.connect(app.quit)
    
    sys.exit(app.exec_())