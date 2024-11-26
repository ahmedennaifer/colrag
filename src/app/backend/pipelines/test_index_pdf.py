from haystack import Pipeline
from haystack.components.converters import (
    PyPDFToDocument,
    TextFileToDocument,
    CSVToDocument,
)
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.components.builders import PromptBuilder


from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from haystack_integrations.components.embedders.fastembed import (
    FastembedDocumentEmbedder,
    FastembedTextEmbedder,
)


import logging

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
        self.dense_doc_embedder = FastembedDocumentEmbedder(
            model="BAAI/bge-small-en-v1.5"
        )
        self.pipeline = Pipeline()
        self.pipeline.add_component("converter", self.converter)
        self.pipeline.add_component("cleaner", self.cleaner)
        self.pipeline.add_component("splitter", self.splitter)
        self.pipeline.add_component("dense_doc_embedder", self.dense_doc_embedder)
        self.pipeline.add_component("writer", self.writer)

        self.pipeline.connect("converter", "cleaner")
        self.pipeline.connect("cleaner", "splitter")
        self.pipeline.connect("splitter", "dense_doc_embedder")
        self.pipeline.connect("dense_doc_embedder", "writer")

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

    def run_index_pipeline(self, docs) -> None:
        self.pipeline.run({"sources": docs})


class Query:
    def __init__(self, document_store, generator):
        self.template = """
                        <start_of_turn>user
                Using the information contained in the context, give a comprehensive answer to the question.
                If the answer cannot be deduced from the context, do not give an answer.
                
                Context:
                  {% for doc in documents %}
                  {{ doc.content }} 
                  {% endfor %};
                  
                  
                Question: {{query}}<end_of_turn>
                
                <start_of_turn>model
                """

        self.prompt_builder = PromptBuilder(template=self.template)
        self.embedder = FastembedTextEmbedder(model="BAAI/bge-small-en-v1.5")

        self.rag_pipeline = Pipeline()
        self.retriever = QdrantEmbeddingRetriever(document_store=document_store)

        self.rag_pipeline.add_component("text_embedder", self.embedder)
        self.rag_pipeline.add_component("retriever", self.retriever)

        self.rag_pipeline.add_component("prompt_builder", self.prompt_builder)
        self.rag_pipeline.add_component("llm", generator)

        self.rag_pipeline.connect("text_embedder", "retriever")
        self.rag_pipeline.connect("retriever.documents", "prompt_builder.documents")
        self.rag_pipeline.connect("prompt_builder.prompt", "llm.prompt")

    def run_pipeline(self, query: str) -> str:
        res = self.rag_pipeline.run(
            {
                "text_embedder": {"text": query},
                "prompt_builder": {"query": query},
            }
        )
        return res


"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to file")
    parser.add_argument("--query", help="the query to run")
    args = parser.parse_args()

    doc_store = QdrantDocumentStore(
        url="localhost:6333",
        index="Test coll 5",
        embedding_dim=384,
    )

    idx = Indexing(doc_store, args.path)
    idx.run_index_pipeline([args.path])

    generator = OpenAIGenerator(
        api_key=Secret.from_env_var("GROQ_API_KEY"),
        api_base_url="https://api.groq.com/openai/v1",
        model="gemma2-9b-it",
        generation_kwargs={"max_tokens": 4096},
    )

    print(f" number of docs: {doc_store.count_documents()}")

    print(f" printing stuff.. query: {args.query}, path: {args.path}")
    query = Query(doc_store, generator)

    response = query.run_pipeline(args.query)
    print(response["llm"]["replies"][0])

"""
