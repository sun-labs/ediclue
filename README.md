# EDI Command Line Interface Tools

## Requirements
- Python 3

## Setup
Install python dependencies
```pip install -r requirements.txt```

## Examples

Get emails with certain subject
```bash
python cli.py com get --username mail@domain.com --password secret --server imap.domain.com --imap-search-query "SUBJECT UTILTS NOT (SUBJECT spam)"
# returns list of mail ids
```

Get emails with certain subject and store in folder
```bash
python cli.py com get --username mail@domain.com --password secret --server imap.domain.com --imap-search-query "SUBJECT UTILTS NOT (SUBJECT spam)" --output-dir "./saved-emails"
# stores as "email-id.eml"
```

Get emails and grab edi-content and parse to json format and then store
```bash
python cli.py com get --username mail@domain.com --password secret --server imap.domain.com --imap-search-query "SUBJECT UTILTS NOT (SUBJECT spam)" --output-dir "./saved-emails" && python cli.py parse --from mail --to json --output-dir "./edi-messages-json" --input-dir "./saved-emails"
# stored as email-id.eml.json
```

Get emails and grab edi-content and parse edi and generate aperak message, convert to email and send back to the sender.
```bash
python cli.py com get --username mail@domain.com --password secret --server imap.domain.com --imap-search-query "SUBJECT UTILTS NOT (SUBJECT spam)" --output-dir "./saved-emails" && python cli.py parse --from mail --to email --aperak --output-dir "./edi-aperak-mails" --input-dir "./saved-emails" && python cli.py com send --username mail@domain.com --password secret --server smtp.domain.com --input-dir "./edi-aperak-mails"
# returns a list of email ids
# every sent message will be stored in the imap folder INBOX.sent
```

### Parser
Create EDI messages and convert to different formats


### Communicator
Manage e-mails via SMTP and/or IMAP