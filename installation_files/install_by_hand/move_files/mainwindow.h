#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <string>
#include <vector>
#include <QCheckBox>
#include <fstream>

namespace Ui {
class MainWindow;
}

const int channels = 8;
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    void disabletriggers();

    ~MainWindow();

private:
    bool move_data_file(int run, int subrun, double voltage, double threshold, std::string triggerCh, std::string extra, std::string primary, std::string file_type);
    bool move_data_file_style2(int run, int subrun, std::string block1, std::string block2, std::string extra, std::string primary, std::string file_type);

    bool move_calibration_file(int run, int subrun, double voltage, double threshold, std::string triggerCh, std::string extra, std::string primary, std::string file_type);

    std::string folder_name();
    std::string folder_name2();

    std::string changeVoltage(double voltage);
    bool checkSpaces(std::string var);
    int getFactor();
    void writeConfigFile(bool extra);
    void save_config_file(std::string folder);


private slots:
    void on_pushButton_2_clicked();
    void on_pushButton_4_clicked();

    void on_button_movefile_clicked();
    void on_button_movefile_5_clicked();

    void on_button_movefile_2_clicked();

    //void on_radioButton_2_clicked(bool checked);

    void on_pushButtonRecompile_clicked();

    void on_lock_folder_clicked(bool checked);

    void enable_and_trigger(bool checked, QCheckBox* myt);
    void setEnabledTrigger(QCheckBox *myt);
    void setDisabledTrigger(QCheckBox *myt);
    void on_externaltrigger_clicked(bool checked);



    void on_enable1_clicked(bool checked);
    void on_enable2_clicked(bool checked);
    void on_enable3_clicked(bool checked);
    void on_enable4_clicked(bool checked);
    void on_enable5_clicked(bool checked);
    void on_enable6_clicked(bool checked);
    void on_enable7_clicked(bool checked);
    void on_enable8_clicked(bool checked);



    void on_FileTypeSet_currentTextChanged(const QString &arg1);

    void on_pushButton_SetConfig_clicked();

    void on_button_save_config_2_clicked();

    void on_button_save_config_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
