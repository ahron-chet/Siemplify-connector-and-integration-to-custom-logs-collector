# Siemplify Connector and Integration to Custom Logs Collector
This repository contains a Siemplify connector and integration to a custom logs collector using sockets as a custom Logstash. 
The connector allows for the collection analysis and send logs and  data to Siemplify soar system system.

The integration is implemented using sockets, allowing for real-time data transfer and flexible data processing. The connector can be easily configured to fit the needs of the specific environment. 

# In addition, the repository includes a folder called TOOLS containing additional features such as:

- Creating a daily report in a specified format and automatically sending it via email
- Saving all events in a DATABASE and performing actions such as hunting and pulling a summary of events over a range of time, which can be sent to email or Telegram as needed
- potential errors are monitored and will be sent via email or Telegram as needed.

To use the connector and integration, follow the instructions provided in the repository. Note that the integration requires the use of Logstash and a custom logs collector, which must be set up and configured separately.
