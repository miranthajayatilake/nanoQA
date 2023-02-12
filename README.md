<!-- # nanoQA -->
<img src="./utils/logo.jpg" height="100">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/miranthajayatilake/kudle/blob/main/LICENSE) [![version](https://img.shields.io/badge/version-0.2-yellow)]() [![discord](https://img.shields.io/badge/chat-discord-blueviolet)](https://discord.gg/UgeAukFB)



# Chat with your data to find answers :mag: :zap: 

nanoQA builds a question-answering application on your own data using the power of Large Language Models (LLMs).

**Please refer to this blog post for a comprehensive guide** :heavy_exclamation_mark: [LINK]()

Demo

<img src="./utils/demo.gif">

## Quick start

- Create a virtual environment with python (Tested with `python 3.10.9` on [Anaconda](https://www.anaconda.com/))
- `pip install -r requirements.txt` to install all dependecies.
- Make sure [Docker](https://www.docker.com/) is up and running in your local environment. We use docker to set up [elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) as our data store.
- Run `bash datastore.sh` to pull and set up elasticsearch. Wait till this step is completed.
- Run `python sample_data.py data/faq_covid https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/small_faq_covid.csv.zip index_qa`. This script will download a sample dataset of FAQs on COVID 19 and index it under `index_qa`. This dataset and index name are for demo purposes. You can replace this with your own data and naming.
- Run `streamlit run app.py` to spin up the user interface.

Now you can provide your index name and start chatting with your data.

## Contributing

I highly appreciate your contributions to this project in any amount possible. This is still at an very basic stage. Suggestions on additional features and functionality are welcome. General instructions on how to contribute are mentioned in [CONTRIBUTING](CONTRIBUTING.md)

## Getting help

Please use the issues tracker of this repository to report on any bugs or questions you have.

Also you can join the [DISCORD](https://discord.gg/UgeAukFB)