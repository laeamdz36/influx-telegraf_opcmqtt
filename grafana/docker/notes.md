# Summary - Automating deploying of grafana

## COnfiguring security with Docker secrets in ``Grafana``

Configure the admins passwords with secrets:
Admin password secret: ``/run/secrets/admin_password``
Environment variable: ``GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/admin_password``

> [!Note]
> For each secret in Docker compose is need a separated file, in this case for admin and password
> will be needed 2 files  

```
└── 📁Proyect_Folder
    └── 📁config
    └── 📁gf_provisioning
        ├── datasources.yml
    └── 📁secrets
        ├── .env.grafana_admin_password # <- file for password
        ├── .env.grafana_admin_user # <- file for name of admin user
        ├── .env.influxdb_admin_token
    ├── docker-compose.yml
    └── grafana.env
```

In Docker compose the configuration will be:

```yml
services:
  grafana:
    image: grafana/grafana:main-ubuntu
    container_name: grafana01
    restart: unless-stopped
    ports:
      - '3000:3000'
    environment:
        # This settigns will override th conf/grafana.ini
      - GF_DEFAULT_INSTANCE_NAME=GF_Main
      - GF_SECURITY_ADMIN_USER__FILE=/run/secrets/grafana_admin_user
      - GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/grafana_admin_password
      - API_TOKEN__FILE=/run/secrets/influxdb_admin_token
    volumes:
      - grafana-data:/var/lib/grafana
      - ./gf_provisioning:/etc/grafana/provisioning:ro
    secrets:
      - grafana_admin_user
      - grafana_admin_password
      - influxdb_admin_token
    networks:
      - iot-network
```

> [!NOTE]
> For grafana nee to be specified with **__FILE** at the final of the enviroment variable at the final
> as mentioned in the grafana documentation  

## Configuring Grafana

!!! Note
    Do not modify grafana.ini, instead override configurations with enviroment variables override an option 

For Docker :whale2: compose:
> [!NOTE]
> Do not modify grafana.ini, instead override configurations with enviroment variables override an option 

```bash
GF_<SECTION NAME>_<KEY>
```

Where ``<SECTION NAME>`` is the text within the square brackets (``[`` and ``]``) in the configuration file. All letters must be uppercase, periods (.) and dashes (-) must replaced by underscores (_). For example, if you have these configuration settings:


```ini
# default section
instance_name = ${HOSTNAME}

[security]
admin_user = admin

[auth.google]
client_secret = 0ldS3cretKey

[plugin.grafana-image-renderer]
rendering_ignore_https_errors = true

[feature_toggles]
enable = newNavigation
```

You can override variables on Linux machines with:

```bash
export GF_DEFAULT_INSTANCE_NAME=my-instance
export GF_SECURITY_ADMIN_USER=owner
export GF_AUTH_GOOGLE_CLIENT_SECRET=newS3cretKey
export GF_PLUGIN_GRAFANA_IMAGE_RENDERER_RENDERING_IGNORE_HTTPS_ERRORS=true
export GF_FEATURE_TOGGLES_ENABLE=newNavigation
```

### Configuring a image for grafana

There are 2 docker images for grafana
- Grafan enterprise: ``grafana/grafana-enterprise``
- Grafana Open Source: ``grafana/grafana``

Each edition is available in two variants: Alpine and Ubuntu.

### Default paths

The following configurations are set by default when you start the Grafana Docker container. When running in Docker you cannot change the configurations by editing the ``conf/grafana.ini`` file. Instead, you can modify the configuration using ``environment variables.``

| Setting               |             Default value |
| :-------------------- | ------------------------: |
| GF_PATHS_CONFIG       |  /etc/grafana/grafana.ini |
| GF_PATHS_DATA         |          /var/lib/grafana |
| GF_PATHS_HOME         |        /usr/share/grafana |
| GF_PATHS_LOGS         |          /var/log/grafana |
| GF_PATHS_PLUGINS      |  /var/lib/grafana/plugins |
| GF_PATHS_PROVISIONING | /etc/grafana/provisioning |

```yml

```

### Build Grafana with the Image Renderer plugin pre-installed

```bash
# go to the folder
cd packaging/docker/custom

# running the build command
docker build \
  --build-arg "GRAFANA_VERSION=latest" \
  --build-arg "GF_INSTALL_IMAGE_RENDERER_PLUGIN=true" \
  -t grafana-custom .

# running the docker run command
docker run -d -p 3000:3000 --name=grafana grafana-custom
```

> Note: To specify the version of a plugin, you can use the GF_INSTALL_PLUGINS build argument and add the version number. The latest version is used if you don’t specify a version number. For example, you can use --build-arg "GF_INSTALL_PLUGINS=grafana-clock-panel 1.0.1,grafana-simple-json-datasource 1.3.5" to specify the versions of two plugins.

*Example:*

The following example shows how to build and run a custom Grafana Docker image with pre-installed plugins.

```bash
# go to the custom directory
cd packaging/docker/custom

# running the build command
# include the plugins you want e.g. clock planel etc
docker build \
  --build-arg "GRAFANA_VERSION=latest" \
  --build-arg "GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource" \
  -t grafana-custom .

# running the custom Grafana container using the docker run command
docker run -d -p 3000:3000 --name=grafana grafana-custom
```

### Configure Grafana with docker secrets

You can apply this technique to any configuration options in ``conf/grafana.ini`` by setting ``GF_<SectionName>_<KeyName>__FILE``

The following example demonstrates how to set the admin password:

Admin password secret: ``/run/secrets/admin_password``
Environment variable: ``GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/admin_password``


## Provisioning the datasources

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```