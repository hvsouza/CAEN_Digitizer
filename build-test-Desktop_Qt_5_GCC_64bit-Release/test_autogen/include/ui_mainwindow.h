/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.2.4
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QLineEdit *primary_name;
    QTabWidget *tabWidget;
    QWidget *tab;
    QLabel *label_3;
    QLineEdit *run;
    QLineEdit *voltage;
    QPushButton *button_movefile;
    QLabel *label;
    QLineEdit *subrun;
    QPushButton *pushButton_2;
    QLineEdit *threshold;
    QLabel *label_6;
    QLabel *label_2;
    QLabel *label_5;
    QLabel *label_4;
    QLineEdit *extra;
    QLabel *label_7;
    QLabel *triggerCh;
    QLineEdit *trigger_channel;
    QRadioButton *calibration_check;
    QWidget *tab_2;
    QLineEdit *led_width;
    QLabel *LED_voltage;
    QLineEdit *led_voltage;
    QLabel *width;
    QLabel *label_8;
    QLabel *label_9;
    QPushButton *button_movefile_2;
    QTabWidget *tabWidget_2;
    QWidget *tab_3;
    QWidget *tab_4;
    QLabel *Information;
    QLineEdit *subrun_2;
    QLabel *label_11;
    QWidget *tab_5;
    QLineEdit *file_type;
    QLabel *file_type_2;
    QLabel *label_10;
    QRadioButton *lock_folder;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;
    QMenuBar *menuBar;
    QMenu *menuLAr_Test;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(385, 372);
        QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindow->sizePolicy().hasHeightForWidth());
        MainWindow->setSizePolicy(sizePolicy);
        MainWindow->setMinimumSize(QSize(385, 372));
        MainWindow->setMaximumSize(QSize(385, 372));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        primary_name = new QLineEdit(centralWidget);
        primary_name->setObjectName(QString::fromUtf8("primary_name"));
        primary_name->setEnabled(false);
        primary_name->setGeometry(QRect(161, 10, 211, 25));
        QSizePolicy sizePolicy1(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(primary_name->sizePolicy().hasHeightForWidth());
        primary_name->setSizePolicy(sizePolicy1);
        primary_name->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        primary_name->setReadOnly(false);
        tabWidget = new QTabWidget(centralWidget);
        tabWidget->setObjectName(QString::fromUtf8("tabWidget"));
        tabWidget->setEnabled(true);
        tabWidget->setGeometry(QRect(10, 50, 361, 251));
        tab = new QWidget();
        tab->setObjectName(QString::fromUtf8("tab"));
        label_3 = new QLabel(tab);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(24, 90, 67, 17));
        label_3->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        run = new QLineEdit(tab);
        run->setObjectName(QString::fromUtf8("run"));
        run->setGeometry(QRect(94, 30, 91, 21));
        run->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        run->setReadOnly(false);
        voltage = new QLineEdit(tab);
        voltage->setObjectName(QString::fromUtf8("voltage"));
        voltage->setGeometry(QRect(94, 90, 91, 21));
        voltage->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        button_movefile = new QPushButton(tab);
        button_movefile->setObjectName(QString::fromUtf8("button_movefile"));
        button_movefile->setGeometry(QRect(250, 50, 89, 25));
        label = new QLabel(tab);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(24, 30, 67, 17));
        label->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        subrun = new QLineEdit(tab);
        subrun->setObjectName(QString::fromUtf8("subrun"));
        subrun->setGeometry(QRect(94, 60, 91, 21));
        subrun->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        pushButton_2 = new QPushButton(tab);
        pushButton_2->setObjectName(QString::fromUtf8("pushButton_2"));
        pushButton_2->setGeometry(QRect(250, 140, 89, 25));
        QPalette palette;
        QBrush brush(QColor(239, 41, 41, 255));
        brush.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Button, brush);
        QBrush brush1(QColor(255, 51, 51, 255));
        brush1.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Light, brush1);
        QBrush brush2(QColor(229, 25, 25, 255));
        brush2.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Midlight, brush2);
        QBrush brush3(QColor(102, 0, 0, 255));
        brush3.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Dark, brush3);
        QBrush brush4(QColor(136, 0, 0, 255));
        brush4.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Mid, brush4);
        palette.setBrush(QPalette::Active, QPalette::Base, brush);
        palette.setBrush(QPalette::Active, QPalette::Window, brush);
        QBrush brush5(QColor(0, 0, 0, 255));
        brush5.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::Shadow, brush5);
        QBrush brush6(QColor(229, 127, 127, 255));
        brush6.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Active, QPalette::AlternateBase, brush6);
        palette.setBrush(QPalette::Inactive, QPalette::Button, brush);
        palette.setBrush(QPalette::Inactive, QPalette::Light, brush1);
        palette.setBrush(QPalette::Inactive, QPalette::Midlight, brush2);
        palette.setBrush(QPalette::Inactive, QPalette::Dark, brush3);
        palette.setBrush(QPalette::Inactive, QPalette::Mid, brush4);
        palette.setBrush(QPalette::Inactive, QPalette::Base, brush);
        palette.setBrush(QPalette::Inactive, QPalette::Window, brush);
        palette.setBrush(QPalette::Inactive, QPalette::Shadow, brush5);
        palette.setBrush(QPalette::Inactive, QPalette::AlternateBase, brush6);
        palette.setBrush(QPalette::Disabled, QPalette::Button, brush);
        palette.setBrush(QPalette::Disabled, QPalette::Light, brush1);
        palette.setBrush(QPalette::Disabled, QPalette::Midlight, brush2);
        palette.setBrush(QPalette::Disabled, QPalette::Dark, brush3);
        palette.setBrush(QPalette::Disabled, QPalette::Mid, brush4);
        palette.setBrush(QPalette::Disabled, QPalette::Base, brush);
        palette.setBrush(QPalette::Disabled, QPalette::Window, brush);
        palette.setBrush(QPalette::Disabled, QPalette::Shadow, brush5);
        QBrush brush7(QColor(204, 0, 0, 255));
        brush7.setStyle(Qt::SolidPattern);
        palette.setBrush(QPalette::Disabled, QPalette::AlternateBase, brush7);
        pushButton_2->setPalette(palette);
        pushButton_2->setAutoFillBackground(false);
        pushButton_2->setStyleSheet(QString::fromUtf8("background-color: rgb(239, 41, 41);\n"
""));
        pushButton_2->setAutoDefault(false);
        pushButton_2->setFlat(false);
        threshold = new QLineEdit(tab);
        threshold->setObjectName(QString::fromUtf8("threshold"));
        threshold->setGeometry(QRect(94, 120, 91, 21));
        threshold->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        label_6 = new QLabel(tab);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setGeometry(QRect(194, 120, 41, 16));
        label_2 = new QLabel(tab);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(24, 60, 67, 17));
        label_2->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        label_5 = new QLabel(tab);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setGeometry(QRect(194, 90, 16, 16));
        label_4 = new QLabel(tab);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setGeometry(QRect(10, 120, 81, 20));
        label_4->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        extra = new QLineEdit(tab);
        extra->setObjectName(QString::fromUtf8("extra"));
        extra->setGeometry(QRect(94, 180, 91, 21));
        extra->setStyleSheet(QString::fromUtf8(""));
        extra->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        label_7 = new QLabel(tab);
        label_7->setObjectName(QString::fromUtf8("label_7"));
        label_7->setGeometry(QRect(10, 180, 81, 20));
        label_7->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        triggerCh = new QLabel(tab);
        triggerCh->setObjectName(QString::fromUtf8("triggerCh"));
        triggerCh->setGeometry(QRect(10, 150, 81, 20));
        triggerCh->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        trigger_channel = new QLineEdit(tab);
        trigger_channel->setObjectName(QString::fromUtf8("trigger_channel"));
        trigger_channel->setGeometry(QRect(94, 150, 91, 21));
        trigger_channel->setStyleSheet(QString::fromUtf8(""));
        trigger_channel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        calibration_check = new QRadioButton(tab);
        calibration_check->setObjectName(QString::fromUtf8("calibration_check"));
        calibration_check->setGeometry(QRect(201, 180, 141, 23));
        calibration_check->setLayoutDirection(Qt::RightToLeft);
        tabWidget->addTab(tab, QString());
        tab_2 = new QWidget();
        tab_2->setObjectName(QString::fromUtf8("tab_2"));
        led_width = new QLineEdit(tab_2);
        led_width->setObjectName(QString::fromUtf8("led_width"));
        led_width->setGeometry(QRect(230, 50, 91, 21));
        led_width->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        LED_voltage = new QLabel(tab_2);
        LED_voltage->setObjectName(QString::fromUtf8("LED_voltage"));
        LED_voltage->setGeometry(QRect(126, 20, 101, 20));
        LED_voltage->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        led_voltage = new QLineEdit(tab_2);
        led_voltage->setObjectName(QString::fromUtf8("led_voltage"));
        led_voltage->setGeometry(QRect(230, 20, 91, 21));
        led_voltage->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        led_voltage->setReadOnly(false);
        width = new QLabel(tab_2);
        width->setObjectName(QString::fromUtf8("width"));
        width->setGeometry(QRect(136, 50, 91, 20));
        width->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        label_8 = new QLabel(tab_2);
        label_8->setObjectName(QString::fromUtf8("label_8"));
        label_8->setGeometry(QRect(330, 20, 16, 16));
        label_9 = new QLabel(tab_2);
        label_9->setObjectName(QString::fromUtf8("label_9"));
        label_9->setGeometry(QRect(330, 50, 16, 16));
        button_movefile_2 = new QPushButton(tab_2);
        button_movefile_2->setObjectName(QString::fromUtf8("button_movefile_2"));
        button_movefile_2->setGeometry(QRect(180, 120, 161, 25));
        tabWidget_2 = new QTabWidget(tab_2);
        tabWidget_2->setObjectName(QString::fromUtf8("tabWidget_2"));
        tabWidget_2->setGeometry(QRect(30, 250, 127, 80));
        tab_3 = new QWidget();
        tab_3->setObjectName(QString::fromUtf8("tab_3"));
        tabWidget_2->addTab(tab_3, QString());
        tab_4 = new QWidget();
        tab_4->setObjectName(QString::fromUtf8("tab_4"));
        tabWidget_2->addTab(tab_4, QString());
        Information = new QLabel(tab_2);
        Information->setObjectName(QString::fromUtf8("Information"));
        Information->setGeometry(QRect(10, 20, 141, 201));
        Information->setAutoFillBackground(false);
        Information->setTextFormat(Qt::AutoText);
        Information->setScaledContents(false);
        Information->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignTop);
        Information->setWordWrap(true);
        subrun_2 = new QLineEdit(tab_2);
        subrun_2->setObjectName(QString::fromUtf8("subrun_2"));
        subrun_2->setGeometry(QRect(230, 80, 91, 21));
        subrun_2->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        label_11 = new QLabel(tab_2);
        label_11->setObjectName(QString::fromUtf8("label_11"));
        label_11->setGeometry(QRect(160, 80, 67, 17));
        label_11->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        tabWidget->addTab(tab_2, QString());
        tab_5 = new QWidget();
        tab_5->setObjectName(QString::fromUtf8("tab_5"));
        file_type = new QLineEdit(tab_5);
        file_type->setObjectName(QString::fromUtf8("file_type"));
        file_type->setGeometry(QRect(284, 10, 61, 21));
        file_type->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        file_type->setReadOnly(false);
        file_type_2 = new QLabel(tab_5);
        file_type_2->setObjectName(QString::fromUtf8("file_type_2"));
        file_type_2->setGeometry(QRect(190, 10, 91, 20));
        file_type_2->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        tabWidget->addTab(tab_5, QString());
        label_10 = new QLabel(centralWidget);
        label_10->setObjectName(QString::fromUtf8("label_10"));
        label_10->setGeometry(QRect(60, 10, 91, 20));
        label_10->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        lock_folder = new QRadioButton(centralWidget);
        lock_folder->setObjectName(QString::fromUtf8("lock_folder"));
        lock_folder->setEnabled(true);
        lock_folder->setGeometry(QRect(310, 40, 61, 23));
        lock_folder->setCheckable(true);
        lock_folder->setChecked(true);
        lock_folder->setAutoExclusive(false);
        MainWindow->setCentralWidget(centralWidget);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        MainWindow->setStatusBar(statusBar);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 385, 20));
        menuLAr_Test = new QMenu(menuBar);
        menuLAr_Test->setObjectName(QString::fromUtf8("menuLAr_Test"));
        MainWindow->setMenuBar(menuBar);

        menuBar->addAction(menuLAr_Test->menuAction());

        retranslateUi(MainWindow);

        tabWidget->setCurrentIndex(0);
        pushButton_2->setDefault(false);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        primary_name->setText(QCoreApplication::translate("MainWindow", "new_data", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "Voltage:", nullptr));
        run->setText(QCoreApplication::translate("MainWindow", "0", nullptr));
        voltage->setText(QCoreApplication::translate("MainWindow", "42.3", nullptr));
        button_movefile->setText(QCoreApplication::translate("MainWindow", "Move files", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "Run:", nullptr));
        subrun->setText(QCoreApplication::translate("MainWindow", "0", nullptr));
        pushButton_2->setText(QCoreApplication::translate("MainWindow", "Finish run", nullptr));
        threshold->setText(QCoreApplication::translate("MainWindow", "20", nullptr));
        label_6->setText(QCoreApplication::translate("MainWindow", "ADC", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "subrun:", nullptr));
        label_5->setText(QCoreApplication::translate("MainWindow", "V", nullptr));
        label_4->setText(QCoreApplication::translate("MainWindow", "Threshold:", nullptr));
        extra->setText(QString());
        label_7->setText(QCoreApplication::translate("MainWindow", "Extra info:", nullptr));
        triggerCh->setText(QCoreApplication::translate("MainWindow", "Trigger Ch:", nullptr));
        trigger_channel->setText(QCoreApplication::translate("MainWindow", "Ch0", nullptr));
        calibration_check->setText(QCoreApplication::translate("MainWindow", "Calibration done", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(tab), QCoreApplication::translate("MainWindow", "Acquisition", nullptr));
        led_width->setText(QCoreApplication::translate("MainWindow", "100", nullptr));
        LED_voltage->setText(QCoreApplication::translate("MainWindow", "LED Voltage:", nullptr));
        led_voltage->setText(QCoreApplication::translate("MainWindow", "3", nullptr));
        width->setText(QCoreApplication::translate("MainWindow", "Width:", nullptr));
        label_8->setText(QCoreApplication::translate("MainWindow", "V", nullptr));
        label_9->setText(QCoreApplication::translate("MainWindow", "ns", nullptr));
        button_movefile_2->setText(QCoreApplication::translate("MainWindow", "Move Calibration files", nullptr));
        tabWidget_2->setTabText(tabWidget_2->indexOf(tab_3), QCoreApplication::translate("MainWindow", "Tab 1", nullptr));
        tabWidget_2->setTabText(tabWidget_2->indexOf(tab_4), QCoreApplication::translate("MainWindow", "Tab 2", nullptr));
        Information->setText(QCoreApplication::translate("MainWindow", "If you are running Calibration before data acquisition, make sure that the Acquisition tab have the correct informations", nullptr));
        subrun_2->setText(QCoreApplication::translate("MainWindow", "0", nullptr));
        label_11->setText(QCoreApplication::translate("MainWindow", "subrun:", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(tab_2), QCoreApplication::translate("MainWindow", "Calibration", nullptr));
        file_type->setText(QCoreApplication::translate("MainWindow", ".dat", nullptr));
        file_type_2->setText(QCoreApplication::translate("MainWindow", "File type:", nullptr));
        tabWidget->setTabText(tabWidget->indexOf(tab_5), QCoreApplication::translate("MainWindow", "More", nullptr));
        label_10->setText(QCoreApplication::translate("MainWindow", "Folder name:", nullptr));
        lock_folder->setText(QCoreApplication::translate("MainWindow", "Lock", nullptr));
        menuLAr_Test->setTitle(QCoreApplication::translate("MainWindow", "LAr Test", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
