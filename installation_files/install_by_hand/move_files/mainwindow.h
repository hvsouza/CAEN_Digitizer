#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <string>
#include <vector>
namespace Ui {
class MainWindow;
}

const int channels = 8;
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    bool move_data_file(int run, int subrun, double voltage, double threshold, std::string triggerCh, std::string extra, std::string primary, std::string file_type);
    bool move_data_file_style2(int run, int subrun, std::string block1, std::string block2, std::string extra, std::string primary, std::string file_type);

    bool move_calibration_file(int run, int subrun, double voltage, double threshold, std::string triggerCh, std::string extra, std::string primary, std::string file_type);

    std::string folder_name(int run, int subrun, double voltage, double threshold, std::string triggerCh);
    std::string changeVoltage(double voltage);
    bool checkSpaces(std::string var);

private slots:
    void on_pushButton_2_clicked();
    void on_pushButton_4_clicked();

    void on_button_movefile_clicked();
    void on_button_movefile_5_clicked();

    void on_button_movefile_2_clicked();

    //void on_radioButton_2_clicked(bool checked);

    void on_lock_folder_clicked(bool checked);

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
