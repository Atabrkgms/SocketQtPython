#include "mainwindow.h"

#include <QApplication>
#include <QLocale>
#include <QTranslator>
#include <QCoreApplication>
#include <QTcpSocket>
#include <QDebug>
#include <QFile>
#include <QProcess>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "denemeQT_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            a.installTranslator(&translator);
            break;
        }
    }

    QProcess process;

    // Python kodunu çalıştırmak için komutu oluşturun (örneğin: python3 script.py)
    process.start("/Library/Frameworks/Python.framework/Versions/3.12/bin/python3", QStringList() << "/Users/ataberkgumus/Desktop/LocalSocket/localsocket.py");

    if (!process.waitForStarted()) {
        qDebug() << "İşlem başlatılamadı veya bir hata oluştu:" << process.errorString();
        // Kullanıcıya uygun bir mesajı göstermek için QMessageBox veya başka bir yöntem kullanabilirsiniz
    } else {
        qDebug() << "İşlem başlatıldı";
        process.waitForFinished(-1);
    }

    MainWindow w;
    w.show();
    return a.exec();
}
