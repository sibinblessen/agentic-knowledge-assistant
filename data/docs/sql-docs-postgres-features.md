---
title: Cloud SQL for PostgreSQL features | Google Cloud Documentation
source_url: https://docs.cloud.google.com/sql/docs/postgres/features
license: CC BY 4.0, Google Cloud documentation
---

# Cloud SQL for PostgreSQL features | Google Cloud Documentation

## PostgreSQL features by Cloud SQL editions

For more information about the features for each edition of Cloud SQL for PostgreSQL, see Introduction to Cloud SQL editions.

## PostgreSQL feature support for Cloud SQL

- Fully managed PostgreSQL databases in the cloud.
- Instances available in the Americas, EU, Asia, and Australia. See all locations where you can create Cloud SQL instances.
- Supports migration from source databases to Cloud SQL destination databases using Database Migration Service (DMS).
- Customer data encrypted on Google's internal networks and in database tables, temporary files, and backups.
- Support for secure external connections with the Cloud SQL Auth Proxy or with the SSL/TLS protocol.
- Data replication between multiple zones with automatic failover.
- Import and export databases using SQL dump files.
- Support for PostgreSQL client-server protocol and standard PostgreSQL connectors.
- Automated backups, on-demand backups, and point-in-time recovery.
- Instance cloning.
- Integration with Google Cloud Observability logging and monitoring.
- Support for multiple PostgreSQL versions.
- Logical replication
- Support for read pools and read pool autoscaling
- Storage shrink. For more information, see About storage shrink.

## Supported PostgreSQL extensions for Cloud SQL

Cloud SQL supports many PostgreSQL extensions. For a complete list of these extensions, see Configure PostgreSQL extensions.

## Supported PostgreSQL procedural languages for Cloud SQL

Cloud SQL supports the `PL/pgSQL` SQL procedural
language.

## Supported languages for Cloud SQL for PostgreSQL

You can use Cloud SQL with App Engine applications running in the flexible environment that are written in:

- C#
- Go
- Java
- Node.js
- PHP
- Python
- Ruby

You can also use Cloud SQL with external applications using the standard PostgreSQL client-server protocol.

## How you can connect to Cloud SQL for PostgreSQL instances

You can connect to a Cloud SQL instance from:

- A `psql` client. Learn more.
- Third-party tools that use the standard PostgreSQL client-server protocol.
- External applications. Learn more.
- App Engine applications. Learn more.
- Applications running on Compute Engine. Learn more.
- Applications running on Google Kubernetes Engine. Learn more.
- Cloud Run functions. Learn more.
  - Cloud Run. Learn more.

Connecting to Cloud SQL with Private Google access isn't supported.

## Differences between standard PostgreSQL and Cloud SQL for PostgreSQL

In general, the PostgreSQL functionality provided by a Cloud SQL instance is the same as the functionality provided by a locally-hosted PostgreSQL instance. However, there are a few differences between a standard PostgreSQL instance and a Cloud SQL instance.

### Unsupported features for Cloud SQL for PostgreSQL

- Any feature that requires `SUPERUSER` privileges with the following exceptions:
  - You can use the `CREATE EXTENSION` statement only for supported extensions.
  - If you are assigned to the `cloudsqlsuperuser` role, then you can perform `CREATE CAST` and `DROP CAST` statements. For more information, see Superuser restrictions and privileges.
- The `WITHOUT FUNCTION` cast method.
- Custom background workers.
- The `psql` client in Cloud Shell doesn't support operations that
require a reconnection, such as connecting to a different database using the `\c` command.
- Low-Level Virtual Machine (LLVM) Just-in-Time (JIT) compilation.

### Notable differences between PostgreSQL and Cloud SQL for PostgreSQL

- Some PostgreSQL options and parameters aren't enabled for editing as Cloud SQL flags.
