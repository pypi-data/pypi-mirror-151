# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source/stats_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_statsWindow(object):
    def setupUi(self, statsWindow):
        statsWindow.setObjectName("statsWindow")
        statsWindow.resize(1089, 779)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(statsWindow)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.scrollArea = QtWidgets.QScrollArea(statsWindow)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, -175, 1054, 1140))
        self.scrollAreaWidgetContents_2.setMinimumSize(QtCore.QSize(950, 1140))
        self.scrollAreaWidgetContents_2.setStyleSheet("")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.labelStatistics = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatistics.sizePolicy().hasHeightForWidth())
        self.labelStatistics.setSizePolicy(sizePolicy)
        self.labelStatistics.setMinimumSize(QtCore.QSize(0, 80))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.labelStatistics.setFont(font)
        self.labelStatistics.setObjectName("labelStatistics")
        self.verticalLayout_4.addWidget(self.labelStatistics)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.labelTodayScore = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTodayScore.sizePolicy().hasHeightForWidth())
        self.labelTodayScore.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setItalic(True)
        self.labelTodayScore.setFont(font)
        self.labelTodayScore.setObjectName("labelTodayScore")
        self.gridLayout.addWidget(self.labelTodayScore, 0, 2, 1, 1)
        self.labelAllTimeScore = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAllTimeScore.sizePolicy().hasHeightForWidth())
        self.labelAllTimeScore.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setItalic(True)
        self.labelAllTimeScore.setFont(font)
        self.labelAllTimeScore.setObjectName("labelAllTimeScore")
        self.gridLayout.addWidget(self.labelAllTimeScore, 2, 2, 1, 1)
        self.labelToday = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelToday.sizePolicy().hasHeightForWidth())
        self.labelToday.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.labelToday.setFont(font)
        self.labelToday.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelToday.setObjectName("labelToday")
        self.gridLayout.addWidget(self.labelToday, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 3, 1, 1)
        self.labelAllTIme = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAllTIme.sizePolicy().hasHeightForWidth())
        self.labelAllTIme.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.labelAllTIme.setFont(font)
        self.labelAllTIme.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelAllTIme.setObjectName("labelAllTIme")
        self.gridLayout.addWidget(self.labelAllTIme, 2, 0, 1, 1)
        self.labelDaysAgo = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDaysAgo.sizePolicy().hasHeightForWidth())
        self.labelDaysAgo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setItalic(True)
        self.labelDaysAgo.setFont(font)
        self.labelDaysAgo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelDaysAgo.setObjectName("labelDaysAgo")
        self.gridLayout.addWidget(self.labelDaysAgo, 2, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem5, 1, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        spacerItem6 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem6)
        self.graphView = PlotWidget(self.scrollAreaWidgetContents_2)
        self.graphView.setMinimumSize(QtCore.QSize(900, 350))
        self.graphView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.graphView.setObjectName("graphView")
        self.verticalLayout_4.addWidget(self.graphView)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_4.addItem(spacerItem7)
        self.labelResetTitle = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelResetTitle.sizePolicy().hasHeightForWidth())
        self.labelResetTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(False)
        font.setWeight(50)
        self.labelResetTitle.setFont(font)
        self.labelResetTitle.setStyleSheet("")
        self.labelResetTitle.setObjectName("labelResetTitle")
        self.verticalLayout_4.addWidget(self.labelResetTitle)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8, 0, 1, 1, 1)
        self.buttonResetAllTime = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonResetAllTime.sizePolicy().hasHeightForWidth())
        self.buttonResetAllTime.setSizePolicy(sizePolicy)
        self.buttonResetAllTime.setMinimumSize(QtCore.QSize(0, 40))
        self.buttonResetAllTime.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonResetAllTime.setAutoDefault(True)
        self.buttonResetAllTime.setObjectName("buttonResetAllTime")
        self.gridLayout_2.addWidget(self.buttonResetAllTime, 0, 0, 1, 1)
        self.buttonResetDaily = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonResetDaily.sizePolicy().hasHeightForWidth())
        self.buttonResetDaily.setSizePolicy(sizePolicy)
        self.buttonResetDaily.setMinimumSize(QtCore.QSize(0, 40))
        self.buttonResetDaily.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonResetDaily.setAutoDefault(True)
        self.buttonResetDaily.setObjectName("buttonResetDaily")
        self.gridLayout_2.addWidget(self.buttonResetDaily, 1, 0, 1, 1)
        self.buttonResetAll = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonResetAll.sizePolicy().hasHeightForWidth())
        self.buttonResetAll.setSizePolicy(sizePolicy)
        self.buttonResetAll.setMinimumSize(QtCore.QSize(0, 40))
        self.buttonResetAll.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonResetAll.setAutoDefault(True)
        self.buttonResetAll.setObjectName("buttonResetAll")
        self.gridLayout_2.addWidget(self.buttonResetAll, 2, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        spacerItem9 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem9)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonMainMenu = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonMainMenu.sizePolicy().hasHeightForWidth())
        self.buttonMainMenu.setSizePolicy(sizePolicy)
        self.buttonMainMenu.setMinimumSize(QtCore.QSize(0, 40))
        self.buttonMainMenu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonMainMenu.setAutoDefault(True)
        self.buttonMainMenu.setDefault(True)
        self.buttonMainMenu.setObjectName("buttonMainMenu")
        self.horizontalLayout.addWidget(self.buttonMainMenu)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem10)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        spacerItem11 = QtWidgets.QSpacerItem(18, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem11)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        spacerItem12 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem12)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_4.addWidget(self.scrollArea)

        self.retranslateUi(statsWindow)
        QtCore.QMetaObject.connectSlotsByName(statsWindow)

    def retranslateUi(self, statsWindow):
        _translate = QtCore.QCoreApplication.translate
        statsWindow.setWindowTitle(_translate("statsWindow", "Stats"))
        self.labelStatistics.setText(_translate("statsWindow", "Statistics"))
        self.labelTodayScore.setText(_translate("statsWindow", "0 WPM"))
        self.labelAllTimeScore.setText(_translate("statsWindow", "0 WPM"))
        self.labelToday.setText(_translate("statsWindow", "Today"))
        self.labelAllTIme.setText(_translate("statsWindow", "All-time "))
        self.labelDaysAgo.setText(_translate("statsWindow", "- 0 days ago"))
        self.labelResetTitle.setText(_translate("statsWindow", "Reset Highscores"))
        self.buttonResetAllTime.setText(_translate("statsWindow", "All-time"))
        self.buttonResetDaily.setText(_translate("statsWindow", "Today\'s"))
        self.buttonResetAll.setText(_translate("statsWindow", "All"))
        self.buttonMainMenu.setText(_translate("statsWindow", "Back"))
from pyqtgraph import PlotWidget
