/*
 Copyright (C) 2011 James Coliz, Jr. <maniacbug@ymail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 2 as published by the Free Software Foundation.
 */

/**
 * Example of a sensor network 
 *
 * This sketch demonstrates how to use the RF24Network library to
 * manage a set of low-power sensor nodes which mostly sleep but
 * awake regularly to send readings to the base.
 *
 * The example uses TWO sensors, a 'temperature' sensor and a 'voltage'
 * sensor.
 *
 * To see the underlying frames being relayed, compile RF24Network with
 * #define SERIAL_DEBUG.
 *
 * The logical node address of each node is set in EEPROM.  The nodeconfig
 * module handles this by listening for a digit (0-9) on the serial port,
 * and writing that number to EEPROM.
 */

#include "RF24Network.h"
#include "RF24.h"
#include "S_message.h"

// Pin definitions
#define __PLATFORM__ "Getting Started board"

RF24 radio("/dev/spidev0.0", 8000000,25);
RF24Network network(radio);

void loop(void)
{
  while(1) {
    // Pump the network regularly
   network.update();

    // If we are the base, is there anything ready for us?
   while ( network.available() )
   {
     // If so, grab it and print it out
     RF24NetworkHeader header;
     S_message message;
     network.read(header,&message,sizeof(message));
     printf("APP Received %u %s from 0%o\n\r",header.id,message.toString(),header.from_node);
    }
  }
}

int main(void)
{
  //
  // Print preamble
  //
  printf("\n\rHomeRemote SensorNet Base Station/\n\r");

  // Which node are we?
  int this_node = 0;

  //
  // Bring up the RF network
  //

  radio.begin();
  network.begin(/*channel*/ 92, /*node address*/ this_node);
  loop();
}
// vim:ai:cin:sts=2 sw=2 ft=cpp
