![EDICLUE, ribbon-like form in the background](/docs/cover.png)

<div align="center">
Command Line Tools for EDI Communication. Generate APERAK and CONTRL without having to sell your firstborn
<br/>
<br/>

<a href="https://www.sunlabs.se">
  <img src="https://img.shields.io/badge/%20-Made%20by%20Sun%20Labs-black?labelColor=ffe601&style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAGKSURBVHgB7Zi/SgNBEMZnxFpTC4J9BNPaWVpa2VrZi3kAkzc4a4maMjZJaWkndjaCnQHF1j8vsO6czQ63d3uXZGAS5oOB5Hbmu/vtLnPsoftEByugNVgRGYg2GYg2GYg2GYg2GYg2GYg2GYg2GYg2rTdJ/v718fN/oGxtIrQ2YKGaxz8JQuaXVw5u7wCm7+GIg04boLMLcHGOsLMNM2lh/nRmL4teF5yfFZe7JoJyq7yk/aMgX6/oDvbr3SAMP4N5bQpAwj8KcnRYbuaXOI+ycXrAFIiEP8SWO2ae9ZHNBv2+yTB606wPldtJwp+BvD0VC1PbhWooJ6yhfR+rkfRn75GHR8c6B3WK8XV1G4zlUCcajorf/ST9GchwxE163XptlXLOTvm1yX0xT9KfgTy/8MG9NtTWyTGy/9OPYo6kP4bffnGLL5cfgyZK1Uv6sxUJl3mWN3WqXtKfgYwHCL5P5zEZNJutOvWS/mxrLbPsPKJNBqJNBqJNBqJNBqJNBqJNBqJNBqJNBqJNf0F+WMETxwNrAAAAAElFTkSuQmCC" alt="Badge with text 'Made by Sun Labs'" />
  </a>
</div>

## Features

- Convert EDI to JSON
- Generate APERAK and CONTRL for EDI messages
- Support for SMTP and IMAP
- Made for EDIEL

## Requirements
- Python 3

## Setup

Install python dependencies
```bash
pip install -r requirements.txt
```

Make a copy of `config/config.sample.sh` to `config/config.sh` and set variables as needed

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

---

With ⚡️ from Uppsala
