from pathlib import Path
from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.builders import PromptBuilder
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret

import argparse
import os

os.environ["HF_TOKEN_API"] = "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"
os.environ["GROQ_API_KEY"] = "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"


class Indexing:
    def __init__(self, document_store):
        self.converter = PyPDFToDocument()
        self.cleaner = DocumentCleaner()
        self.splitter = DocumentSplitter(
            split_by="sentence", split_length=10, split_overlap=2
        )
        self.writer = DocumentWriter(document_store=document_store)
        self.pipeline = Pipeline()
        self.pipeline.add_component("converter", self.converter)
        self.pipeline.add_component("cleaner", self.cleaner)
        self.pipeline.add_component("splitter", self.splitter)
        self.pipeline.add_component("writer", self.writer)

        self.pipeline.connect("converter", "cleaner")
        self.pipeline.connect("cleaner", "splitter")
        self.pipeline.connect("splitter", "writer")

    def get_pipeline(self) -> Pipeline:
        return self.pipeline

    def run_index_pipeline(self, path):
        self.pipeline.run({"converter": {"sources": [Path(path)]}})


class Query:
    def __init__(self, document_store, generator):
        self.template = """
                        {% for document in documents %}
                            {{ document.content }}
                        {% endfor %}

                        Please answer the question based on the given information.

                        {{question}}
                        """
        self.prompt_builder = PromptBuilder(template=self.template)
        self.rag_pipeline = Pipeline()
        self.retriever = InMemoryBM25Retriever(document_store)

        self.rag_pipeline.add_component("retriever", self.retriever)
        self.rag_pipeline.add_component("prompt_builder", self.prompt_builder)
        self.rag_pipeline.add_component("llm", generator)

        self.rag_pipeline.connect("retriever", "prompt_builder.documents")
        self.rag_pipeline.connect("prompt_builder", "llm")

    def run_pipeline(self, query):
        res = self.rag_pipeline.run(
            {
                "retriever": {"query": query},
                "prompt_builder": {"question": query},
            }
        )
        return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to file")
    parser.add_argument("--query", help="the query to run")
    args = parser.parse_args()
    doc_store = InMemoryDocumentStore()
    idx = Indexing(doc_store)
    idx.run_index_pipeline(args.path)
    generator = OpenAIGenerator(
        api_key=Secret.from_env_var("GROQ_API_KEY"),
        api_base_url="https://api.groq.com/openai/v1",
        model="gemma2-9b-it",
        generation_kwargs={"max_tokens": 4096},
    )

    query = Query(doc_store, generator)
    response = query.run_pipeline(args.query)
    print(response["llm"]["replies"][0])
