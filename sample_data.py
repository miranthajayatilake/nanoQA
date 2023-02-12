from haystack.utils import fetch_archive_from_http
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever
import os
import pandas as pd
import argparse

host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

def index_data(doc_dir, s3_url, index_name):
    # Download
    doc_dir = doc_dir
    s3_url = s3_url
    fetch_archive_from_http(url=s3_url, output_dir=doc_dir)

    document_store = ElasticsearchDocumentStore(
        host=host,
        username="",
        password="",
        index=index_name,
        embedding_field="question_emb",
        embedding_dim=384,
        excluded_meta_data=["question_emb"],
        similarity="cosine",
    )

    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        use_gpu=True,
        scale_score=False,
    )

    # Get dataframe with columns "question", "answer" and some custom metadata
    df = pd.read_csv(f"{doc_dir}/small_faq_covid.csv")
    # Minimal cleaning
    df.fillna(value="", inplace=True)
    df["question"] = df["question"].apply(lambda x: x.strip())

    # Get embeddings for our questions from the FAQs
    questions = list(df["question"].values)
    df["question_emb"] = retriever.embed_queries(queries=questions).tolist()
    df = df.rename(columns={"question": "content"})

    # Convert Dataframe to list of dicts and index them in our DocumentStore
    docs_to_index = df.to_dict(orient="records")
    document_store.write_documents(docs_to_index)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('doc_dir', type=str)
    parser.add_argument('s3_url', type=str)
    parser.add_argument('index_name', type=str)
    args = parser.parse_args()

    index_data(args.doc_dir, args.s3_url, args.index_name)