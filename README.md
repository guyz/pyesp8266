ESP8266 Serial-to-WiFi Module
=========

The ESP8266 is a low cost Serial-to-WiFi module that interfaces nicely to any microcontroller. However, a word of caution -- it is highly undocumented (primary reason for writing this document), and more importantly, it is frequently updated and not backward compatible. A good example is how newer versions use 9600 baud rate, while older versions (by old I'm referring to 2-3 months old modules) used 57600-115200 baud rates.

In general, the tutorial below will get you started. Once you are set up, you should learn more about the module's protocol here: https://nurdspace.nl/ESP8266#AT_Commands

## Usage

First, it is important to understand how the board works. The ESP8266 has a full TCP/UDP stack support. It can also be easily configured as a web server. The module accepts commands via a simple serial interface. It then responds back with the operation's outcome (assuming everything is running correctly). Also, once the device is connected and is set to accept connections, it will send unsolicited messages whenever a new connection or a new request is issued.

### Testing the module via FTDI (or a USB-to-Serial cable)

Before connecting the module to a microcontroller, it's important to try it directly via a serial interface. An easy solution is to use a 3V3 FTDI cable. Note that the module is not designed for more than 3.6V, so a 3.3V power supply should be used - both for power and logic. The current batch of the FTDI cables deliver 5V in the supply rail even for the 3V3 version. Apparently, this is an error made by the manufacturer, so it might be corrected at some point.

#### Hardware setup

![alt text](https://raw.githubusercontent.com/guyz/pyesp8266/master/esp8266_pinout.png "ESP8266 Pinout") ![alt text](https://raw.githubusercontent.com/guyz/pyesp8266/master/ftdi_pinout.png "FTDI Pinout")

1. Connect the RX/TX pins in a 3v3 FTDI cable to the TX/RX pins in the ESP module.
2. Connect a 3v3 power supply to the VCC/GND pins. Note that it is possible to use an Arduino 3v3 supply for this.
3. Connect the CH_PID pin to VCC as well.
4. The rest of the pins should be floating. However, be prepared to occasionally ground the RST pin. This would help if the board is stuck on some command.

### Software and testing:
1. Clone this repository.
2. Unzip and execute the following command:
```python esp8266test.py <serial_port> <baud_rate> <ssid> <password> ```
3. You should see a bunch of commands going through, including a list of available APs. Eventually, you should see the IP address assigned to the module printed.
4. ping the IP address obtained in (3). If that works, then you got it working and can start doing cool stuff!

### Webserver example:
Once you've successfully set up the device and confirmed that it can connect to a WiFi, you can try something more elaborate. the file esp8266server.py will go through the same flow as the test module, but it will also continue to setting up the device to accepting multiple connections:

```python
send_cmd( "AT+CIPMUX=1" ) # multiple connection mode
send_cmd( "AT+CIPSERVER=1,80" )
```

To run this module, issue the following command in the right directory:
```
python esp8266server.py <serial_port> <ssid> <password>
```

Then, head to your browser and enter the following URL:
```
http://<ip_address>
```

If everything works correctly, you should see the serial request being pushed through the serial interface. The python code would in turn serve a response back which will show on the browser. If you want to fiddle around with the response, look at this line in the code:

```python
process_request("GOT IT! (" + str(datetime.datetime.now()) + ")")
```

### Troubleshooting:

If you encountered issues, check the following:
1. Is the red LED on the module lit? If it isn't, the board isn't getting power.
2. When trying to issue commands, do you see the blue LED on the module blinking? If not, check the RX/TX connections. If the LED is constantly lit, then one of the connections is wrong - probably RX/TX or one of the other pins.
3. Are you seeing gibberish? You're probably doing well, but try a different BAUD rate.

If you receive the error `ImportError: No module named serial`
Run `sudo pip install pyserial`

### Testing the module via a microcontroller

Once you've got the module up and running with a direct serial connection, you can move on to plugging it into a microcontroller board. The steps are largely the same - you connect the RX/TX pins to the TX/RX pins of a microcontroller, or - if you're using an Arduino like board - you can set up a SoftwareSerial interface and use any 2 digital pins for the communication.

As to powering up the device - while I have briefly tried and confirmed that a direct 5V supply could work, it is not recommended and your mileage may vary. There are multiple ways to regulate the voltage (e.g., http://rayshobby.net/?p=9734), or if you're at the CBA lab - try using one of the larger 3.3V SOT223 voltage regulators, or a similar capable one.

If you're using the Arduino IDE, you should check out these resources for some reference code:

1. http://rayshobby.net/?p=9734
2. https://github.com/INEXTH/Arduino-ESP8266_libs

The result should look something like this:

<< vid arduino >>
