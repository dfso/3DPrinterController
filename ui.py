#<a target="_blank" href="https://icons8.com/icon/11997/close">Close</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>

from PyQt6 import QtCore, QtGui, QtWidgets

import resources

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('3D Printer Controller')

        self.resize(720, 600)

        self.centralize_window()

        self.make_actions()
        self.make_toolbar()
        self.make_menu()

        gbox_connection = QtWidgets.QGroupBox('Conexão')
        layout_conexao = QtWidgets.QFormLayout()
        self.combo_portas = QtWidgets.QComboBox()
        self.combo_portas.setMinimumWidth(150)
        layout_conexao.addRow('Portas', self.combo_portas)
        self.combo_baunds = QtWidgets.QComboBox()
        self.combo_baunds.addItems(['9600', '115200'])
        layout_conexao.addRow('Baund', self.combo_baunds)
        self.status_port = QtWidgets.QLabel('<font color = red>offline</font>')
        layout_conexao.addRow('Estado da porta', self.status_port)
        gbox_connection.setLayout(layout_conexao)

        center = QtCore.Qt.AlignmentFlag.AlignCenter
        self.gbox_jog = QtWidgets.QGroupBox('JOG')
        layout_jog = QtWidgets.QGridLayout()
        self.btn_home_xy = QtWidgets.QPushButton(QtGui.QIcon(':home.svg'), 'home')
        self.btn_home_z = QtWidgets.QPushButton(QtGui.QIcon(':home.svg'), 'home')
        self.btn_x_plus = QtWidgets.QPushButton(QtGui.QIcon(':right.svg'), 'x')
        self.btn_x_minus = QtWidgets.QPushButton(QtGui.QIcon(':left.svg'), 'x')
        self.btn_y_plus = QtWidgets.QPushButton(QtGui.QIcon(':up.svg'), 'y')
        self.btn_y_minus = QtWidgets.QPushButton(QtGui.QIcon(':down.svg'), 'y')
        self.btn_z_up = QtWidgets.QPushButton(QtGui.QIcon(':up.svg'), 'z')
        self.btn_z_down = QtWidgets.QPushButton(QtGui.QIcon(':down.svg'), 'z')
        layout_jog.addWidget(QtWidgets.QLabel('X/Y'), 0, 1, center)
        layout_jog.addWidget(QtWidgets.QLabel('Z'), 0, 4, center)
        layout_jog.addWidget(self.btn_y_plus, 1, 1)
        layout_jog.addWidget(self.btn_z_up, 1, 4)
        layout_jog.addWidget(self.btn_x_minus, 2, 0)
        layout_jog.addWidget(self.btn_home_xy, 2, 1)
        layout_jog.addWidget(self.btn_x_plus, 2, 2)
        layout_jog.addWidget(self.btn_home_z, 2, 4)
        layout_jog.addWidget(self.btn_y_minus, 3, 1)
        layout_jog.addWidget(self.btn_z_down, 3, 4)
        layout_jog.addWidget(QtWidgets.QLabel('mover'), 4, 0, center)
        layout_jog.addWidget(QtWidgets.QLabel('1mm'), 4, 1, center)
        layout_jog.addWidget(QtWidgets.QLabel('10mm'), 4, 2, center)
        self.gbox_jog.setLayout(layout_jog)

        gbox_position =QtWidgets.QGroupBox('Posição')
        layout_position = QtWidgets.QFormLayout()
        self.x_pos = QtWidgets.QLabel('...')
        self.y_pos = QtWidgets.QLabel('...')
        self.z_pos = QtWidgets.QLabel('...')
        layout_position.addRow('X', self.x_pos)
        layout_position.addRow('Y', self.y_pos)
        layout_position.addRow('Z', self.z_pos)
        gbox_position.setLayout(layout_position)

        layout_controles = QtWidgets.QHBoxLayout()
        layout_controles.addWidget(gbox_connection)
        layout_controles.addWidget(self.gbox_jog)
        layout_controles.addWidget(gbox_position)

        layout_cmd = QtWidgets.QFormLayout()
        self.cmd_input = QtWidgets.QLineEdit()
        layout_cmd.addRow('comando', self.cmd_input)

        root_layout = QtWidgets.QVBoxLayout()
        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setLayout(root_layout)

        root_layout.addLayout(layout_controles)
        root_layout.addLayout(layout_cmd)

        tab_log = QtWidgets.QTabWidget()
        log_tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout()
        self.text_log = QtWidgets.QTextEdit()
        self.text_log.setReadOnly(True)
        tab_layout.addWidget(self.text_log)
        log_tab.setLayout(tab_layout)
        tab_log.addTab(log_tab, 'log')
        
        root_layout.addWidget(tab_log)
       
        self.setMaximumSize(720, 600)

        self.disconnectAction.setDisabled(True)
        self.gbox_jog.setDisabled(True)
        self.cmd_input.setDisabled(True)

        self.show()

    def make_actions(self):
        self.exitAction = QtGui.QAction(QtGui.QIcon(':close.svg'), '&Sair', self)
        self.exitAction.setShortcut('Ctrl+q')

        self.aboutAction = QtGui.QAction(QtGui.QIcon(':about.svg'), '&Sobre...', self)
        self.aboutAction.setShortcut('F1')

        self.connectAction = QtGui.QAction(QtGui.QIcon(':connect.svg'), '&Conectar...', self)
        self.connectAction.setShortcut('F2')

        self.disconnectAction = QtGui.QAction(QtGui.QIcon(':disconnect.svg'), 'Descone&ctar...', self)
        self.disconnectAction.setShortcut('F3')

        self.reloadAction = QtGui.QAction(QtGui.QIcon(':reload.svg'), '&Recarregar portas...', self)
        self.reloadAction.setShortcut('F5')

    def make_menu(self):
        menubar = self.menuBar()

        menu_app = QtWidgets.QMenu('A&plicação', self)
        menu_app.addAction(self.exitAction)

        menu_actions = QtWidgets.QMenu('&Ações', self)
        menu_actions.addAction(self.connectAction)
        menu_actions.addAction(self.disconnectAction)
        menu_actions.addAction(self.reloadAction)

        menu_about = QtWidgets.QMenu('&Sobre...', self)
        menu_about.addAction(self.aboutAction)

        menubar.addMenu(menu_app)
        menubar.addMenu(menu_actions)
        menubar.addMenu(menu_about)

    def make_toolbar(self):
        toolbar = self.addToolBar('toolbar')
        toolbar.addAction(self.connectAction)
        toolbar.addAction(self.disconnectAction)
        toolbar.addAction(self.reloadAction)
        toolbar.addAction(self.aboutAction)
        toolbar.addAction(self.exitAction)

    def centralize_window(self):

        fg = self.frameGeometry()
        center = self.screen().availableGeometry().center()

        fg.moveCenter(center)
        self.move(fg.topLeft())
 
