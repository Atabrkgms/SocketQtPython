#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QCoreApplication>
#include <QLocalSocket>
#include <QtNetwork>
#include <QImage>
#include <QBuffer>
#include <QDebug>
#include <QMessageBox>
#include <QProcess>
#include <QFile>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_button_clicked()
{

    QString serverAddress = "/tmp/python_unix_socket"; // Sunucu adresi     arguments << "/Users/ataberkgumus/Desktop/LocalSocket/localsocket.py";

    QLocalSocket socket(this);

    // Sunucuya bağlan
    socket.connectToServer(serverAddress);

    if (socket.waitForConnected()) {
        qDebug() << "Bağlantı başarılı. Sunucuya istek gönderiliyor...";

        // Bölge numarasını al
        QString bolgeNo = ui->bolgeno->text();

        // Semblol adını al
        QString sembolAdi = ui->sembolno->text();

        // Sunucuya bölge numarasını gönder
        socket.write(bolgeNo.toUtf8());
        socket.waitForBytesWritten();

        socket.waitForReadyRead();
        QByteArray responseBolgeData = socket.readAll();
        QString responseBolge = QString::fromUtf8(responseBolgeData);
        qDebug() << "Sunucudan gelen yanıt:" << responseBolge;

        // Başarılı yanıt kontrolü
        if (responseBolge == "Basarili") {
            qDebug() << "Bölge numarası başarılı bir şekilde alındı. Sembol adı gönderiliyor...";

            // Sembol adını gönder
            socket.write(sembolAdi.toUtf8());
            socket.waitForBytesWritten();

            socket.waitForReadyRead();
            QByteArray responseSembolData = socket.readAll();
            QString responseSembol = QString::fromUtf8(responseSembolData);
            qDebug() << "Sunucudan gelen yanıt:" << responseSembol;

            // Başarılı sembol yanıt kontrolü
            if (responseSembol == "Basarili") {
                qDebug() << "Sembol adı başarılı bir şekilde alındı. Resim gönderiliyor...";

                // Resmi gönder
                QString imagePath = "/Users/ataberkgumus/Desktop/test5.png";
                QFile file(imagePath);
                if (file.open(QIODevice::ReadOnly)) {
                    qDebug() << "Resim dosyası başarıyla açıldı.";

                    while (!file.atEnd()) {
                        QByteArray imageData = file.read(1024);
                        socket.write(imageData);
                        socket.waitForBytesWritten();
                    }

                    qDebug() << "Resim başarıyla sunucuya gönderildi.";

                    socket.waitForReadyRead();
                    QByteArray responseFunc = socket.readAll();
                    QString responsesfunc = QString::fromUtf8(responseFunc);
                    qDebug() << "Sunucudan gelen yanıt:" << responsesfunc;

                    file.close();
                    socket.close();
                } else {
                    qDebug() << "Resim dosyası açılamadı.";
                }
            } else {
                qDebug() << "Sembol adı alınamadı veya başarısız.";
            }
        } else {
            qDebug() << "Bölge numarası alınamadı veya başarısız.";
        }
    } else {
        qDebug() << "Bağlantı başarısız: " << socket.errorString();
    }


}

