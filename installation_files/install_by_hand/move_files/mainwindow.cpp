#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include <QLocale>
#include <locale.h>
#include <math.h>       /* round, floor, ceil, trunc */
#include <iostream>
MainWindow::MainWindow(QWidget *parent) :

    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    setlocale(LC_ALL, "C");
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_4_clicked()
{
    bool cali_status = ui->calibration_check_3->isChecked();
    int answer;
    if(cali_status){
        answer = QMessageBox::question(this,"","Finish this run?",QMessageBox::Yes,QMessageBox::No);
    }
    else{
        answer = QMessageBox::question(this,"","<b>Warning</b>: calibration might not exist.\nFinish run anyway?",QMessageBox::Yes,QMessageBox::No);
    }

    if(answer==QMessageBox::Yes){

        QMessageBox::about(this,"","New Run!");
        int runNo = std::stoi(ui->run_3->text().toStdString());
        runNo++;
        std::string newRun = std::to_string(runNo);

        ui->run_3->setText(QString::fromStdString(newRun));
        ui->subrun3->setText("0");
        ui->subrun_2->setText("0");

//        ui->calibration_check_3->setChecked(false);
    }

}

void MainWindow::on_pushButton_2_clicked()
{
    bool cali_status = ui->calibration_check->isChecked();
    int answer;
    if(cali_status){
        answer = QMessageBox::question(this,"","Finish this run?",QMessageBox::Yes,QMessageBox::No);
    }
    else{
        answer = QMessageBox::question(this,"","<b>Warning</b>: calibration might not exist.\nFinish run anyway?",QMessageBox::Yes,QMessageBox::No);
    }

    if(answer==QMessageBox::Yes){

        QMessageBox::about(this,"","New Run!");
        int runNo = std::stoi(ui->run->text().toStdString());
        runNo++;
        std::string newRun = std::to_string(runNo);

        ui->run->setText(QString::fromStdString(newRun));
        ui->subrun->setText("0");
        ui->subrun_2->setText("0");

       // ui->calibration_check->setChecked(false);
    }

}

void MainWindow::on_button_movefile_5_clicked()
{
    QMessageBox::about(this,"","File was moved, new subrun");

    // This take the necessary info to create the folder and files
    int runNo = std::stoi(ui->run_3->text().toStdString());
    int subRunNo = std::stoi(ui->subrun3->text().toStdString());
    std::string block1 = ui->block1->text().toStdString();
    std::string block2 = ui->block2->text().toStdString();
    std::string extra = ui->extra_3->text().toStdString();
    std::string primary = ui->primary_name->text().toStdString();
    std::string file_type = ui->file_type->text().toStdString();
    //

    // here we create the folder and the move the files
    move_data_file_style2(runNo,subRunNo,block1,block2,extra,primary,file_type);

    // update subrun number
    subRunNo++;
    std::string newSubRun = std::to_string(subRunNo);

    ui->subrun3->setText(QString::fromStdString(newSubRun));
}

void MainWindow::on_button_movefile_clicked()
{
    QMessageBox::about(this,"","File was moved, new subrun");

    // This take the necessary info to create the folder and files
    int runNo = std::stoi(ui->run->text().toStdString());
    int subRunNo = std::stoi(ui->subrun->text().toStdString());
    double voltage = std::stod(ui->voltage->text().toStdString());
    double threshold = std::stod(ui->threshold->text().toStdString());
    std::string triggerCh = ui->trigger_channel->text().toStdString();
    std::string extra = ui->extra->text().toStdString();
    std::string primary = ui->primary_name->text().toStdString();
    std::string file_type = ui->file_type->text().toStdString();
    //

    // here we create the folder and the move the files
    move_data_file(runNo,subRunNo,voltage,threshold,triggerCh,extra,primary,file_type);

    // update subrun number
    subRunNo++;
    std::string newSubRun = std::to_string(subRunNo);

    ui->subrun->setText(QString::fromStdString(newSubRun));
}

std::string MainWindow::folder_name(){
    // This take the necessary info to create the folder and files
    int run = std::stoi(ui->run->text().toStdString());
    double voltage = std::stod(ui->voltage->text().toStdString());
    double threshold = std::stod(ui->threshold->text().toStdString());
    std::string triggerCh = ui->trigger_channel->text().toStdString();

    std::string folder = "";
    std::string voltageS = changeVoltage(voltage);
    folder = "run" + std::to_string(run) + "_" + voltageS + "_" + std::to_string(static_cast<int>(threshold)) + "ADC_" + triggerCh + "/";
    return folder;
}



bool MainWindow::move_data_file(int run, int subrun, double voltage, double threshold, std::string triggerCh, std::string extra, std::string primary, std::string file_type)
{
    int out = 0;
    std::string mkdir = "mkdir -p ~/Documents/ADC_data/coldbox_data/" + primary + "/";
    out = system(mkdir.c_str());
    std::string folder = folder_name();

    std::vector<std::string> mvi(channels);
    for(int i = 0; i<channels; i++){
        mvi[i] = "mv -n ~/Desktop/WaveDumpData/wave" + std::to_string(i) + file_type +" ~/Documents/ADC_data/coldbox_data/" + primary + "/";
    }
    std::string voltageS = changeVoltage(voltage);

    //QMessageBox::about(this,"",QString::fromStdString(folder0));
    mkdir = mkdir+folder;
    for(int i = 0; i<channels; i++){
        mvi[i] = mvi[i] + folder;
    }
    // checking if there is no space in the extra
    char extraChar[extra.size()+1];
    strcpy(extraChar,extra.c_str());
    char c;
    int aux = 0;
    bool noSpace = true;
    while(extraChar[aux]){
         c = extraChar[aux];
         if(isspace(c)){
             noSpace = false;
         }
         aux++;
    }

    // checked

    for(int i = 0; i<channels; i++){
         mvi[i] = mvi[i] + std::to_string(subrun) + "_wave"+ std::to_string(i) + "_" + voltageS + "_" + std::to_string(static_cast<int>(threshold)) + "ADC_" + triggerCh;
    }
    if(extra!=""){
        if(noSpace){
            for(int i = 0; i<channels; i++){
                 mvi[i] = mvi[i] + "_" + extra;
            }
        }
        else{
            QMessageBox::about(this,"","Warning: extra has space");
            return false;
        }
    }
    for(int i = 0; i<channels; i++){
        mvi[i] = mvi[i]+file_type;
    }

    out = system(mkdir.c_str());

    bool enable_ch[8];
    enable_ch[0] = ui->enable1->isChecked();
    enable_ch[1] = ui->enable2->isChecked();
    enable_ch[2] = ui->enable3->isChecked();
    enable_ch[3] = ui->enable4->isChecked();
    enable_ch[4] = ui->enable5->isChecked();
    enable_ch[5] = ui->enable6->isChecked();
    enable_ch[6] = ui->enable7->isChecked();
    enable_ch[7] = ui->enable8->isChecked();

    //QMessageBox::about(this,"",QString::fromStdString(mv0));
    for(int i = 0; i<channels; i++){
        //std::cout << mvi[i] << std::endl;
        if(enable_ch[i]) out = system(mvi[i].c_str());
    }

    return true;

}
bool MainWindow::checkSpaces(std::string var){
    // checking if there is no space in the extra
    if(var=="") return true;
    char varChar[var.size()+1];
    strcpy(varChar,var.c_str());
    char c;
    int aux = 0;
    bool noSpace = true;
    while(varChar[aux]){
         c = varChar[aux];
         if(isspace(c)){
             noSpace = false;
         }
         aux++;
    }

    return noSpace;
}

std::string MainWindow::folder_name2(){

    std::string folder = "";
    int run = std::stoi(ui->run_3->text().toStdString());
    std::string block1 = ui->block1->text().toStdString();
    std::string block2 = ui->block2->text().toStdString();
    std::string extra = ui->extra_3->text().toStdString();


    bool noSpaceB1 = checkSpaces(block1);
    bool noSpaceB2 = checkSpaces(block2);
    bool noSpace = checkSpaces(extra);

    folder = "run" + std::to_string(run);

    if(!noSpaceB1){
        QMessageBox::about(this,"","Warning: block1 has space");
        return "false";
    }
    if(!noSpaceB2){
        QMessageBox::about(this,"","Warning: block2 has space");
        return "false";
    }
    if(!noSpace){
        QMessageBox::about(this,"","Warning: extra has space");
        return "false";
    }

     if(block1!=""){
         folder = folder + "_" + block1;
     }
     if(block2!=""){
         folder = folder + "_" + block2;
     }
     folder = folder + "/";
     return folder;
}

bool MainWindow::move_data_file_style2(int run, int subrun, std::string block1, std::string block2, std::string extra, std::string primary, std::string file_type)
{
    int out = 0;
    std::string mkdir = "mkdir -p ~/Documents/ADC_data/coldbox_data/" + primary + "/";
    out = system(mkdir.c_str());

    std::string folder = folder_name2();
    if(folder=="false") return false;


    std::vector<std::string> mvi(channels);
    for(int i = 0; i<channels; i++){
        mvi[i] = "mv -n ~/Desktop/WaveDumpData/wave" + std::to_string(i) + file_type +" ~/Documents/ADC_data/coldbox_data/" + primary + "/";
    }

    //QMessageBox::about(this,"",QString::fromStdString(folder0));
    mkdir = mkdir+folder;
    for(int i = 0; i<channels; i++){
        mvi[i] = mvi[i] + folder;
    }

    for(int i = 0; i<channels; i++){
         mvi[i] = mvi[i] + std::to_string(subrun) + "_wave"+ std::to_string(i);
         if(block1!=""){
             mvi[i] = mvi[i] + "_" + block1;
         }
         if(block2!=""){
             mvi[i] = mvi[i] + "_" + block2;
         }
    }
    if(extra!=""){
        for(int i = 0; i<channels; i++){
            mvi[i] = mvi[i] + "_" + extra;
        }

    }
    for(int i = 0; i<channels; i++){
        mvi[i] = mvi[i]+file_type;
    }

    out = system(mkdir.c_str());

    bool enable_ch[8];
    enable_ch[0] = ui->enable1->isChecked();
    enable_ch[1] = ui->enable2->isChecked();
    enable_ch[2] = ui->enable3->isChecked();
    enable_ch[3] = ui->enable4->isChecked();
    enable_ch[4] = ui->enable5->isChecked();
    enable_ch[5] = ui->enable6->isChecked();
    enable_ch[6] = ui->enable7->isChecked();
    enable_ch[7] = ui->enable8->isChecked();

    //QMessageBox::about(this,"",QString::fromStdString(mv0));
    for(int i = 0; i<channels; i++){
        //std::cout << mvi[i] << std::endl;
        if(enable_ch[i]) out = system(mvi[i].c_str());
    }

    return true;

}

std::string MainWindow::changeVoltage(double voltage){
    std::string post;
    std::string pre;
    pre = std::to_string(static_cast<int>(voltage));
    post = std::to_string(static_cast<int>(trunc(voltage*10))%10) + std::to_string(static_cast<int>(trunc(voltage*1000))%100 / 10);
    std::string voltageS = pre+"V"+post;
    //QMessageBox::about(this,"",QString::fromStdString(voltageS));

    return voltageS;
}


void MainWindow::on_button_movefile_2_clicked()
{
    QMessageBox::about(this,"","Calibration file moved. Check it!");

    ui->calibration_check->setChecked(true);
    ui->calibration_check_3->setChecked(true);
    // Take info from the data tab, so it is possible to go to the right folder
    int runNo = std::stoi(ui->run->text().toStdString());
    int subRunNo = std::stoi(ui->subrun_2->text().toStdString());
    double voltage = std::stod(ui->voltage->text().toStdString());
    double threshold = std::stod(ui->threshold->text().toStdString());
    std::string triggerCh = ui->trigger_channel->text().toStdString();
    std::string extra = ui->extra->text().toStdString();
    std::string primary = ui->primary_name->text().toStdString();
    std::string file_type = ui->file_type->text().toStdString();

    move_calibration_file(runNo,subRunNo,voltage,threshold,triggerCh,extra,primary,file_type);

    // update subrun number
    subRunNo++;
    std::string newSubRun = std::to_string(subRunNo);

    ui->subrun_2->setText(QString::fromStdString(newSubRun));

}

bool MainWindow::move_calibration_file(int run, int subrun, double voltage, double threshold, std::string triggerCh, std::string extra, std::string primary, std::string file_type)
{
    int out = 0;
    std::string mkdir = "mkdir -p ~/Documents/ADC_data/coldbox_data/" + primary + "/";
    out = system(mkdir.c_str());
    std::string folder = folder_name();
    folder = folder + "Calibration/";

    std::vector<std::string> mvi(channels);
    for(int i = 0; i<channels; i++){
        mvi[i] = "mv -n ~/Desktop/WaveDumpData/wave"+std::to_string(i)+file_type+" ~/Documents/ADC_data/coldbox_data/" + primary + "/";
    }

    std::string voltageS = changeVoltage(voltage);

    double led_voltage = std::stod(ui->led_voltage->text().toStdString());
    std::string led_voltageS = changeVoltage(led_voltage);
    int width = std::stoi(ui->led_width->text().toStdString());

    //QMessageBox::about(this,"",QString::fromStdString(folder0));
    mkdir = mkdir+folder;

    for(int i = 0; i<channels; i++){
       mvi[i] = mvi[i] + folder;
       mvi[i]= mvi[i] + std::to_string(subrun) + "_wave"+std::to_string(i) + "_" + voltageS + "_" + led_voltageS + "_" + std::to_string(width) + "ns";
       mvi[i] = mvi[i]+file_type;


    }



    out = system(mkdir.c_str());

    bool enable_ch[8];
    enable_ch[0] = ui->enable1->isChecked();
    enable_ch[1] = ui->enable2->isChecked();
    enable_ch[2] = ui->enable3->isChecked();
    enable_ch[3] = ui->enable4->isChecked();
    enable_ch[4] = ui->enable5->isChecked();
    enable_ch[5] = ui->enable6->isChecked();
    enable_ch[6] = ui->enable7->isChecked();
    enable_ch[7] = ui->enable8->isChecked();

    //QMessageBox::about(this,"",QString::fromStdString(mv0));
    for(int i = 0; i<channels; i++){
        // std::cout << mvi[i] << std::endl;
        if(enable_ch[i]) out = system(mvi[i] .c_str());
    }


    return true;
}


void MainWindow::on_lock_folder_clicked(bool checked)
{
    if(checked){
        ui->primary_name->setDisabled(true);
    }
    else{
        ui->primary_name->setEnabled(true);
    }
}

int MainWindow::getFactor()
{
    std::string max_samplingRate = ui->adcMaximumRate->currentText().toStdString();
    std::string samplingRate = ui->samplingRate_2->currentText().toStdString();
    double sampling=1;
    double maxsampling=1;
    if(samplingRate == "500 MSamples/s") sampling = 500;
    if(samplingRate == "250 MSamples/s") sampling = 250;
    if(samplingRate == "125 MSamples/s") sampling = 125;
    if(samplingRate == "62.5 MSamples/s") sampling = 62.5;

    if(max_samplingRate == "500 MSamples/s") maxsampling = 500;
    if(max_samplingRate == "250 MSamples/s") maxsampling = 250;

    int factor = (int)maxsampling/sampling;
    return factor;
}


void MainWindow::on_pushButtonRecompile_clicked()
{
    std::string nwaveforms= ui->nwvfs->text().toStdString();
    if(nwaveforms == "") nwaveforms = "10000";
    std::string passwrd= ui->passwrd->text().toStdString();
    passwrd = passwrd+"\n";

    std::string max_samplingRate = ui->adcMaximumRate->currentText().toStdString();
    std::string samplingRate = ui->samplingRate_2->currentText().toStdString();

    int factor = getFactor();

    if(factor==0){
        std::string errormessage = "ADC Nominal sampling should be higher or equal to Sampling rate!";
        QMessageBox::about(this,"ERROR!",errormessage.c_str());
        return;
    }

    std::string message = "Recompiling wavedump\nSetting " + nwaveforms + " as maximum for continous writting.\nSampling Rate set to " + samplingRate;
    QMessageBox::about(this,"",message.c_str());

    std::string validate_sudo = "printf '" + passwrd + "' | sudo -S -v";
    system(validate_sudo.c_str());

    std::string recompile_command = "bash ~/Documents/CAEN_Digitizer/recompile_wavedump.sh " + nwaveforms + " " + std::to_string(factor);
    system(recompile_command.c_str());

    ui->samplingRate->setCurrentText(ui->samplingRate_2->currentText());
    writeConfigFile(false);

    QMessageBox::about(this,"","Done!\n\Please restart wavedump.");

}


void MainWindow::on_FileTypeSet_currentTextChanged(const QString &arg1)
{
    if(arg1 == "Binary"){
        ui->file_type->setText(".dat");
    }
    else{
        int answer = QMessageBox::question(this,"","Are you sure? Binary is awesome...",QMessageBox::Yes,QMessageBox::No);
        if(answer==QMessageBox::Yes){
            QMessageBox::about(this,"",":(");
            ui->file_type->setText(".txt");
        }
        else{
            ui->FileTypeSet->setCurrentText("Binary");
        }
    }
}


void MainWindow::enable_and_trigger(bool checked, QCheckBox* myt)
{
    if(checked){
        if(!ui->externaltrigger->isChecked()){
            setEnabledTrigger(myt);
        }
    }
    else{
        setDisabledTrigger(myt);
    }
}
void MainWindow::setEnabledTrigger(QCheckBox *myt)
{
    myt->setDisabled(false);
}
void MainWindow::setDisabledTrigger(QCheckBox *myt)
{
    myt->setChecked(false);
    myt->setDisabled(true);
}


void MainWindow::disabletriggers()
{
        ui->trigger1->setChecked(false);
        ui->trigger2->setChecked(false);
        ui->trigger3->setChecked(false);
        ui->trigger4->setChecked(false);
        ui->trigger5->setChecked(false);
        ui->trigger6->setChecked(false);
        ui->trigger7->setChecked(false);
        ui->trigger8->setChecked(false);


        ui->trigger1->setDisabled(true);
        ui->trigger2->setDisabled(true);
        ui->trigger3->setDisabled(true);
        ui->trigger4->setDisabled(true);
        ui->trigger5->setDisabled(true);
        ui->trigger6->setDisabled(true);
        ui->trigger7->setDisabled(true);
        ui->trigger8->setDisabled(true);


}

void MainWindow::on_externaltrigger_clicked(bool checked)
{
    if(checked){
        disabletriggers();
    }
    else{
        if(ui->enable1->isChecked()) ui->trigger1->setDisabled(false);
        if(ui->enable2->isChecked()) ui->trigger2->setDisabled(false);
        if(ui->enable3->isChecked()) ui->trigger3->setDisabled(false);
        if(ui->enable4->isChecked()) ui->trigger4->setDisabled(false);
        if(ui->enable5->isChecked()) ui->trigger5->setDisabled(false);
        if(ui->enable6->isChecked()) ui->trigger6->setDisabled(false);
        if(ui->enable7->isChecked()) ui->trigger7->setDisabled(false);
        if(ui->enable8->isChecked()) ui->trigger8->setDisabled(false);
    }

}


void MainWindow::on_enable1_clicked(bool checked)
{
    enable_and_trigger(checked,ui->trigger1);
}

void MainWindow::on_enable2_clicked(bool checked)
{
    enable_and_trigger(checked,ui->trigger2);
}

void MainWindow::on_enable3_clicked(bool checked)
{
    enable_and_trigger(checked,ui->trigger3);
}

void MainWindow::on_enable4_clicked(bool checked)
{
    enable_and_trigger(checked,ui->trigger4);
}

void MainWindow::on_enable5_clicked(bool checked)
{
    enable_and_trigger(checked,ui->trigger5);
}

void MainWindow::on_enable6_clicked(bool checked)
{
    enable_and_trigger(checked,ui->trigger6);
}

void MainWindow::on_enable7_clicked(bool checked)
{
    enable_and_trigger(checked,ui->trigger7);
}

void MainWindow::on_enable8_clicked(bool checked)
{
    enable_and_trigger(checked,ui->trigger8);
}








void MainWindow::on_pushButton_SetConfig_clicked()
{

    writeConfigFile(true);

}


void MainWindow::writeConfigFile(bool extra)
{

    bool enable_ch[8];
    enable_ch[0] = ui->enable1->isChecked();
    enable_ch[1] = ui->enable2->isChecked();
    enable_ch[2] = ui->enable3->isChecked();
    enable_ch[3] = ui->enable4->isChecked();
    enable_ch[4] = ui->enable5->isChecked();
    enable_ch[5] = ui->enable6->isChecked();
    enable_ch[6] = ui->enable7->isChecked();
    enable_ch[7] = ui->enable8->isChecked();

    bool trigger_ch[8];
    trigger_ch[0] = ui->trigger1->isChecked();
    trigger_ch[1] = ui->trigger2->isChecked();
    trigger_ch[2] = ui->trigger3->isChecked();
    trigger_ch[3] = ui->trigger4->isChecked();
    trigger_ch[4] = ui->trigger5->isChecked();
    trigger_ch[5] = ui->trigger6->isChecked();
    trigger_ch[6] = ui->trigger7->isChecked();
    trigger_ch[7] = ui->trigger8->isChecked();

    int trigger_level_ch[8];
    trigger_level_ch[0] = std::stoi(ui->triggerL1->text().toStdString());
    trigger_level_ch[1] = std::stoi(ui->triggerL2->text().toStdString());
    trigger_level_ch[2] = std::stoi(ui->triggerL3->text().toStdString());
    trigger_level_ch[3] = std::stoi(ui->triggerL4->text().toStdString());
    trigger_level_ch[4] = std::stoi(ui->triggerL5->text().toStdString());
    trigger_level_ch[5] = std::stoi(ui->triggerL6->text().toStdString());
    trigger_level_ch[6] = std::stoi(ui->triggerL7->text().toStdString());
    trigger_level_ch[7] = std::stoi(ui->triggerL8->text().toStdString());

    bool externaltrigger = ui->externaltrigger->isChecked();

    std::string trigger_type = "";
    if(externaltrigger){
        trigger_type = "External trigger";
    }
    else{
        trigger_type = "Self trigger";
    }

    int baseline_ch[8];
    baseline_ch[0] = std::stoi(ui->base1->text().toStdString());
    baseline_ch[1] = std::stoi(ui->base2->text().toStdString());
    baseline_ch[2] = std::stoi(ui->base3->text().toStdString());
    baseline_ch[3] = std::stoi(ui->base4->text().toStdString());
    baseline_ch[4] = std::stoi(ui->base5->text().toStdString());
    baseline_ch[5] = std::stoi(ui->base6->text().toStdString());
    baseline_ch[6] = std::stoi(ui->base7->text().toStdString());
    baseline_ch[7] = std::stoi(ui->base8->text().toStdString());

    std::string filetype = ui->FileTypeSet->currentText().toStdString();
    std::transform(filetype.begin(), filetype.end(),filetype.begin(), ::toupper);

    double time = std::stod(ui->time_in_us->text().toStdString());
    time = time*1e-6;
    double sampling = 0;
    std::string samplingRate = ui->samplingRate->currentText().toStdString();
    if(samplingRate == "500 MSamples/s") sampling = 2e-9;
    if(samplingRate == "250 MSamples/s") sampling = 4e-9;
    if(samplingRate == "125 MSamples/s") sampling = 8e-9;
    if(samplingRate == "62.5 MSamples/s") sampling = 16e-9;

    double dnpts = time/sampling;
    int npts = (int)round(dnpts);


    int timeCheck = int(round(time*1e9));
    int samplingCheck = sampling*1e9;
    int res = timeCheck%samplingCheck;
    if(res!=0){
        int finaltime = npts*samplingCheck;
        std::string message = "Time duration and sampling rate are not compatible!\nRecord length set to " + std::to_string(npts) + "\nCorresponding to " + std::to_string(finaltime) + " ns";
        QMessageBox::about(this,"WARNING!!!",message.c_str());
    }

    std::string samplingRate2 = ui->samplingRate_2->currentText().toStdString();

    if(samplingRate!=samplingRate2){
        QMessageBox::about(this,"ERROR!!!","Sampling rate does not match the what is set at ''Recompile''.\nPlease, check if the configuration is correct or recompile wavedump");
    }

    int factor = getFactor();

    int record_length = npts*factor;

    std::string polarity = ui->setPolarity->currentText().toStdString();
    std::transform(polarity.begin(), polarity.end(),polarity.begin(), ::toupper);

   std::ofstream f;
   f.open("/etc/wavedump/WaveDumpConfig.txt", std::ofstream::out);

   if(!f.is_open()){
       QMessageBox::about(this,"ERROR!","WaveDumpConfig.txt not opened");
   }
   std::string setexternaltrigger = "DISABLED";
   if(externaltrigger){
       setexternaltrigger = "ACQUISITION_ONLY";
   }

   std::string output[15];
   int nout = 15;
   output[0] = "[COMMON]";
   output[1] = "OPEN USB " + std::to_string(ui->usbPort->value()) + " 0";
   output[2] = "RECORD_LENGTH  " + std::to_string(record_length);
   output[3] = "DECIMATION_FACTOR  1";
   output[4] = "POST_TRIGGER  " + ui->postTrigger->text().toStdString();
   output[5] = "PULSE_POLARITY  " + polarity;
   output[6] = "EXTERNAL_TRIGGER   " + setexternaltrigger;
   output[7] = "FPIO_LEVEL  " + ui->externalType->currentText().toStdString();
   output[8] = "OUTPUT_FILE_FORMAT  " + filetype;
   output[9] = "OUTPUT_FILE_HEADER  YES";
   output[10] = "TEST_PATTERN  NO";
   output[11] = "ENABLE_INPUT  NO";
   output[12] = "BASELINE_LEVEL  10";
   output[13] = "TRIGGER_THRESHOLD  100";
   output[14] = "CHANNEL_TRIGGER  DISABLED";

   std::string tstate[2] = {"DISABLED","ACQUISITION_ONLY"};
   std::string estate[2] = {"NO","YES"};

   for(int i = 0; i<nout; i++){
       f << output[i] << "\n\n";
   }
   for(int i = 0; i<channels; i++){
       int aux = enable_ch[i] ? 1 : 0;
       int aux2 = trigger_ch[i] ? 1 : 0;
       f << "[" + std::to_string(i) + "]" + "\n";
       f << "ENABLE_INPUT		" + estate[aux] + "\n";
       if(enable_ch[i]){
            f << "BASELINE_LEVEL		" + std::to_string(baseline_ch[i]) + "\n";
            f << "TRIGGER_THRESHOLD	" + std::to_string(trigger_level_ch[i]) + "\n";
            f << "CHANNEL_TRIGGER		" + tstate[aux2] + "\n";
       }
    f << "\n";
   }
   f << "\n";
   f.close();

   std::string setmessage = "Trigger type: " + trigger_type + "\nRecord length: " + std::to_string(npts) + " pts\nPulse polarity: " + polarity + "\nFile type: " + filetype;
   if(extra){
       setmessage = setmessage + "\nClick 'Ok' and reaload wavedump (shift+r)";
   }
   QMessageBox::about(this,"",setmessage.c_str());






}

void MainWindow::save_config_file(std::string folder){
    std::string primary = ui->primary_name->text().toStdString();
    std::string cpy_command = "cp /etc/wavedump/WaveDumpConfig.txt ~/Documents/ADC_data/coldbox_data/" + primary + "/" + folder + "config_used.log";
    system(cpy_command.c_str());

    QMessageBox::about(this,"","Config. file saved to corresponding run folder");
};


void MainWindow::on_button_save_config_2_clicked()
{
    std::string primary = ui->primary_name->text().toStdString();

    std::string mkdir = "mkdir -p ~/Documents/ADC_data/coldbox_data/" + primary + "/";
    system(mkdir.c_str());
    std::string folder = folder_name2();


    mkdir = mkdir+folder;

    system(mkdir.c_str());

    save_config_file(folder);
}


void MainWindow::on_button_save_config_clicked()
{


    // This take the necessary info to create the folder and files
    std::string primary = ui->primary_name->text().toStdString();

    std::string mkdir = "mkdir -p ~/Documents/ADC_data/coldbox_data/" + primary + "/";
    system(mkdir.c_str());
    std::string folder = folder_name();

    mkdir = mkdir+folder;

    system(mkdir.c_str());


    save_config_file(folder);
}

