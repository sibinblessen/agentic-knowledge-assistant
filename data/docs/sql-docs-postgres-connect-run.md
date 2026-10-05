---
title: Connect from Cloud Run | Cloud SQL for PostgreSQL | Google Cloud Documentation
source_url: https://docs.cloud.google.com/sql/docs/postgres/connect-run
license: CC BY 4.0, Google Cloud documentation
---

# Connect from Cloud Run | Cloud SQL for PostgreSQL | Google Cloud Documentation

This page contains information and examples for connecting to a Cloud SQL instance from a service running in Cloud Run.

**For step-by-step instructions on running a Cloud Run sample web
   application connected to Cloud SQL,** see the
   quickstart for connecting
   from Cloud Run.

Cloud SQL is a fully-managed database service that helps you set up, maintain, manage, and administer your relational databases in the cloud.

Cloud Run is a managed compute platform that lets you run containers directly on top of Google Cloud infrastructure.

## Set up a Cloud SQL instance

1. Enable the Cloud SQL Admin API in the Google Cloud project that you are connecting from, if you
   haven't already done so:
  
  
  
  
**Roles required to enable APIs**
To enable APIs, you need the `serviceusage.services.enable` permission. If you
          created the project, then you likely already have this permission through the
          Owner role (`roles/owner`). Otherwise, you can get this permission through the
          Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
          Learn how to grant roles.
Enable the API
2. Create a Cloud SQL
  for PostgreSQL instance. We recommend that you choose a Cloud SQL 
  instance location in the same region as your Cloud Run service for better latency, to avoid some networking costs, and to reduce
  cross region failure risks.
  By default, Cloud SQL assigns a public IP address to a new instance. You also have the option to assign a private IP address. For more information about the connectivity options for both, see the Connecting Overview page.
3. When you create the instance, you can choose the 
   server certificate (CA) hierarchy for the instance and then configure the hierarchy
   as the `serverCaMode` for the instance. You must select the
   per-instance CA option (`GOOGLE_MANAGED_INTERNAL_CA`) as the server CA mode
   for instances that you want to connect to from
   web applications.

## Configure Cloud Run

The steps to configure Cloud Run depend on the type of IP address that you assigned to your Cloud SQL instance. If you route all egress traffic through Direct VPC egress or a Serverless VPC Access connector, use a private IP address. For a comparison of the two egress methods, see Compare Direct VPC egress with VPC connectors.
### Public IP (default)


- Make sure that the instance has a public IP address. You can
   verify this on the **Overview** page for your instance in the
   Google Cloud console.
   If you need to add one, see the
   Configuring public IP page
   for instructions.
- Get the `INSTANCE_CONNECTION_NAME` for your instance. You can find
  this value on the **Overview** page for your instance in the
  Google Cloud console or by running the
  following `gcloud sql instances describe` command: gcloud sql instances describe `INSTANCE_NAME` Replace `INSTANCE_NAME` with the name of your Cloud SQL
   instance.
- Get the `CLOUD_RUN_SERVICE_ACCOUNT_NAME` for your Cloud Run
  service. You can find this value on the **IAM** page of the
  project that's hosting the Cloud Run service in the
  Google Cloud console or by
  running the following `gcloud run services describe` command in the project that's hosting the Cloud Run service: gcloud run services describe `CLOUD_RUN_SERVICE_NAME` --region `CLOUD_RUN_SERVICE_REGION` --format="value(spec.template.spec.serviceAccountName)"
   
   Replace the following variables:
  - `CLOUD_RUN_SERVICE_NAME`: the name of your Cloud Run service
  - `CLOUD_RUN_SERVICE_REGION`: the region of your Cloud Run service
- 
  Configure the service account for your Cloud Run service. To
  connect to Cloud SQL, make sure that the service account has the
  `Cloud SQL Client` IAM role.
- If you're adding a Cloud SQL connection to a new service, you need to have your service containerized and uploaded to the Container Registry or Artifact Registry. If you don't already have a connection, then see these instructions about building and deploying a container image.
- If you're connecting to
    instances that are configured with the shared certificate authority (CA)
    (`GOOGLE_MANAGED_CAS_CA`) option or the customer-managed CA
    (`CUSTOMER_MANAGED_CAS_CA`) option as the
    server CA mode,
    then select the second generation execution environment when you
    select the
    execution environment for the service.
    Both server CA mode options require you to connect to the instance
    with the Cloud SQL Auth Proxy v2.
If your service runs in a first generation execution environment, then
    you can connect only to Cloud SQL instances that are configured with
    the per-instance certificate authority (CA) option
    (`GOOGLE_MANAGED_INTERNAL_CA`) as the server CA mode. The first
    generation execution environment of Cloud Run embeds the Cloud SQL Auth Proxy
    v1. For more information about connection requirements to Cloud SQL
    for the Cloud SQL Auth Proxy,
    see Requirements for using the Cloud SQL Auth Proxy.

Like any configuration change, setting a new configuration for the Cloud SQL connection leads to the creation of a new Cloud Run revision. Subsequent revisions will also automatically get this Cloud SQL connection unless you make explicit updates to change it.

### Console

1. Go to Cloud Run
2. Start configuring the service. To add Cloud SQL connections to an existing service, do the following: 
  1. From the **Services** list, click the service name you want.
  2. Click **Edit & deploy new revision**.
3. Enable connecting to a Cloud SQL instance:
           
            
  1. Click **Container(s)** and then **Settings**.
  2. Scroll to **Cloud SQL connections**.
  3. Click **Add connection**.
  4. Click **Enable the Cloud SQL Admin** button if you haven't
                  enabled the Cloud SQL Admin API yet.
  - If you're adding a connection to a Cloud SQL instance in your project, then select the Cloud SQL instance you want from the menu.
  - If you're using a Cloud SQL instance from another
                     project, then select **custom connection string** in
                     the menu and enter the full instance connection name in the
                     format `PROJECT-ID:REGION:INSTANCE-ID`.
  - To delete a connection, hold your cursor to the
                     right of the connection to display the 
                     **Delete** icon, and click it.
4. Click **Create** or **Deploy**.

### Command line

Before using any of the following commands, make the following replacements:

- `IMAGE` with the image you're deploying
- `SERVICE_NAME` with the name of your Cloud Run service
- `INSTANCE_CONNECTION_NAME` with the instance connection name of
               your Cloud SQL instance, or a comma delimited list of
               connection names.
If you're deploying a new container, use the following command: gcloud run deploy \ --image= `IMAGE` \
  --add-cloudsql-instances=`INSTANCE_CONNECTION_NAME` If you're updating an existing service, use the following command: gcloud run services update `SERVICE_NAME` \
  --add-cloudsql-instances=`INSTANCE_CONNECTION_NAME`

### Terraform

The following code creates a base Cloud Run container, with a connected Cloud SQL instance.

1. 
            Apply the changes by entering `terraform apply`.
2. 
            Verify the changes by checking the Cloud Run service, clicking the **Revisions** tab, and then the **Connections** tab.

### Private IP

If the authorizing service account belongs to a different project than the one containing the Cloud SQL instance, do the following:

- In both projects, enable the Cloud SQL Admin API.
- For the service account in the project that contains the Cloud SQL instance, add the IAM permissions.

Direct VPC egress and connectors use private IP addresses to handle communication to your VPC network. To connect directly with private IP addresses using one of these egress methods, do the following:

1. Make sure that the Cloud SQL instance created previously has a private IP address. To add an internal IP address, see Configure private IP.
2. Configure your egress method to connect to the same VPC network as your Cloud SQL instance. Note the following conditions:
3. Direct VPC egress and Serverless VPC Access both support communication to VPC networks connected using Cloud VPN and VPC Network Peering.
4. Direct VPC egress and Serverless VPC Access don't support legacy networks.
5. Unless you're using Shared VPC, a connector must share the same project and region as the resource that uses it, although the connector can send traffic to resources in different regions.
6. Connect using your instance's private IP address and port `5432`.

## Connect to Cloud SQL

After you configure Cloud Run, you can connect to your Cloud SQL instance.

### Public IP (default)



For public IP paths, Cloud Run can be set up to use the Cloud SQL Auth Proxy for encryption in two ways:

- Through Unix sockets
- By using a Cloud SQL connector

### Use Secret Manager

Google recommends that you use Secret Manager to store sensitive information such as SQL credentials. You can pass secrets as environment variables or mount as a volume with Cloud Run.

After creating a secret in Secret Manager, update an existing service, with the following command:

### Command line

gcloud run services update `SERVICE_NAME` \
  --add-cloudsql-instances=`INSTANCE_CONNECTION_NAME`
  --update-env-vars=INSTANCE\_CONNECTION\_NAME=`INSTANCE_CONNECTION_NAME_SECRET` \
  --update-secrets=DB\_USER=`DB_USER_SECRET`:latest \
  --update-secrets=DB\_PASS=`DB_PASS_SECRET`:latest \
  --update-secrets=DB\_NAME=`DB_NAME_SECRET`:latest

### Terraform

The following creates secret resources to securely hold the database user, password, and name values using `google_secret_manager_secret` and `google_secret_manager_secret_version`. Note that you must update the project compute service account to have access to each secret.

Update the main Cloud Run resource to include the new secrets.

Apply the changes by entering `terraform apply`.

The example command uses the secret version, `latest`; however, Google recommends
    pinning the secret to a specific version, `SECRET_NAME:v1`.

### Private IP

For private IP paths, your application connects directly to your instance through a VPC network. This method uses TCP to connect directly to the Cloud SQL instance without using the Cloud SQL Auth Proxy.

### Connect with TCP

Connect using the private IP address of your Cloud SQL instance as the host and port `5432`.

### Python

To see this snippet in the context of a web application, view the README on GitHub.

### Java

To see this snippet in the context of a web application, view the README on GitHub.

Note:

- CLOUD\_SQL\_CONNECTION\_NAME should be represented as \<MY-PROJECT>:\<INSTANCE-REGION>:\<INSTANCE-NAME>
- Using the argument ipTypes=PRIVATE will force the SocketFactory to connect with an instance's associated private IP
- See the JDBC socket factory version requirements for the pom.xml file.

### Node.js

To see this snippet in the context of a web application, view the README on GitHub.

### Go

To see this snippet in the context of a web application, view the README on GitHub.

### C#

To see this snippet in the context of a web application, view the README on GitHub.

### Ruby

To see this snippet in the context of a web application, view the README on GitHub.

### PHP

To see this snippet in the context of a web application, view the README on GitHub.

## Best practices and other information

You can use the Cloud SQL Auth Proxy when testing your application locally. See the quickstart for using the Cloud SQL Auth Proxy for detailed instructions.

You can also test using the Cloud SQL Proxy via a docker container.

### Connection Pools

Connections to underlying databases may be dropped, either by the database server itself, or by the platform infrastructure. We recommend using a client library that supports connection pools that automatically reconnect broken client connections. You can use Managed Connection Pooling with your Cloud SQL instances, which lets you scale your workloads by optimizing resource utilization and connection latency for your Cloud SQL instances using pooling. For detailed information about Managed Connection Pooling, see Managed Connection Pooling overview.

For more detailed examples on how to use connection pools, see the Managing database connections page.

### Connection Limits

Both the MySQL and PostgreSQL editions of Cloud SQL impose a maximum limit on concurrent connections, and these limits may vary depending on the database engine chosen (see the Cloud SQL Quotas and Limits page).

Cloud Run container instances are limited to 100 connections to a Cloud SQL database. Each instance of a Cloud Run service or job can have 100 connections to the database, and as this service or job scales, the total number of connections per deployment can grow.

You can limit the maximum number of connections used per instance by using a connection pool. For more detailed examples on how to limit the number of connections, see the Managing database connections page.

### API Quota Limits

Cloud Run provides a mechanism that connects using the Cloud SQL Auth Proxy, which uses the Cloud SQL Admin API. API quota limits apply to the Cloud SQL Auth Proxy. The Cloud SQL Admin API quota used is approximately two times the number of Cloud SQL instances configured by the number of Cloud Run instances of a particular service deployed at any one time. You can cap or increase the number of Cloud Run instances to modify the expected API quota consumed.

## What's next

- Learn more about Cloud Run.
- Learn more about building and deploying container images.
- See a complete example in Python for using Cloud Run with PostgreSQL.
