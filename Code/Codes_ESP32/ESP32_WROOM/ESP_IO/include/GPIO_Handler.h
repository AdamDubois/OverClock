#ifndef GPIO_HANDLER_H
#define GPIO_HANDLER_H

class GPIO_Handler {
public:
    Adafruit_MCP23X17 mcp;

    void init();
    int* readAll();
};

#endif