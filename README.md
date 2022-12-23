# Siemplify Connector and Custom Logs Collector Integration

This repository contains a connector and integration for Siemplify that allows for the collection, analysis, and transfer of logs and data to the Siemplify SOAR system using sockets as a custom Logstash. The integration is designed to provide real-time data transfer and flexible data processing, and can be easily configured to meet the specific needs of your environment.

### In addition to the main connector and integration, the repository includes a TOOLS folder with additional features such as:

- A daily report generator that can be automatically sent via email in a specified format
- The ability to save all events in a database, and perform actions such as hunting or pulling a summary of events over a specified time period.
- Monitoring for potential errors, with alerts sent via email or Telegram as needed


## To use the connector and integration:

###### Server Side:`

- Copy the server folder to a dedicated Linux server
- Define the log feed address that will listen for client logs on the syslog port
- Set a password for authentication and a key for encryption
- Run the Server.py file

###### Siemplify Side:

Create a new connector for the desired integration
Add the contents of the Connector.py file in the Connector folder
Define the IP address of the server (Server.py)
Set the same password and encryption key as on the server side
