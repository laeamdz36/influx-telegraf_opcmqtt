
### admin-token-file
Specifies an offline admin ``token file`` to use if no tokens exist when the server starts. Once started, you can interact with the server using the provided token. Offline admin tokens are designed to help with automated deployments.

influxdb3 serve option = --admin-token-file	
Environment variable = INFLUXDB3_ADMIN_TOKEN_FILE

### object-store

Specifies which object storage to use to store Parquet files. This option supports the following values:

memory: Effectively no object persistence
memory-throttled: Like memory but with latency and throughput that somewhat resembles a cloud object store
file: Stores objects in the local filesystem (must also set --data-dir)
s3: Amazon S3 (must also set --bucket, --aws-access-key-id, --aws-secret-access-key, and possibly --aws-default-region)
google: Google Cloud Storage (must also set --bucket and --google-service-account)
azure: Microsoft Azure blob storage (must also set --bucket, --azure-storage-account, and --azure-storage-access-key)

influxdb3 serve option = --object-store	
Environment variable = INFLUXDB3_OBJECT_STORE