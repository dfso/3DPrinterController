import sys

from PyQt6 import QtWidgets, QtCore

import ui, serial_tool, threads_r_w


class App():
    
    device = None
    read_thread = None
    write_thread = None

    def __init__(self) -> None:
        self.window = ui.MainWindow()

        self.find_ports()

        self.window.aboutAction.triggered.connect(self.about)
        self.window.exitAction.triggered.connect(self.close_app)
        self.window.reloadAction.triggered.connect(self.find_ports)
        self.window.connectAction.triggered.connect(self.connect)
        self.window.disconnectAction.triggered.connect(self.disconnect)
        self.window.cmd_input.returnPressed.connect(lambda: self.send_command(self.window.cmd_input.text()))
        self.window.btn_home_xy.clicked.connect(lambda: self.go_home(''))
        self.window.btn_home_z.clicked.connect(lambda: self.go_home('z'))

    def find_ports(self):
        self.window.combo_portas.clear()
        self.window.combo_portas.addItems(serial_tool.SerialTool.listar_portas())

    def connect(self):
        self.device = serial_tool.SerialTool.conectar(
            self.window.combo_portas.currentText(),
            self.window.combo_baunds.currentText()
        )
        if self.device.is_open:
            self.window.gbox_jog.setEnabled(True)
            self.window.cmd_input.setEnabled(True)
            self.window.disconnectAction.setEnabled(True)
            self.window.connectAction.setDisabled(True)
            self.window.reloadAction.setDisabled(True)
            self.window.status_port.setText('<font color=green><b>online</b></font>')

            self.read_thread = threads_r_w.ReadThread(self.device)
            self.read_thread.signal.connect(self.window.text_log.append)
            self.read_thread.start()

    def send_command(self, cmd):
        if self.device:
            self.write_thread = threads_r_w.WriteThread(self.device, cmd.upper())
            self.write_thread.start()
            self.window.text_log.append(f'<font color=green><b>Comando: {cmd.upper()}</b></font>')

    def go_home(self, axis):
        #g28 ; home all axes
        self.send_command(f'g28 {axis}')

    def get_position(self):
        #Hosts should respond to the output of M114 by updating their current position
        self.send_command('m114')

    def disconnect(self):
        if self.read_thread:
            if self.read_thread.isRunning():
                self.read_thread.stop_work()
        if self.write_thread:
            self.write_thread.stop_work()
        if self.device:
            self.device.close()

        self.window.status_port.setText('<font color=red>offline</font>')
        self.window.gbox_jog.setDisabled(True)
        self.window.cmd_input.setDisabled(True)
        self.window.disconnectAction.setDisabled(True)
        self.window.connectAction.setDisabled(True)
        self.window.reloadAction.setDisabled(True)
        self.window.connectAction.setEnabled(True)
        self.window.reloadAction.setEnabled(True)

    def close_app(self):
        self.disconnect()
        self.window.close()

    def about(self):
        pyqt_version = QtCore.PYQT_VERSION_STR
        autor = 'dfso'
        sw_version = '1.03.23'
        github = 'https://github.com/dfso'
        icons_source = 'https://fonts.google.com/icons'

        msg = f'''
            <p>Um controlador para sua impressora 3D</p>
            <br>
            <p>versão: {sw_version}</p>
            <p>versão pyqt: {pyqt_version}</p>
            <p>github: {github}</p>
            <p>ícones: {icons_source}</p>
            <p>autor: {autor}</p>
        '''
        QtWidgets.QMessageBox.about(self.window, 'sobre...', msg)


app = QtWidgets.QApplication(sys.argv)
my_app = App()
sys.exit(app.exec())
