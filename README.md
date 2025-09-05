# GLEIF-IT.github.io

This repository contains .well-known information.

The software "gleif-serve" is not intended to be deployed in production, it is a tool to support development of documentation.

## Installation

### Install Project Dependencies

```bash
uv sync
```

## Usage

### Start the Server

```bash
uv run serve

```

### cURL example

```bash
curl -s http://127.0.0.1:8080/.well-known/index.json | jq '.resources.schema.schemas | keys'
```

### shell script example

```bash
#!/bin/bash
BASE_URL="http://127.0.0.1:8080/.well-known"

OOBI_PATHS=$(curl -s "${BASE_URL}/index.json" | jq -r '.resources.witness.witnesses[].oobi')
echo $OOBI_PATHS

for oobi_path in $OOBI_PATHS; do
    curl -s "${BASE_URL}${oobi_path}"
    echo
done
```

## Schema SAID

```bash
uv run saidify
```
