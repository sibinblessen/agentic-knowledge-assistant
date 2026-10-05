---
title: Quickstart: Deploy a Python (Flask) web app to Google Cloud with Cloud Run | Google Cloud Documentation
source_url: https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service
license: CC BY 4.0, Google Cloud documentation
---

# Quickstart: Deploy a Python (Flask) web app to Google Cloud with Cloud Run | Google Cloud Documentation

# Quickstart: Build and deploy a Python (Flask) web app to Cloud Run

Learn how to use a single command to build and deploy a "Hello World" web application from a code sample to Google Cloud using Cloud Run.

By following the steps in this quickstart, Cloud Run automatically builds a Dockerfile for you when you deploy from source code. For more information on how the Python buildpack determines the default entrypoint for Cloud Run source deployments, see Build a Python application.

## Before you begin

1. Sign in to your Google Cloud account. If you're new to Google Cloud, create an account to evaluate how our products perform in real-world scenarios. New customers also get $300 in free credits to run, test, and deploy workloads.
2. Install the Google Cloud CLI.
3. If you're using an external identity provider (IdP), you must first sign in to the gcloud CLI with your federated identity.
4. To initialize the gcloud CLI, run the following command: `gcloud init`
5. Create or select a Google Cloud project. **Roles required to select or create a project**
  - **Select a project**: Selecting a project doesn't require a specific
      IAM role—you can select any project that you've been
      granted a role on.
  - **Create a project**: To create a project, you need the Project Creator role
      (`roles/resourcemanager.projectCreator`), which contains the `resourcemanager.projects.create` permission. Learn how to grant
      roles.
  - Create a Google Cloud project: gcloud projects create `PROJECT_ID` Replace `PROJECT_ID`
  - Select the Google Cloud project that you created: gcloud config set project `PROJECT_ID` Replace `PROJECT_ID`
6. If you're using an existing project for this guide, verify that you have the permissions required to complete this guide. If you created a new project, then you already have the required permissions.
7. Verify that billing is enabled for your Google Cloud project.
8. Install the Google Cloud CLI.
9. If you're using an external identity provider (IdP), you must first sign in to the gcloud CLI with your federated identity.
10. To initialize the gcloud CLI, run the following command: `gcloud init`
11. Create or select a Google Cloud project. **Roles required to select or create a project**
  - **Select a project**: Selecting a project doesn't require a specific
      IAM role—you can select any project that you've been
      granted a role on.
  - **Create a project**: To create a project, you need the Project Creator role
      (`roles/resourcemanager.projectCreator`), which contains the `resourcemanager.projects.create` permission. Learn how to grant
      roles.
  - Create a Google Cloud project: gcloud projects create `PROJECT_ID` Replace `PROJECT_ID`
  - Select the Google Cloud project that you created: gcloud config set project `PROJECT_ID` Replace `PROJECT_ID`
12. If you're using an existing project for this guide, verify that you have the permissions required to complete this guide. If you created a new project, then you already have the required permissions.
13. Verify that billing is enabled for your Google Cloud project.
14.  To set the default project for your Cloud Run service, run the
  following command:
    gcloud config set project `PROJECT_ID` Replace `PROJECT_ID` with your Google Cloud project ID.
15. If you are under a domain restriction organization policy restricting unauthenticated invocations for your project, you will need to access your deployed service as described under Testing private services.
16. Enable the Cloud Run Admin API and Cloud Build APIs, if any are not already enabled: **Roles required to enable APIs**
To enable APIs, you need the `serviceusage.services.enable` permission. If you
      created the project, then you likely already have this permission through the
      Owner role (`roles/owner`). Otherwise, you can get this permission through the
      Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
      Learn how to grant roles.
gcloud services enable run.googleapis.com cloudbuild.googleapis.com After the Cloud Run Admin API is enabled, the Compute Engine default service account is automatically created.
17. Review Cloud Run pricing or estimate costs with the pricing calculator.

### Required roles

To get the permissions that you need to complete this quickstart, ask your administrator to grant you the following IAM roles:

- Cloud Run Admin  (`roles/run.admin`)
              on the project
- Cloud Run Source Developer  (`roles/run.sourceDeveloper`)
              on the project
- Service Account User  (`roles/iam.serviceAccountUser`)
              on the service identity
- Logs Viewer  (`roles/logging.viewer`)
              on the project

For more information about granting roles, see Manage access to projects, folders, and organizations.

You might also be able to get the required permissions through custom roles or other predefined roles.

### Grant the Cloud Build service account access to your project

Cloud Build automatically uses the Compute Engine default service account as the default Cloud Build service account to build your source code and Cloud Run resource, unless you override this behavior.

For Cloud Build to build your sources, grant the Cloud Build service
account the Cloud Run
Builder
(`roles/run.builder`) role on your project:

gcloud projects add-iam-policy-binding `PROJECT_ID` \
    --member=serviceAccount:`SERVICE_ACCOUNT_EMAIL_ADDRESS` \
    --role=roles/run.builder

Replace `PROJECT_ID``SERVICE_ACCOUNT_EMAIL_ADDRESS`

`PROJECT_NUMBER`-compute@developer.gserviceaccount.com

Replace `PROJECT_NUMBER`

For detailed instructions on how to find your project ID, and project number, see Creating and managing projects.

Granting the Cloud Run builder role takes a couple of minutes to propagate.

## Write the sample application

To write an application in Python:

1. Create a new directory named `helloworld` and change directory
into it:
```
mkdir helloworld
cd helloworld
```
2. Create a file named `main.py` and paste the following code into it:
This code responds to requests with our "Hello World" greeting. HTTP
handling is done by a Gunicorn web server in the container. When
directly invoked for local use, this code creates a basic web server that
listens on the port defined by the
`PORT` environment variable.
3. Create a file named `requirements.txt` and paste the following code into it:
```
Flask~=3.0
gunicorn~=23.0
Werkzeug~=3.0
```
This code adds packages needed by the sample.

Your app is finished and ready to be deployed.

## Deploy to Cloud Run from source

Deploy from source automatically builds a container image from source code and deploys it.

To deploy from source:

1. In your source code directory, deploy the current folder using the following command: gcloud run deploy --source . 
  1. When you are prompted for the service name, press Enter to accept the
default name, for example `helloworld`.
  2. If you are prompted to enable additional APIs on the project,
for example, the Artifact Registry API, respond by pressing
`y`.
  3. When you are prompted for region: select the region
of your choice, for example `europe-west1`.
  4. If you are prompted to create a repository in the specified region, respond by pressing `y`.
  5. If you are prompted to *allow public access*:
respond `y`. You might not see this prompt if there is a domain
restriction organization policy that prevents it; for more details see the
Before you begin section.
Then wait a few moments until the deployment is complete. On success, the command line displays the service URL.
2. Visit your deployed service by opening the service URL in a web browser.

### Cloud Run locations

Cloud Run is regional, which means the infrastructure that
runs your Cloud Run services is located in a specific region and is
managed by Google to be redundantly available across
all the zones within that region.

Meeting your latency, availability, or durability requirements are primary
factors for selecting the region where your Cloud Run services are run.
You can generally select the region nearest to your users but you should consider
the location of the other Google Cloud
products that are used by your Cloud Run service.
Using Google Cloud products together across multiple locations can affect
your service's latency as well as cost.

Cloud Run is available in the following regions:

#### Subject to Tier 1 pricing

- `asia-east1` (Taiwan)
- `asia-northeast1` (Tokyo)
- `asia-northeast2` (Osaka)
- `asia-south1` (Mumbai, India)
- `asia-southeast3` (Bangkok)
- `europe-north1` (Finland) 
 Low CO<sub>2</sub>
- `europe-north2` (Stockholm) 
 Low CO<sub>2</sub>
- `europe-southwest1` (Madrid) 
 Low CO<sub>2</sub>
- `europe-west1` (Belgium) 
 Low CO<sub>2</sub>
- `europe-west4` (Netherlands) 
 Low CO<sub>2</sub>
- `europe-west8` (Milan) 
 Low CO<sub>2</sub>
- `europe-west9` (Paris) 
 Low CO<sub>2</sub>
- `me-west1` (Tel Aviv)
- `northamerica-south1` (Mexico)
- `us-central1` (Iowa) 
 Low CO<sub>2</sub>
- `us-east1` (South Carolina)
- `us-east4` (Northern Virginia)
- `us-east5` (Columbus)
- `us-south1` (Dallas) 
 Low CO<sub>2</sub>
- `us-west1` (Oregon) 
 Low CO<sub>2</sub>

#### Subject to Tier 2 pricing

- `africa-south1` (Johannesburg)
- `asia-east2` (Hong Kong)
- `asia-northeast3` (Seoul, South Korea)
- `asia-southeast1` (Singapore)
- `asia-southeast2` (Jakarta)
- `asia-south2` (Delhi, India)
- `australia-southeast1` (Sydney)
- `australia-southeast2` (Melbourne)
- `europe-central2` (Warsaw, Poland) 
 Low CO<sub>2</sub>
- `europe-west10` (Berlin)
- `europe-west12` (Turin) 
 Low CO<sub>2</sub>
- `europe-west2` (London, UK) 
 Low CO<sub>2</sub>
- `europe-west3` (Frankfurt, Germany)
- `europe-west6` (Zurich, Switzerland) 
 Low CO<sub>2</sub>
- `me-central1` (Doha)
- `me-central2` (Dammam)
- `northamerica-northeast1` (Montreal) 
 Low CO<sub>2</sub>
- `northamerica-northeast2` (Toronto) 
 Low CO<sub>2</sub>
- `southamerica-east1` (Sao Paulo, Brazil) 
 Low CO<sub>2</sub>
- `southamerica-west1` (Santiago, Chile) 
 Low CO<sub>2</sub>
- `us-west2` (Los Angeles)
- `us-west3` (Salt Lake City)
- `us-west4` (Las Vegas)

If you already created a Cloud Run service, you can view the region in the Cloud Run dashboard in the Google Cloud console.

## Clean up

To avoid additional charges to your Google Cloud account, delete all the resources you deployed with this quickstart.

### Delete your repository

Cloud Run doesn't charge you when your deployed service isn't in use. However, you might still be charged for storing the container image in Artifact Registry. To delete Artifact Registry repositories, follow the steps in Delete repositories in the Artifact Registry documentation.

### Delete your service

Cloud Run services don't incur costs until they receive requests. To delete your Cloud Run service, follow one of these steps:

### Console

To delete a service:

1. In the Google Cloud console, go to the Cloud Run **Services** page:
Go to Cloud Run
2. Locate the service you want to delete in the services list, and click its checkbox to select it.
3. Click **Delete**. This deletes all revisions of the service.

### gcloud

To delete a service, run the following command:

gcloud run services delete `SERVICE` --region `REGION`

Replace the following:

- `SERVICE`: name of your service.
- `REGION`: Google Cloud region of the service.

### Delete your test project

Deleting your Google Cloud project stops billing for all resources in that project. To release all Google Cloud resources in your project, follow these steps:

Delete a Google Cloud project:

gcloud projects delete `PROJECT_ID`

## What's next

For more information on building a container from code source and pushing to a repository, see:
