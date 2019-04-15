#!/bin/bash

IMAP_SEARCH_QUERY="OR (NOT ANSWERED SUBJECT UTILTS) (SUBJECT UTILTS FLAGGED)"
chmod +x config.sh && \
source ./config.sh && \
mkdir -p /tmp/mails/ && \
mkdir -p /tmp/mails-aperak/ && \
cd ../ediel-parser/ && \
python cli.py com --imap-search-query "$IMAP_SEARCH_QUERY" --output-dir /tmp/mails && \
python cli.py parse --from mail --to mail --aperak --input-dir /tmp/mails --output-dir /tmp/mails-aperak && \
python cli.py com --input-dir /tmp/mails-aperak --imap-store-query \"+FLAGS\" "\\Seen \\Answered" --send | \
python cli.py com --imap-store-query \"-FLAGS\" "\\Flagged"