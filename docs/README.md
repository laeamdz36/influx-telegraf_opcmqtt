# Collector telegraf MQTT, OPC UA, InfluxDB

Objetivo: Recoleccion e ingesta de datos hacia la base de datos influx db desde fuentes como Servidor OPC y Brokers MQTT
Servir los datos a traves de la API de Influx DB hacia Servicios Grafana

### Notes 2025/11/09:
Los dispositivos Pi Pico W con micropython estan enviando la data del tipo string
es necesario ya sea desde el mismo dispositivo enviarlo como line protocol para influxDB o manejarlo desde alguna aplicacion como Python o Java.

Desarrollo 1, forwarder en Python para suscribirse a el Broker MQTT principal que es Mosquitto en Home assistant y desde pyhton llevar a cabo la transformacion en line protolo de los topicos registrados en dicha aplicacion, para asi insertarlo de forma directa a InfluxDB

Desventajas en python:
1. La concurrencia, tiene un event loop del tipo poll, puede existir overhead en la ingesta de datos desde el broker

Desarrollo 2, es la ingesta desde el input plugin de telegraf para MQTT, esto ha sido probado con resultados satisfactorios

Para la conexion OPC UA, se utilizaria el servidor de Ignition Maker, pero es posible explirar

-->> Como desarrollo practico, para la Observavilidad en plataformas y tecnologias Open Source, se llevara a cabo la implementacion del monitor para infraestructura de control

PLC Allen Bradley
Los PLC allen bradley cuentan con comunicacion Ethernet IP basado en el porotcolo CIP, al igual de OPC, para la lectura de informacion de monitore, utilizaremos la libreria pycomm3 para leer tags del PLC, transformaremos la data en el lineprotocol necesario par INfluxDB 3 Core
Tecnologias:
InfluxDB 3 Core
Python 3
    pycomm3
Grafana

Node exorter para infraestructura:
Input plugin Telegra, enviar a influxDb3 y monitorear con grafana

The container will initialize a bucket with the configured name

Plataforma montada sobre docker

- InfluxDB OSS 2
- Telegraf Plugin MQTT input
- Telegraf Plugin OPC UA, conexion a OPC Server (Ignition OPC UA), ON DEV
- Grafana

# Desarrollos en el PLC

1. Maquina secuencial, se enviara un entero como descriptor del State, para asii graficar Stat Graph en grafana
2. Mauqina secuencial, se enviara un String como descriptor del State, visualizacion Stat Grafana
3. Monitorizacion de Variables de Negocio, como Runtime, utilizando Transaction groups de Ignition
4. Desarrollos de medicion de OEE, conceptos de breakdown, downtime

## Influx DB - Line Protocol (Se utilizara Influx DB 3 Core)

General structure:
> measurement, tag_set field_set timestamp

    - Measurement: The name of the metric or table
    - tag_set: A set of tags key-value to index the values
    - filed_set: The set of values or data that is being measured
    - timestamp: The date and time of the data in Unix format in nanoseconds

| Concepto  | InfluxDB 2.x | InfluxDB 3.x    |
| --------- | ------------ | --------------- |
| Bucket    | bucket       | database        |
| DB-Engine | TSM          | Arrow / Parquet |
| Query     | Flux / SQL   | ANSI SQL        |

influxdb 3 core utiliza SQL, de esta forma onoo tendriamos que aprender un nuevo lenguaje
para el caso si ya conocemos SQL

## Docker compose file

Docker compose file will export the needed variables for the telegraf.config file from the
``.env`` file

> Variables
    - INFLUXDB_INIT_MODE=setup # Mode needed to init influxdb instance with initial settings
    - INFLUXDB_INIT_ORG=MyOrg # Organization for set influxdb
    - INFLUXDB_INIT_BUCKET=MyInitialBucket # initial bucket name
    - MQTT_BROKER_URL=tcp://192.168.0.1:1883 # the ip for the MQTT Broker


## Notas de desarrollo

2025/11/10
Se realizaron pruebas con los contenedores de influxdb3 core u su contenedor explroer
que es el UI web para administrar la instancia de influxdb3 core

Referencias a el explorer

[InfluxDb3 Core Explorer](https://docs.influxdata.com/influxdb3/explorer/)

1. Se llevo a cabo la generacion manual del token de InfluxDB3 core con la linea:

```bash
docker exec -it <Name_of_the_service_InfluxDB3> influxdb3 create token --admin
```

example:
```bash
docker exec -it <influxdb3_core> influxdb3 create token --admin
```