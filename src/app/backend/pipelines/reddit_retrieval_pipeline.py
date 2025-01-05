import logging
import os

from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.converters import (
    CSVToDocument,
    PyPDFToDocument,
    TextFileToDocument,
)
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.components.joiners import DocumentJoiner
from haystack.components.builders import AnswerBuilder

from haystack.utils import Secret


from haystack_integrations.components.embedders.fastembed import (
    FastembedDocumentEmbedder,
    FastembedTextEmbedder,
)
from haystack_integrations.components.rankers.cohere import CohereRanker
from haystack_integrations.components.generators.amazon_bedrock import AmazonBedrockGenerator

from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever

os.environ["HF_TOKEN_API"] = "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"


class Indexing:
    def __init__(self, document_store, file_path: str):
        self.cleaner = DocumentCleaner()
        self.splitter = DocumentSplitter(
            split_by="sentence", split_length=30, split_overlap=2
        )
        self.writer = DocumentWriter(document_store=document_store)
        self.converter = TextFileToDocument()

        self.pipeline = Pipeline()
        self.pipeline.add_component("writer", self.writer)
        self.pipeline.add_component("converter", self.converter)
        self.pipeline.add_component("cleaner", self.cleaner)
        self.pipeline.add_component("splitter", self.splitter)
        self.pipeline.add_component(
            "index_dense_doc_embedder",
            FastembedDocumentEmbedder(model="BAAI/bge-small-en-v1.5"),
        )
        self.pipeline.connect("converter", "cleaner")
        self.pipeline.connect("cleaner", "splitter")
        self.pipeline.connect("splitter", "index_dense_doc_embedder")
        self.pipeline.connect("index_dense_doc_embedder", "writer")

    def run_index_pipeline(self, docs) -> None:
        self.pipeline.run({"sources": [docs]})


class Query:
    def __init__(self, document_store):
        self.template = """
                You are a world class reddit specialist. Your task is to read reddit posts and their related comments, which can sometimes have malformed or missing comments,
                and sythenzise a response to the query of the user. You need to be as thorough and detail oriented as possible. If you cannot accurately identify the requested info or related post, say you dont have acess to that specific post.


            Context:
                  {% for doc in documents %}
                  {{ doc.content }}
                  {% endfor %};
                \nQuestion: {{query}}
                \nAnswer:
                """

        self.prompt_builder = PromptBuilder(template=self.template)
        self.ranker = CohereRanker(
            api_key=Secret.from_token("I5lMdF4rP7b0MidA0mppC68cLQhxUaD1IMdVOuIO"),
            top_k=10
        )
        self.joiner = DocumentJoiner()

        self.generator = AmazonBedrockGenerator(
            model="meta.llama3-3-70b-instruct-v1:0",
            aws_region_name=Secret.from_token("us-east-2"),
            model_max_length= 128000,
            truncate= False,
            max_length=2048
        )
        self.embedder = FastembedTextEmbedder(model="BAAI/bge-small-en-v1.5")
        self.answer_builder = AnswerBuilder()

        self.rag_pipeline = Pipeline()
        self.retriever = QdrantEmbeddingRetriever(document_store=document_store, top_k=150)

        self.rag_pipeline.add_component("q_dense_text_embedder", self.embedder)
        self.rag_pipeline.add_component("retriever", self.retriever)
        self.rag_pipeline.add_component("ranker", self.ranker)
        self.rag_pipeline.add_component("prompt_builder", self.prompt_builder)
        self.rag_pipeline.add_component("llm", self.generator)
        self.rag_pipeline.add_component("answer_builder", self.answer_builder)

        self.rag_pipeline.connect("q_dense_text_embedder", "retriever")
        self.rag_pipeline.connect("retriever", "ranker")
        self.rag_pipeline.connect("ranker", "prompt_builder")
        self.rag_pipeline.connect("prompt_builder.prompt", "llm.prompt")
        self.rag_pipeline.connect("llm.replies", "answer_builder.replies")
        self.rag_pipeline.connect("retriever", "answer_builder.documents")

    def run_pipeline(self, query: str) -> str:
        res = self.rag_pipeline.run(
            {
                "q_dense_text_embedder": {"text": query},
                "prompt_builder": {"query": query},
                "ranker": {"query": query},
                "answer_builder": {"query": query},

            }
        )
        return res
