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

### Description for lñine protocol to write data in InfluxDB3

- Table: A string that identifies the table to store data in
- tag set: Comma-delimited list of key value pairs, each representing a tag
- field set: Key-value pairs between the first and second unscaped whitespaces
- timestamp: Integer value after the second unescaped whitespace

> myTable,tag1=val1,tag2=val2 field1="v1",field2=1i 0000000000000000000

example:
```
Table: home
- tags
  - room: Living Room or Kitchen
- fields
    temp: temperature in °C (float)
    hum: percent humidity (float)
    co: carbon monoxide in parts per million (integer)
timestamp: Unix timestamp in second precision
```