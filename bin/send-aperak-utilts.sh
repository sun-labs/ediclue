#!/bin/bash

chmod +x config.sh && \
./config.sh && \
mkdir -p /tmp/mails/ && \
python cli.py com get --imap-search-query "NOT ANSWERED SUBJECT UTILTS" --output-dir /tmp/mails && \
python cli.py com 