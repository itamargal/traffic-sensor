# ATX Traffic Data Collection Network
This is a City of Austin initative to create a network of traffic sensors built with commodity hardware and open-source software. We're kicking off this project at the [2017 ATX Hack for Change](http://atxhackforchange.org/).

 * [Vision](#vision)
 * [Project Components](#project-components)
 * [Resources](#resources)

## Vision
Our goal is to create a network of traffic sensors built with commodity hardware and open-source software. We intend to make the sensor software and collected data publicly available so that research institutions, private companies, and the general public can help us derive new insights about Austin’s transportation system. 

We do not have the IT resources to take on this project by ourselves, and commercial data collection solutions are prohibitively expensive. That’s why we’re seeking help from Austin’s incredible community of civic-minded technologists to help us achieve our goal. We believe strongly that, if successful, this project will lead to tangible improvements in Austin’s transportation system, and will represent a truly innovative approach to the deployment of community-driven smart city technologies.
 
## Project Components

We've identified four components of this project, outlined below.

#### Data Collection 

Write a data collection program to run on an SBC (single board computer) such as a Raspberry Pi, an Arduino, or an Edison. The program can use WiFi, Bluetooth, environmental data, and/or any other sensor technology that the SBC supports. 

Key Requirements
 * output data can be easily consumed for processing and analysis.
 * the software should anonymize MAC addresses, ESSIDs, IP addresses, or any other potentially sensitive data

#### Traffic Data Processing

Process collected data WiFI, Bluetooth, and any other data to derive meaninful information about traffic conditions. Outputs might include:
  * Travel Time
  * Traffic Volume
  * Roadway user classification (motorized vehicle, pedestrian, etc.)

#### Device Management


#### Visual Analysis
 Create a web-application to visualize the Austin transportation network in a way that incorporates the traffic sensor data. The application might display:
 * Real-Time Traffic Conditions Map
 * Traffic Conditions Time-Series 
 * Origin-Destination Analysis


## Resources
 * Hardware
 * AWS
 * Slack
 
