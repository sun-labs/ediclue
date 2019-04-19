#!/bin/bash

TMP_FOLDER="/tmp"
FMAILS="$TMP_FOLDER/mails"
FAPERAK="$TMP_FOLDER/mails-aperak"
IMAP_SEARCH_QUERY="OR (NOT ANSWERED SUBJECT UTILTS) (SUBJECT UTILTS FLAGGED)"

. ../config/config.sh && \
mkdir -p "$FMAILS" && \
mkdir -p "$FAPERAK" && \
cd ../ediel-parser/ && \
"$SL_PYTHON_EXEC" cli.py com --imap-search-query "$IMAP_SEARCH_QUERY" --output-dir "$FMAILS" && \
"$SL_PYTHON_EXEC" cli.py parse --from mail --to mail --aperak --input-dir "$FMAILS" --output-dir "$FAPERAK" && \
"$SL_PYTHON_EXEC" cli.py com --input-dir "$FAPERAK" --imap-store-query \"+FLAGS\" "\\Seen \\Answered" --send | \
"$SL_PYTHON_EXEC" cli.py com --imap-store-query \"-FLAGS\" "\\Flagged"

rm -r "$FMAILS/" "$FAPERAK/"