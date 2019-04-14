#!/bin/bash

chmod +x config.sh && \
source ./config.sh && \
mkdir -p /tmp/mails/ && \
mkdir -p /tmp/mails-aperak/ && \
cd ../ediel-parser/ && \
python cli.py com get --imap-search-query "OR (NOT ANSWERED SUBJECT UTILTS) FLAGGED" --imap-store-query \"-FLAGS\" "\\Flagged" --output-dir /tmp/mails && \
python cli.py parse --from mail --to mail --aperak --input-dir /tmp/mails --output-dir /tmp/mails-aperak && \
python cli.py com send --input-dir /tmp/mails-aperak --imap-store-query \"+FLAGS\" "\\Seen \\Answered"