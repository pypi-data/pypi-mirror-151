from jina import Client
from docarray import DocumentArray, Document
import os
from jfc.helper import preproc, load_config, Formats, default_config
import click
import sys
from docarray import Document
import numpy as np
import yaml


# def load_config(filename):
    # with open(filename, "r") as file:
        # config = yaml.safe_load(file)

    # return config


# def preproc(doc: Document, dims=(64, 64)):
    # doc.load_uri_to_image_tensor()
    # doc.tensor = doc.tensor.astype(np.uint8)

    # doc.set_image_tensor_normalization().set_image_tensor_shape(dims)


# class Formats:
    # table = ["csv"]
    # image = ["jpg", "jpg", "png"]


# default_config = {
    # "host": "http://0.0.0.0:45678",
    # "indexing": {
        # "data": "./data",
        # "num_docs": 1_000_000,
    # },
    # "searching": {"image_size": [64, 64]},
# }


def index(host, num_docs, data, **kwargs):
    """
    Index data in various formats:

    CSV FILES
    One Document per line
    jfc index foo.csv

    EXISTING DOCUMENTARRAYS (coming later)
    Existing (pushed) DocumentArray from Jina Cloud
    jfc index docarray://foo

    GLOBS
    If jfc doesn't know what to do, it assumes a glob, and will index EVERY file that matches
    jfc index foo/**/*.jpg
    """
    # if config_file:
    # config = load_config(config_file)
    # else:
    # config = default_config

    # if host:
    # config["host"] = host
    # if num_docs:
    # config["indexing"]["num_docs"] = int(num_docs)
    # if data:
    # config["indexing"]["data"] = data

    if not host:
        print("Please specify a host with --host")
        sys.exit()
        # print("Please specify a host")
        # sys.exit()

    # if os.path.isdir(data):
    # print(f"Indexing from folder: {data}")
    # docs = DocumentArray.from_files(
    # f"{config['indexing']['data']}/**/*.jpg",
    # recursive=True,
    # size=int(config["indexing"]["num_docs"]),
    # )  # fix this to use all image formats
    # for doc in all_docs:
    # if doc.uri not in already_indexed[:, "uri"]:
    # print(f"{doc.uri} not indexed yet")
    # new_docs.append(doc)
    # else:
    # print(f"{doc.uri} already indexed")

    if data.split(".")[-1] in Formats.table:
        print("Indexing from csv")
        docs = DocumentArray.from_csv(data, size=num_docs)

    elif data.startswith("docarray://"):
        raise NotImplementedError

    else:
        try:
            print("Assuming that this is a glob and treating as such")
            docs = DocumentArray.from_files(data, size=num_docs)
        except:
            print("Unknown format")
            print("Please run jfc --help for more information")

    # for doc in all_docs:
    # if doc.uri not in already_indexed[:, "uri"]:
    # print(f"{doc.uri} not indexed yet")
    # new_docs.append(doc)
    # else:
    # print(f"{doc.uri} already indexed")

    # Now we'll use the client to send only the new docs to our indexing Flow
    # for doc in new_docs:
    docs.summary()
    # for doc in docs:
    # if doc.uri:
    # print(f"Processing {doc.uri}")
    # preproc(doc)

    # new_docs.summary()
    client = Client(host)
    # client = Client(host=config["host"])
    client.post("/update", docs, show_progress=True)
    # client.index(new_docs)

    # Extend our already indexed docs to reflect what's been indexed
    # already_indexed.extend(new_docs)


def search(data, host, **kwargs):
    """
    Run a search operation against a Jina Flow

    FILE
    jfc search foo.jpg

    STRING
    jfc search "foo foo foo"
    """
    # if config_file:
    # config_file = load_config(config_file)
    # else:
    # config_file = default_config

    if os.path.exists(data):
        search_type = "file"
        doc = Document(uri=data)
        print(f"Searching with file {doc.uri}")
        # preproc(doc)

    else:
        # assume it's a string
        search_type = "text"
        print(search_type)
        doc = Document(text=data)

    client = Client(host=host)
    response = client.search(doc)

    for match in response[0].matches:
        print(f"Text: {match.text}")
        print(f"URI: {match.uri}")
        print(f"Tags: {match.tags}")
        print(f"Score: {match.scores['cosine']}")
        print("-" * 60)


@click.command()
@click.argument("task")
@click.argument("data")
@click.option("--num_docs", "-n")
@click.option("--host", "-h")
# @click.option("--config_file", "-c")
def main(task: str, host, num_docs, data):
    if task == "index":
        index(host=host, num_docs=num_docs, data=data)
    elif task == "search":
        search(data, host=host, num_docs=num_docs)
    else:
        print("Please add 'index' or 'search' to your command")


if __name__ == "__main__":
    main()
