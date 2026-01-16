# Main Description

The Compose is integrated by 3 services:
1. Influxdb3 Core
2. Telegraf
3. Influxdb Explorer

``Influexdb3 Core:`` Is the main time series database 
``Telegraf:`` Is a plugin for influxdb 3 core to ingest data from different data sources, for this deployment
MQTT input plugin will be deployed to perform a connection to a MQTT Broker built in Home Assistant.
``Influxdb Explorer:`` is a web graphical user interfaz to monitor and manage the influxdb3 core database.

## Main issues to solve

1. The data format from the source in this case Home assistan MQTT Broker Mosquitto.
2. Flexible way to provisioning the token key to influxdb3 core, in order to write data from telegraf.
3. Flexible way to define and estabish the token to telegraf to link to the corresponding influxdb database.
4. Volume type for each service in order to perform backups and restore.

## Config files

There is initial config files

``.env`` file is used to load during the running docker compose enviroment variables
used to set particular configs in each service

``secrets/`` directory to put all secrets files with extension ``.env`` to be loaded
by docker compose.

``influxdb\config`` directory to config settings for telegraf to achive data writing to influxdb3 core database.

#### Influxdb3 Core Service

Config variables needed:
INFLUX_DB_NAME: The database name

##### The token for Influxdb3 Core

To define a initial admin token for influxdb3 core, is possibel and maintaining
security with the docker secrets, thus, creating a file with the initial admin token 
like this:

``expiry_millis:`` Unix time in miliseconds.

```json
{
  "token": "put_here_the_initial_admin_token!",
  "name": "init-admin-token",
  "expiry_millis": 1857580146000
}
```
Write this lines of code into a file with a name to be used in docker compose secrets for influxdb3 core service.

#### Telegraf config to write Influxdb3 Core

Within the directory ``telegraf\`` the ``telegraf.conf`` is configured to be loaded into telegraf service, the directory is mount in a volume as described next:

```yml
volumes:
    # Mount configuration file
      - ./telegraf/telegraf.conf:/etc/telegraf/telegraf.conf:ro
```

The basic configuration needed to write into the database is:
Where INFLUX_TOKEN is loaded from docker secrets

``telegraf.conf``

```conf
[agent]
  interval = "3s"
  round_interval = true

[[outputs.influxdb_v2]]
  urls = ["http://influxdb3-core:8181"]
  token = "${INFLUXDB_TOKEN}"
  organization = "ignored"
  bucket = "main"
```

To ingest data from MQTT broker use the input plugin

``[[inputs.mqtt_consumer]]``

#### Influxdb Explorer

For configuration the explorer service, is need to mount a ``config.json`` file`in
the directory ``influxdb\config``

```config.json``

```json
{
    "DEFAULT_INFLUX_SERVER": "http://influxdb3-core:8181",
    "DEFAULT_INFLUX_DATABASE": "main",
    "DEFAULT_API_TOKEN": "the_token_configured_also_for_influxdb3_service",
    "DEFAULT_SERVER_NAME": "Local InfluxDB 3"
}
```

## Ingest data

For read and ingest data into influxdb database, is need to configure the ``[[inputs.mqtt_consumer]]`` on telegraf config file ``telegraf.conf``

