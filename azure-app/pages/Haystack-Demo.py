import streamlit as st 
from transformers import T5Tokenizer, T5ForConditionalGeneration
from tqdm.auto import tqdm
from pathlib import Path
# Azure imports
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from requests_aws4auth import AWS4Auth

# Haystack imports
from haystack.document_stores import InMemoryDocumentStore, OpenSearchDocumentStore
from haystack.nodes import (
    BM25Retriever, 
    EmbeddingRetriever, 
    PromptModel,
    PromptNode, 
    PromptTemplate, 
    AnswerParser
)
from haystack.pipelines import Pipeline
from haystack.schema import Document
from haystack.utils import print_questions, print_answers

keyVaultName = '<key_vault_name>'
KVUri = f"https://{keyVaultName}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

aws_access_key = client.get_secret('aws-access-key').value
aws_secret_key = client.get_secret('aws-secret-key').value
azure_oai_api_key = client.get_secret('azure-oai-api-key').value
opensearch_host = client.get_secret('aws-opensearch-host').value

# Authenticate to AWS opensearch instance
region = 'eu-west-2'
service = 'es' 
awsauth = AWS4Auth(aws_access_key, aws_secret_key, region, service)

st.set_page_config(
    page_title="Gen AI <> Haystack Demo",
    page_icon="🤖",
)
st.write("## Gen AI <> Haystack Demo")
st.sidebar.success("Gen AI <> Haystack Demo 🤖")

## If you want to use an open source model for queries
MODEL = 'google/flan-t5-small'

# Create a custom supported prompt using PromptTemplate
user_prompt = PromptTemplate(prompt="""Synthesize a comprehensive answer from the following topk most relevant paragraphs and the given question. 
                             Provide a clear and concise response that summarizes the key points and information presented in the paragraphs. 
                             Your answer should be in your own words and be no longer than 100 words. 
                             \n\n Paragraphs: {join(documents)} \n\n Question: {query} \n\n Answer:""",
                             output_parser=AnswerParser(),) 

@st.cache_resource(show_spinner=False)
def start_opensearch():# Instantiate in-memory document store. In production, you would use a persistent vector database such as OpenSearch
    document_store = OpenSearchDocumentStore(
        host = opensearch_host,
        port = 443,
        aws4auth = awsauth,                                        
        scheme="https",
        verify_certs=True,
        username=None,
        password=None,
        similarity = 'cosine'
    )
    return document_store

@st.cache_resource(show_spinner=False)
def start_bm25_retriever(_doc_store):
    retriever = BM25Retriever(_doc_store)
    return retriever

@st.cache_resource(show_spinner=False)
def start_embedding_retriever(_doc_store):
    retriever = EmbeddingRetriever(
        document_store = _doc_store,
        embedding_model="sentence-transformers/all-mpnet-base-v2"
    )
    return retriever

@st.cache_resource(show_spinner=False)
def get_azure_ai_pipe(_retriever):
    api_key = azure_oai_api_key
    deployment_name = '<azure_oai_deployment_name>' 
    base_url = '<azure_oai_base_url>' 
    azure_prompt = PromptModel(
        model_name_or_path="gpt-4",
        api_key=api_key,
        model_kwargs={
            "api_version": "<api_version>",
            "azure_deployment_name": deployment_name,
            "azure_base_url": base_url,
            "max_tokens": 2000
        },
    )
    azure_prompt_node = PromptNode(azure_prompt, default_prompt_template=user_prompt)
    pipe = Pipeline()
    pipe.add_node(component=embedding_retriever, name="retriever", inputs=["Query"])
    pipe.add_node(component=azure_prompt_node, name="prompt_node", inputs=["retriever"])
    return pipe


@st.cache_resource(show_spinner=False)
def load_model(model_name):
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return model, tokenizer

## If you want to use an open source model for queries
# model, tokenizer = load_model(MODEL)
opensearch_store = start_opensearch()
bm25_retriever = start_bm25_retriever(opensearch_store)
embedding_retriever = start_embedding_retriever(opensearch_store)
azure_ai_pipe = get_azure_ai_pipe(embedding_retriever)

def main():
    '''Applies a query to your Document Store'''
    st.markdown(
        """
        #### Write a natural language query against the documents in your Document Store
        """
    )
    user_query = st.text_area('Input query', height=200, key='user_query', label_visibility='visible')
    if st.button('Submit'):
        with st.spinner("Querying Document Store..."):
            output = azure_ai_pipe.run(query=user_query, params={"retriever": {"top_k": 5}})
            query_response = [a.answer for a in output["answers"]][0]
            st.markdown("### Response")
            st.write("\n")
            st.write(query_response)

if __name__ == "__main__":
    main()