from pathlib import Path
import logging
from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack.document_stores.in_memory import InMemoryDocumentStore
import argparse
from haystack.components.builders import PromptBuilder
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.utils.hf import HFGenerationAPIType
from haystack.components.generators import HuggingFaceAPIGenerator, OpenAIGenerator
from haystack.utils import Secret

import os

os.environ["HF_TOKEN_API"] = "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"
os.environ["GROQ_API_KEY"] = "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"


generator = OpenAIGenerator(
    api_key=Secret.from_env_var("GROQ_API_KEY"),
    api_base_url="https://api.groq.com/openai/v1",
    model="gemma2-9b-it",
    generation_kwargs={"max_tokens": 4096},
)
document_store = InMemoryDocumentStore()
retriever = InMemoryBM25Retriever(document_store)
converter = PyPDFToDocument()
cleaner = DocumentCleaner()
splitter = DocumentSplitter(split_by="sentence", split_length=10, split_overlap=2)
writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.SKIP)

indexing_pipeline = Pipeline()
indexing_pipeline.add_component("converter", converter)
indexing_pipeline.add_component("cleaner", cleaner)
indexing_pipeline.add_component("splitter", splitter)
indexing_pipeline.add_component("writer", writer)

indexing_pipeline.connect("converter", "cleaner")
indexing_pipeline.connect("cleaner", "splitter")
indexing_pipeline.connect("splitter", "writer")

template = """
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Please answer the question based on the given information.

{{question}}
"""
prompt_builder = PromptBuilder(template=template)
rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", generator)

rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")


def run_index_pipeline(path):
    indexing_pipeline.run({"converter": {"sources": [Path(path)]}})
    logging.info("File Indexed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to file")
    parser.add_argument("--query", help="the query to run")
    args = parser.parse_args()
    run_index_pipeline(args.path)
    response = rag_pipeline.run(
        {"retriever": {"query": args.query}, "prompt_builder": {"question": args.query}}
    )
    print(response["llm"]["replies"][0])
