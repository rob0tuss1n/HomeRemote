#include <wiringPi.h>
#include <mcp23017.h>

class IO {
    public:
        void SetupGpio();
        void SetupMcp23017(int, char);
        void SetupIO(int, int);
        void output(int, int);
        int input(int);
        int waitForInput(int, int)
}
IO::SetupGpio() {
    WiringPiSetupGpio();
}
IO::SetupMcp23017(int pinbase, char address) {
    mcp23017(pinbase, address);
}
IO::SetupIO(int pin, int mode) {
    pinMode(pin, mode);
}
IO::output(int pin, int state) {
    digitalWrite(pin, state);
}
IO::input(int pin) {
    return digitalRead(pin);
}
IO::waitForInput(int pin, int timeout) {
    if(timeout == null) {
        return waitForInterrupt(pin, -1)
    } else {
        return waitForInterrupt(pin, timeout)
    }
}