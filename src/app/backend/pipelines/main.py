from pathlib import Path
from haystack import Pipeline
from haystack.components.converters import (
    PyPDFToDocument,
    TextFileToDocument,
    CSVToDocument,
)
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.builders import PromptBuilder
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret

import logging

import argparse
import os

os.environ["HF_TOKEN_API"] = "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"
os.environ["GROQ_API_KEY"] = (
    "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"  ##### API KEY DOWN ####
)


class Indexing:
    def __init__(self, document_store, file_path: str):
        self.cleaner = DocumentCleaner()
        self.splitter = DocumentSplitter(
            split_by="sentence", split_length=10, split_overlap=2
        )
        self.writer = DocumentWriter(document_store=document_store)
        self.converter = self.set_converter_by_extension(file_path)
        self.pipeline = Pipeline()
        self.pipeline.add_component("converter", self.converter)
        self.pipeline.add_component("cleaner", self.cleaner)
        self.pipeline.add_component("splitter", self.splitter)
        self.pipeline.add_component("writer", self.writer)

        self.pipeline.connect("converter", "cleaner")
        self.pipeline.connect("cleaner", "splitter")
        self.pipeline.connect("splitter", "writer")

    def set_converter_by_extension(self, path: str) -> "HaystackConverter":

        extension = path.split(".")[-1]

        logging.debug(f"Got extension {extension}")

        if extension == "txt":
            logging.debug(f"Assigning extension {extension} to TextDocumentConverter")
            return TextFileToDocument()

        elif extension == "pdf":
            logging.debug(f"Assigning extension {extension} to PyPDFDocumentConverter")
            return PyPDFToDocument()

        elif extension == "csv":
            logging.debug(f"Assigning extension {extension} to CSVDocumentConverter")
            return CSVToDocument()
        raise ValueError(f"Unsupported file extension: {extension}")

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

    def run_pipeline(self, query: str) -> str:
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
    idx = Indexing(doc_store, args.path)
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
