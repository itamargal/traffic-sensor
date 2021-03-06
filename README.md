# ATX Traffic Data Collection Network

This is a City of Austin initative to create a network of traffic sensors built with commodity hardware and open-source software. We're kicking off this project at the [2017 ATX Hack for Change](http://atxhackforchange.org/) and are sponsoring it as part of the [GigaTECHs App Competition](https://herox.com/GigaTECHSATX/guidelines).

 * [Vision](#vision)
 * [Project Tasks](#project-tasks)
 * [Hardware](#hardware)
 * [Talk to Us](#talk-to-us)

## Vision

<img src="/media/cabinet_pi_sm.jpg" align="left" alt="A Raspberry Pi in a traffic signal cabinet." height="275px"> 

Our goal is to create a network of traffic sensors built with commodity hardware and open-source software. We intend to make the sensor software and collected data publicly available so that research institutions, private companies, and the general public can help us derive new insights about Austin’s transportation system. 

We do not have the IT resources to take on this project by ourselves, and commercial data collection solutions are prohibitively expensive. That’s why we’re seeking help from Austin’s incredible community of civic-minded technologists to help us achieve our goal. We believe strongly that, if successful, this project will lead to tangible improvements in Austin’s transportation system, and will represent a truly innovative approach to the deployment of community-driven smart city technologies.

<br>

## Project Tasks

### Data Collection 

Write a data collection program to run on an SBC (single board computer) such as a Raspberry Pi, an Arduino, or an Edison. The program can use WiFi, Bluetooth, environmental data, and/or any other sensor technology that the SBC supports. The software should:
 * Produce data that can be easily consumed for processing and analysis.
 * Anonymize MAC addresses, ESSIDs, IP addresses, or any other potentially sensitive data

### Traffic Data Processing

Create a tool which which processes collected WiFi, Bluetooth, and other data to derive meaninful information about traffic conditions. Outputs might include:
  * Travel Time
  * Traffic Volume
  * Roadway user classification (motorized vehicle, pedestrian, etc.)

### Device Management

Write a program that manages the traffic sensors remotely. The application should allow the end-user to:
 * Retrieve information about installed sensors, including device status, device location, memory usage, etc.
 * Configure and deploy a new traffic sensor
 * Remotely push software updates to sensors

### Visual Analysis
 Create a web-application to visualize the Austin transportation network in a way that incorporates the traffic sensor data. The application might display:
 * Real-Time Traffic Conditions
 * How Traffic Conditions Change by day of week and time of day
 * Origin-Destination Analysis


## Hardware

We'll have the following equipment on-hand during the ATX Hack for Change:
 * [Raspbery Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)'s running Raspbian installed via [NOOBS](https://www.raspberrypi.org/downloads/noobs/). SSH is enabled with the [default user login](https://www.raspberrypi.org/documentation/linux/usage/users.md).
 * [External WiFi USB adapters](https://www.amazon.com/gp/product/B00H95C0A2/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) which use the RT5370 chipset.
 * [DHT22 Digital Temperature and Humidity Sensors](https://www.amazon.com/gp/product/B01K1Q6DEO/ref=oh_aui_detailpage_o03_s01?ie=UTF8&psc=1)
 * [Class 1 Bluetooth 4.0 USB adapters](https://www.amazon.com/gp/product/B012EVAME6/ref=oh_aui_detailpage_o04_s01?ie=UTF8&psc=1)


## Talk to Us
 * Slack (details TBD)
 * Email <a href="mailto:HackTheTraffic@austintexas.gov" target="_top">HackTheTraffic@austintexas.gov</a>
 
