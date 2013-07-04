import RPi.GPIO as GPIO
from mcp import MCP230XX_GPIO as mcp

def setup(pin, direction):
    if "mcp" in pin:
        pin = pin[3:]
        mcp.setup(pin, direction)
    else:
        GPIO.setup(int(pin), direction)

def output(pin, dir):
    if "mcp" in pin:
        pin = pin[3:]
        mcp.output(pin, dir)
    else:
        GPIO.output(int(pin), )