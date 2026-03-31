# Main Description

The Compose is integrated by 3 services:
1. Influxdb3 Core
2. Telegraf
3. Influxdb Explorer

# HiveMQ
```bash
docker run --name hivemq-edge -d -p 1883:1883 -p 8080:8080 hivemq/hivemq-edge
```

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

```toml
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

For configuration the explorer service, is need to mount a ``config.json`` file in
the directory ``influxdb\config``

``config.json``

```json
{
    "DEFAULT_INFLUX_SERVER": "http://influxdb3-core:8181",
    "DEFAULT_INFLUX_DATABASE": "main",
    "DEFAULT_API_TOKEN": "the_token_configured_also_for_influxdb3_service",
    "DEFAULT_SERVER_NAME": "Local InfluxDB 3"
}
```

#### Docker secrets with telegraf plugin

References:
[Telegraf Docker Secrets](https://www.influxdata.com/blog/storing-secrets-telegraf/)

To use docker secrets directly in the ``telegraf.conf`` file is needed to configure the plugin ``[[secretstores.docker]]``

Configure the plugin with the basic config:

```toml
[[secretstores.docker]]
  id = "docker_store"
```

Next use the secrets configured in th docker compose:

```yml
  telegraf:
    image: telegraf:1.36.3
    container_name: telegraf
    environment:
      MQTT_BROKER: ${MQTT_BROKER_URL}
      # Configuration output pluguin v2 to write on influxdb3
      INFLUX_SERVICE: influxdb3-core
      INFLUX_PORT: 8181
      DATABASE_NAME: ${INFLUX_DB_NAME}
    user: "1000"
    secrets:
      - influxdbtoken_telegraf
      - mqtt_user
      - mqtt_pass

secrets:
  influxdb_admin_token:
    file: ./secrets/influxdb_admin_token.env
  mqtt_user:
    environment: mqtt_user
  mqtt_pass:
    environment: mqtt_pass
  influxdbtoken_telegraf:
    environment: influxdbtoken_telegraf
```
In the ``telegraf.conf``:

```toml
[[outputs.influxdb_v2]]
  urls = ["http://influxdb3-core:8181"]
  token = "@{docker_store:influxdbtoken_telegraf}"
```

## Ingest data

For read and ingest data into influxdb database, is need to configure the ``[[inputs.mqtt_consumer]]`` on telegraf config file ``telegraf.conf``

```toml
[[outputs.influxdb_v2]]
  urls = ["http://influxdb3-core:8181"]
  token = "@{docker_store:influxdbtoken_telegraf}"
  organization = "ignored"
  bucket = "main"

# Configuration of the host
# [[inputs.cpu]]
#   percpu = true
#   totalcpu = true
#   report_active = true

# [[inputs.mem]]
# [[inputs.disk]]
# [[inputs.system]]

# ************************************
# MQTT CONSUMER
# ************************************
[[inputs.mqtt_consumer]]
  ## MQTT broker URLs to be used. The format should be scheme://host:port,
  ## schema can be tcp, ssl, or ws.
  servers = ["${MQTT_BROKER}"]

  ## Topics that will be subscribed to.
  # topics = [
  #   "pico02/temperature",
  #   "pico02/humidity",
  #   "pico02/pressure",
  #   "pico02/cpu_temp"
  # ]

  # Topic DEV with lineprotocol
  topics = ["pico01/#", "pico02/#"]

  ## QoS policy for messages
    # 0 = at most once
  ##   1 = at least once
  ##   2 = exactly once
  ##
  ## When using a QoS of 1 or 2, you should enable persistent_session to allow
  ## resuming unacknowledged messages.
  qos = 0

  ## If unset, a random client ID will be generated.
  # client_id = "telegraf-infra"

  ## Username and password to connect MQTT server.
  username = "@{docker_store:mqtt_user}"
  password = "@{docker_store:mqtt_pass}"
  data_format = "value"
  data_type = "float"
```

