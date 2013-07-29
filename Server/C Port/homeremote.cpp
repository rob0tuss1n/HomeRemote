#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <map>
#include <wiringPi.h>
#include <mcp23017.h>
#include <sqlite3.h>

int main() {
    system("gpio load i2c");
    sqlite3 *database;
    sqlite3_open("database.sqlite", &database);
    wiringPiSetupGpio();
    mcp23017Setup(100, 0x20);
    getTableData(database);
    pinMode(22, OUTPUT);
    pinMode(101, OUTPUT);
    while (1) {
        digitalWrite(101, 1);
        digitalWrite(22, 1);
        delay(1000);
        digitalWrite(101, 0);
        digitalWrite(22, 0);
        delay(1000);
    }
}
