#include <stdio.h>
#include <mysql/mysql.h>

int main (int argc, char *argv[])
{
    MYSQL *conn;
    MYSQL_RES *res;
    MYSQL_ROW row;

    conn = mysql_init (NULL);
    mysql_real_connect(conn, "localhost", "root", "legoman1", "automation", 0, NULL, 0 );
    if(mysql_query(conn, "SELECT * FROM outputs")) {
        printf("%s \n", mysql_error(conn));
    }   
   
    res = mysql_use_result(conn);
    while((row = mysql_fetch_row(res)) != NULL)
        printf("%s \n", row[2]);
   
    mysql_close (conn);
    return 0;
}
