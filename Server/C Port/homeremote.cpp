#include <stdio.h>
#include <map>
#include <wiringPi.h>
#include <mcp23017.h>
#include <mysql/mysql.h>

class Gpio {
    char Pin;
    char Direction;
    char Name;

    public: 
        void Setup(char, char, char);
};
void Gpio::Setup(char name, char pin, char direction) {
    Pin = pin;
    Direction = direction;
    Name = name;
}

int main() {
    std::map<std::char, Gpio, std::less<std::char> >  outputs;
    Gpio *g;
    MYSQL *conn;
    MYSQL_ROW row;
    MYSQL_RES *res;
	conn = mysql_init (NULL);
    mysql_real_connect(conn, "localhost", "root", "legoman1", "automation", 0, NULL, 0 );
    if(mysql_query(conn, "SELECT * FROM outputs")) {
        printf("%s \n", mysql_error(conn));
    }   
   
    res = mysql_use_result(conn);
    while((row = mysql_fetch_row(res)) != NULL) {
        printf("Got output: %s \n", row[2]);
        g = new Gpio();
        outputs[row[2]] = g;
    }
    wiringPiSetupGpio();
    mcp23017Setup (100, 0x20) ;
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
