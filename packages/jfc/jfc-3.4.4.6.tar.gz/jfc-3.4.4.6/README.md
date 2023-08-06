# JFC

### Jina Flow Companion

That's right: Jina Flow Companion. Not Jentucky Fried Chicken, or Jesus Fiona Christ.

**Note:** Jina AI doesn't officially support JFC. If you have questions, drop an issue. Don't bother Jina on Slack ;)

## What does it do?

A simple CLI to:

- Index data from a folder, file, text string, CSV, or (coming soon) DocArray on Jina Cloud
- Search data via string or file

It should work with all versions of Jina from 3.0 onwards (prior versions had slightly different APIs)

## Features

- Read config from YAML (coming soon) or command-line arguments
- Connect via REST, gRPC, or WebSocket gateways

### Install

```
pip install jfc
```

### Index

```
jfc index <data> -h https://foo.wolf.jina.ai
```

Where `<data>` is a CSV file or glob

### Search

```
jfc search <data> -h https://foo.wolf.jina.ai
```

Where `<data>` is a file or string

### Other endpoints

Just use arbitrary endpoint name instead of `search` or `index`

For [AnnLiteIndexer](https://hub.jina.ai/executor/7yypg8qk) (and maybe others?):

```
jfc status -h https://foo.wolf.jina.ai # Get index status
jfc clear -h https://foo.wolf.jina.ai  # Clear index
```

### Arguments

| Argument | Meaning                                            | 
| ---      | ---                                                | 
| `-h`     | URL to host                                        | 
| `-n`     | Number of documents to index OR return from search |

### Notes

- JFC doesn't do any preprocessing of data. What you input is what you get
- This is alpha-quality software that I built to scratch an itch. Don't expect miracles ;)
- Version number is tied to latest version of Jina it has been tested with. Any number past patch version is the patch version for JFC, not Jina.
