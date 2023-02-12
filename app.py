import streamlit as st

import logging
import os
import time

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever
from haystack.pipelines import FAQPipeline

from haystack.utils import print_answers
from PIL import Image

image = Image.open('utils/logo.jpg')

st.image(image, width=250)
# st.title("NanoQA")
st.subheader("Chat with your data")
st.write('---')

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)


# Get the host where Elasticsearch is running, default to localhost
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")


#------------ 
index_name = st.text_input('Index to refer from datastore', 'index_qa')


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


pipe = FAQPipeline(retriever=retriever)

question = st.text_input('Ask a question', 'Does warm weather stop the spreading of the virus?')

if st.button("Ask"):
    # Infering 
    prediction = pipe.run(query=question, params={"Retriever": {"top_k": 3}})
    # print_answers(prediction, details="medium")

    if prediction['answers'][0].score >= 0.7:
        # print(prediction['answers'])
        text = str(prediction['answers'][0].answer)
        source = '\n\n**Extracted source - ' + str(prediction['answers'][0].meta['source'] + '**')
        link = '\n' + str(prediction['answers'][0].meta['link'])
        full_answer = text + source + link

        t = st.empty()
        for i in range(len(full_answer) + 1):
            t.write("%s..." % full_answer[0:i])
            time.sleep(0.03)
    else:
        st.write('nanoQA failed to find an answer with confidence...sorry!')