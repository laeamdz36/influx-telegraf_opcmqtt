# Collector telegraf MQTT, OPC UA, InfluxDB

Objetivo: Recoleccion e ingesta de datos hacia la base de datos influx db desde fuentes como Servidor OPC y Brokers MQTT
Servir los datos a traves de la API de Influx DB hacia Servicios como grafana

The container will initialize a bucket with the configured name

Plataforma montada sobre docker

- InfluxDB OSS 2
- Telegraf Plugin MQTT input
- Telegraf Plugin OPC UA, conexion a OPC Server (Ignition OPC UA), ON DEV

## Influx DB - Line Protocol

General structure:
> measurement, tag_set field_set timestamp

    - Measurement: The name of the metric or table
    - tag_set: A set of tags key-value to index the values
    - filed_set: The set of values or data that is being measured
    - timestamp: The date and time of the data in Unix format in nanoseconds