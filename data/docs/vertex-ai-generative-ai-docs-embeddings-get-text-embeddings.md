---
title: Get text embeddings | Gemini Enterprise Agent Platform | Google Cloud Documentation
source_url: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/embeddings/get-text-embeddings
license: CC BY 4.0, Google Cloud documentation
---

# Get text embeddings | Gemini Enterprise Agent Platform | Google Cloud Documentation

This document describes how to create a text embedding using the Gemini Enterprise Agent Platform Text embeddings API.

Gemini Enterprise Agent Platform text embeddings API uses dense vector representations: gemini-embedding-001, for example, uses 3072-dimensional vectors. Dense vector embedding models use deep-learning methods similar to the ones used by large language models. Unlike sparse vectors, which tend to directly map words to numbers, dense vectors are designed to better represent the meaning of a piece of text. The benefit of using dense vector embeddings in generative AI is that instead of searching for direct word or syntax matches, you can better search for passages that align to the meaning of the query, even if the passages don't use the same language.

The vectors are normalized, so you can use cosine similarity, dot product, or Euclidean distance to provide the same similarity rankings.

- To learn more about embeddings, see the embeddings APIs overview.
- To learn about text embedding models, see Text embeddings.
- For information about which languages each embeddings model supports, see Supported text languages.

## Before you begin

1. Sign in to your Google Cloud account. If you're new to Google Cloud, create an account to evaluate how our products perform in real-world scenarios. New customers also get $300 in free credits to run, test, and deploy workloads.
2. In the Google Cloud console, on the project selector page, select or create a Google Cloud project. **Roles required to select or create a project**
  - **Select a project**: Selecting a project doesn't require a specific
      IAM role—you can select any project that you've been
      granted a role on.
  - **Create a project**: To create a project, you need the Project Creator role
      (`roles/resourcemanager.projectCreator`), which contains the `resourcemanager.projects.create` permission. Learn how to grant
      roles.
Go to project selector
3. Enable the Agent Platform API, if it is not already enabled. **Roles required to enable APIs**
To enable APIs, you need the `serviceusage.services.enable` permission. If you
          created the project, then you likely already have this permission through the
          Owner role (`roles/owner`). Otherwise, you can get this permission through the
          Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
          Learn how to grant roles.
Enable the API
4. In the Google Cloud console, on the project selector page, select or create a Google Cloud project. **Roles required to select or create a project**
  - **Select a project**: Selecting a project doesn't require a specific
      IAM role—you can select any project that you've been
      granted a role on.
  - **Create a project**: To create a project, you need the Project Creator role
      (`roles/resourcemanager.projectCreator`), which contains the `resourcemanager.projects.create` permission. Learn how to grant
      roles.
Go to project selector
5. Enable the Agent Platform API, if it is not already enabled. **Roles required to enable APIs**
To enable APIs, you need the `serviceusage.services.enable` permission. If you
          created the project, then you likely already have this permission through the
          Owner role (`roles/owner`). Otherwise, you can get this permission through the
          Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
          Learn how to grant roles.
Enable the API
6. Choose a task type for your embeddings job.

### API limits

For each request, you're limited to 250 input texts. The API has a maximum input
token limit of 20,000. Inputs exceeding this limit result in a 400 error. Each
individual input text is further limited to 2048 tokens; any excess is silently
truncated. You can also disable silent truncation by setting `autoTruncate` to
`false`.

For more information, see Text embedding limits.

## Get text embeddings for a snippet of text

You can get text embeddings for a snippet of text by using the Agent Platform API or the Agent Platform SDK for Python.

### Choose an embedding dimension

All models produce a full-length embedding vector by default. For
`gemini-embedding-001`, this vector has 3072 dimensions, and other
models produce 768-dimensional vectors. However, by using the
`output_dimensionality` parameter, users can control the size of the output
embedding vector. Selecting a smaller output dimensionality can save storage
space and increase computational efficiency for downstream applications, while
sacrificing little in terms of quality.

The following examples use the `gemini-embedding-001` model.

### Python

#### Install

pip install --upgrade google-genai

To learn more, see the SDK reference documentation.

Set environment variables to use the Google Gen AI SDK with Vertex AI:

\# Replace the \`GOOGLE\_CLOUD\_PROJECT\` and \`GOOGLE\_CLOUD\_LOCATION\` values
# with appropriate values for your project.
export GOOGLE\_CLOUD\_PROJECT=`GOOGLE_CLOUD_PROJECT`
export GOOGLE\_CLOUD\_LOCATION=`global`
export GOOGLE\_GENAI\_USE\_ENTERPRISE=True

### Go

Learn how to install or update the Go.

To learn more, see the SDK reference documentation.

Set environment variables to use the Google Gen AI SDK with Vertex AI:

\# Replace the \`GOOGLE\_CLOUD\_PROJECT\` and \`GOOGLE\_CLOUD\_LOCATION\` values
# with appropriate values for your project.
export GOOGLE\_CLOUD\_PROJECT=`GOOGLE_CLOUD_PROJECT`
export GOOGLE\_CLOUD\_LOCATION=`global`
export GOOGLE\_GENAI\_USE\_ENTERPRISE=True

### Node.js

#### Install

npm install @google/genai

To learn more, see the SDK reference documentation.

Set environment variables to use the Google Gen AI SDK with Vertex AI:

\# Replace the \`GOOGLE\_CLOUD\_PROJECT\` and \`GOOGLE\_CLOUD\_LOCATION\` values
# with appropriate values for your project.
export GOOGLE\_CLOUD\_PROJECT=`GOOGLE_CLOUD_PROJECT`
export GOOGLE\_CLOUD\_LOCATION=`global`
export GOOGLE\_GENAI\_USE\_ENTERPRISE=True

### Java

Learn how to install or update the Java.

To learn more, see the SDK reference documentation.

Set environment variables to use the Google Gen AI SDK with Vertex AI:

\# Replace the \`GOOGLE\_CLOUD\_PROJECT\` and \`GOOGLE\_CLOUD\_LOCATION\` values
# with appropriate values for your project.
export GOOGLE\_CLOUD\_PROJECT=`GOOGLE_CLOUD_PROJECT`
export GOOGLE\_CLOUD\_LOCATION=`global`
export GOOGLE\_GENAI\_USE\_ENTERPRISE=True

### REST

Before using any of the request data, make the following replacements:

- `PROJECT_ID`: 
Your project ID.
.
- `TEXT`: The text that you want to generate embeddings
    for. **Limit:** five texts of up to 2,048 tokens per text for all models except `textembedding-gecko@001`. The max input token length for `textembedding-gecko@001` is 3072. For `gemini-embedding-001`, each request can only include a single input text. For more information, see Text embedding limits.
- `AUTO_TRUNCATE`: If set to `false`, text that exceeds the token limit causes the request to fail. The default
    value is `true`.

HTTP method and URL:

POST https://us-central1-aiplatform.googleapis.com/v1/projects/`PROJECT_ID`/locations/us-central1/publishers/google/models/gemini-embedding-001:predict

Request JSON body:

```
{
  "instances": [
    { "content": "
```
`TEXT`"}
  ],
  "parameters": { 
    "autoTruncate": `AUTO_TRUNCATE` 
  }
}
To send your request, choose one of these options:

#### curl

Save the request body in a file named `request.json`,
      and execute the following command:

curl -X POST \

-H "Authorization: Bearer $(gcloud auth print-access-token)" \

-H "Content-Type: application/json; charset=utf-8" \

-d @request.json \

"https://us-central1-aiplatform.googleapis.com/v1/projects/`PROJECT_ID`/locations/us-central1/publishers/google/models/gemini-embedding-001:predict"

#### PowerShell

Save the request body in a file named `request.json`,
      and execute the following command:

$cred = gcloud auth print-access-token

$headers = @{ "Authorization" = "Bearer $cred" }

Invoke-WebRequest \`

-Method POST \`

-Headers $headers \`

-ContentType: "application/json; charset=utf-8" \`

-InFile request.json \`

-Uri "https://us-central1-aiplatform.googleapis.com/v1/projects/`PROJECT_ID`/locations/us-central1/publishers/google/models/gemini-embedding-001:predict" | Select-Object -Expand Content

You should receive a JSON response similar to the following. Note that `values`
  has been truncated to save space.

#### Example curl command

```
MODEL_ID="gemini-embedding-001"
PROJECT_ID=
```
`PROJECT_ID`
curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
https://us-central1-aiplatform.googleapis.com/v1/projects/`PROJECT_ID`/locations/us-central1/publishers/google/models/${MODEL_ID}:predict -d \
$'{
  "instances": [
    { "content": "What is life?"}
  ],
}'
## Supported models

The following tables show the available Google and open text embedding models.

### Google models

You can get text embeddings by using the following models:

| Model name | Description | Output Dimensions | Max sequence length | Supported text languages | 
|---|---|---|---|---|
| `gemini-embedding-001` | State-of-the-art performance across English, multilingual and code tasks. It unifies the previously specialized models like `text-embedding-005` and `text-multilingual-embedding-002` and achieves better performance in their respective domains. Read our Tech Report for more detail. | up to 3072 | 2048 tokens | Supported text languages | 
| `text-embedding-005` | Specialized in English and code tasks. | up to 768 | 2048 tokens | English | 
| `text-multilingual-embedding-002` | Specialized in multilingual tasks. | up to 768 | 2048 tokens | Supported text languages | 

For superior embedding quality, `gemini-embedding-001` is our large
model designed to provide the highest performance.

### Open models

You can get text embeddings by using the following models:

| Model name | Description | Output dimensions | Max sequence length | Supported text languages | 
|---|---|---|---|---|
| `multilingual-e5-small` | Part of the E5 family of text embedding models. Small variant contains 12 layers. | Up to 384 | 512 tokens | Supported languages | 
| `multilingual-e5-large` | Part of the E5 family of text embedding models. Large variant contains 24 layers. | Up to 1024 | 512 tokens | Supported languages | 

To get started, see the E5 family model card. For more information on open models, see Open models for MaaS

## Add an embedding to a vector database

After you've generated your embedding you can add embeddings to a vector database, like Vector Search. This enables low-latency retrieval, and is critical as the size of your data increases.

To learn more about Vector Search, see Overview of Vector Search.

## What's next

- To learn more about rate limits, see Agent Platform quotas and system limits.
- To get batch predictions for embeddings, see Get batch text embeddings
inferences
  - To learn more about multimodal embeddings, see Get multimodal embeddings
- To tune an embedding, see Tune text embeddings
- To learn more about the research behind `text-embedding-005` and `text-multilingual-embedding-002`, see the research paper Gecko: Versatile
Text Embeddings Distilled from Large Language
Models.
