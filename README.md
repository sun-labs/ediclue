# EDI Command Line Interface Tools

## Requirements
- Python 3

## Setup

Install python dependencies
```bash
pip install -r requirements.txt
```

Make a copy of `config/config.sample.sh` to `config/config.sh` and set variables as fits.

```bash
# has to be done every time you run the cli.py script
source config/config.sh
```

## Examples

Send APERAK to unanswered UTILTS messages
```bash
# make sure config/config.sh is correctly set
cd bin/
./send-aperak-utilts.sh
```

Get emails with certain subject
```bash
python cli.py com --username mail@domain.com --password secret --server imap.domain.com --imap-search-query "SUBJECT UTILTS NOT (SUBJECT spam)"
# returns list of mail ids
```

Get emails with certain subject and store in folder
```bash
python cli.py com --username mail@domain.com --password secret --server imap.domain.com --imap-search-query "SUBJECT UTILTS NOT (SUBJECT spam)" --output-dir "./saved-emails"
# stores as "email-id.eml"
```

Get emails and grab edi-content and parse to json format and then store
```bash
python cli.py com --username mail@domain.com --password secret --server imap.domain.com --imap-search-query "SUBJECT UTILTS NOT (SUBJECT spam)" --output-dir "./saved-emails" && python cli.py parse --from mail --to json --output-dir "./edi-messages-json" --input-dir "./saved-emails"
# stored as email-id.eml.json
```

Get emails and grab edi-content and parse edi and generate aperak message, convert to email and send back to the sender.
```bash
source ../config/config.sh &&
python cli.py com --imap-search-query "SUBJECT UTILTS NOT (SUBJECT spam)" --output-dir "./saved-emails" && \
python cli.py parse --from mail --to mail --aperak --output-dir "./edi-aperak-mails" --input-dir "./saved-emails" && \
python cli.py com --send --input-dir "./edi-aperak-mails"
# returns a list of email ids
# every message sent will be stored in the "sent" folder of the mail account.
```

Set specific emails to answered
```bash
python cli.py com --username mail@domain.com --password secret --server imap.domain.com --imap-search-query "BEFORE 14-Apr-2019" --imap-store-query \"+FLAGS\" "\\Answered \\Seen"
# returns list of email ids that was updated
```

### Parser
Create EDI messages and convert to different formats


### Communicator
Manage e-mails via SMTP and/or IMAP