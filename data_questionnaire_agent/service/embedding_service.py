import re
from typing import TypeVar, List
from pathlib import Path

from langchain.schema import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import FAISS

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.config import cfg
import numpy as np


VST = TypeVar("VST", bound="VectorStore")


def load_text(path: Path) -> List[Document]:
    """
    Loads the text files and extracts chunks of a pre-defined size.
    The page details are added to the extracted metadata

    Parameters:
    path (Path): The path where the documents are saved.

    Returns:
    List[Document]: Returns a list of values
    """
    assert path.exists()
    all_pages = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    for text_file in path.glob("*.txt"):
        loader = TextLoader(text_file.as_posix(), encoding="utf-8")
        pages: List[Document] = loader.load_and_split(text_splitter=text_splitter)
        for i, p in enumerate(pages):
            file_name = re.sub(r".+[\\/]", "", p.metadata["source"])
            p.metadata["source"] = f"{file_name} page {i + 1}"
        all_pages.extend(pages)
        logger.info(f"Processed {text_file}, all_pages size: {len(all_pages)}")
    log_stats(all_pages)
    return all_pages


def log_stats(documents: List[Document]):
    logger.info(f"Total number of documents {len(documents)}")
    counts = []
    for d in documents:
        counts.append(count_words(d))
    logger.info(f"Tokens Max {np.max(counts)}")
    logger.info(f"Tokens Min {np.min(counts)}")
    logger.info(f"Tokens Min {np.mean(counts)}")


def count_words(document: Document) -> int:
    splits = [s for s in re.split("[\s,.]", document.page_content) if len(s) > 0]
    return len(splits)


def generate_embeddings(
    documents: List[Document], persist_directory: str
) -> VST:
    """
    Receives a list of documents and generates the embeddings via OpenAI API.

    Parameters:
    documents (List[Document]): The document list with one page per document.
    path (Path): The path where the documents are found.

    Returns:
    VST: Recturs a reference to the vector store.
    """
    try:
        docsearch = FAISS.from_documents(documents, cfg.embeddings)
        docsearch.save_local(persist_directory)
        logger.info("Vector database persisted")
    except Exception as e:
        logger.exception(f"Failed to process documents")
        if "docsearch" in vars() or "docsearch" in globals():
            docsearch.persist()
        return None
    return docsearch


if __name__ == "__main__":
    from data_questionnaire_agent.config import cfg

    raw_text_folder = cfg.raw_text_folder
    document_list = load_text(raw_text_folder)
    logger.info("Amount of documents: %d", len(document_list))
    generate_embeddings(document_list, cfg.embeddings_persistence_dir.as_posix())
