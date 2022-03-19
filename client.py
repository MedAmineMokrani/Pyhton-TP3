from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys
import webbrowser


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 400)
        self.label1 = QLabel("Enter your host IP:", self)
        self.text = QLineEdit(self)
        self.text.move(10, 30)
        self.label2 = QLabel("API KEY:", self)
        self.label2.move(10, 60)
        self.text2 = QLineEdit(self)
        self.text2.move(10, 80)
        self.label3 = QLabel("IP ADRESSE:", self)
        self.label3.move(10, 110)
        self.text3 = QLineEdit(self)
        self.text3.move(10, 140)
        self.label4 = QLabel("Details :", self)
        self.label4.move(10, 170)
        self.label5 = QLabel("Lien :", self)
        self.label5.move(10, 180)
        self.button = QPushButton("Send", self)
        self.button.move(10, 200)

        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def on_click(self):
        hostname = self.text.text()
        apikey = self.text2.text()
        ip = self.text3.text()

        if hostname == "":
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.sendrequest(hostname,apikey,ip)
            if res:
                lat = res["Latitude"]
                lon = res["Longitude"]
             
                openstreetmap = "https://www.openstreetmap.org/?mlat=%s" % (lat) + "&mlon=%s" % lon
                self.label4.setText("Details :" "Latitude%s " % lat + "Longitude%s " % lon)
                self.label4.adjustSize()
                self.show()
                self.label5.setText("Lien :" + openstreetmap)
                self.label5.adjustSize()
                self.show()
                webbrowser.open(openstreetmap)
                

    def __query(self, hostname):
        url = "http://%s" % (hostname)
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()
        
    def sendrequest(self, hostname,apikey,ip):
        url = "http://%s" % (hostname) + "/ip/%s" % ip + "?key=%s" % apikey
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()
        
        
     


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()
   