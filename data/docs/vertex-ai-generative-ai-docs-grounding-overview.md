---
title: Grounding overview | Gemini Enterprise Agent Platform | Google Cloud Documentation
source_url: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/overview
license: CC BY 4.0, Google Cloud documentation
---

# Grounding overview | Gemini Enterprise Agent Platform | Google Cloud Documentation

In generative AI, grounding is the ability to connect model output to verifiable sources of information. If you provide models with access to specific data sources, then grounding tethers their output to these data and reduces the chances of inventing content. This is particularly important in situations where accuracy and reliability are significant.

Grounding provides the following benefits:

- Reduces model hallucinations, which are instances where the model generates content that isn't factual.
- Anchors model responses to your data sources.
- Provides auditability by providing grounding support, which are links to sources.

You can ground supported-model output in Gemini Enterprise Agent Platform in the following ways:

| **Grounding type** | **Description** | 
|---|---|
| Grounding with Google Search | Connect your model to world knowledge and a wide possible range of topics using results from Google's search engine. | 
| Grounding with Google Maps | Use Google Maps data with your model to provide more accurate and context-aware responses to your prompts, including geospatial context. | 
| Grounding with Agent Search | Use retrieval-augmented generation (RAG) to connect your model to your website data or your sets of documents stored in Agent Search. | 
| Grounding with RAG Engine on Gemini Enterprise Agent Platform | Ground using your data through RAG Engine on Gemini Enterprise Agent Platform, which is a configurable managed RAG service. | 
| Grounding with Elasticsearch | Use retrieval-augmented generation with your existing Elasticsearch indexes and Gemini. | 
| Grounding with your search API | Connect Gemini to your external data sources by grounding with any search API. | 
| Web Grounding for Enterprise | Use a web index suitable for highly-regulated industries to generate grounded responses with compliance controls. | 
| Grounding with Parallel web search | Connect Gemini to an LLM-optimized web index to use the most recent information from the web. | 

For language support, see Supported languages for prompts.

## What's next

- To learn more about responsible AI best practices and Gemini Enterprise Agent Platform's safety filters, see Responsible AI.
