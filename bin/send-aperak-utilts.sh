#!/bin/bash

TMP_FOLDER="/tmp"
FMAILS="$TMP_FOLDER/mails"
FAPERAK="$TMP_FOLDER/mails-aperak"
IMAP_SEARCH_QUERY="OR (NOT ANSWERED SUBJECT UTILTS) (SUBJECT UTILTS FLAGGED)"

chmod +x config.sh && \
source ./config.sh && \
mkdir -p "$FMAILS" && \
mkdir -p "$FAPERAK" && \
cd ../ediel-parser/ && \
python cli.py com --imap-search-query "$IMAP_SEARCH_QUERY" --output-dir "$FMAILS" && \
python cli.py parse --from mail --to mail --aperak --input-dir "$FMAILS" --output-dir "$FAPERAK" && \
python cli.py com --input-dir /tmp/mails-aperak --imap-store-query \"+FLAGS\" "\\Seen \\Answered" --send | \
python cli.py com --imap-store-query \"-FLAGS\" "\\Flagged"

rm /tmp/mails/* 2> /dev/null
rm /tmp/mails-aperak/* 2> /dev/null