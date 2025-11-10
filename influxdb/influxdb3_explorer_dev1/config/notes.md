Need to create a token as example as --admin
with the line

```bash
docker exec -it <Name_of_the_service_InfluxDB3> influxdb3 create token --admin
```

example:
```bash
docker exec -it influxdb3_core influxdb3 create token --admin
```

# References for creation fo tokens

[InfluxDB3 Creation token](https://docs.influxdata.com/influxdb3/core/reference/cli/influxdb3/create/token/)
