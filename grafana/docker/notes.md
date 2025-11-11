## Summary

Configure the admins passwords with secrets:
Admin password secret: ``/run/secrets/admin_password``
Environment variable: ``GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/admin_password``

1. Do not modiry grafana.ini, instead override configurations with enviroment variables
override an option 

Where ``<SECTION NAME>`` is the text within the square brackets (``[`` and ``]``) in the configuration file. All letters must be uppercase, periods (.) and dashes (-) must replaced by underscores (_). For example, if you have these configuration settings:

```bash
GF_<SECTION NAME>_<KEY>
```

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

Setting	Default value
GF_PATHS_CONFIG	/etc/grafana/grafana.ini
GF_PATHS_DATA	/var/lib/grafana
GF_PATHS_HOME	/usr/share/grafana
GF_PATHS_LOGS	/var/log/grafana
GF_PATHS_PLUGINS	/var/lib/grafana/plugins
GF_PATHS_PROVISIONING	/etc/grafana/provisioning

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