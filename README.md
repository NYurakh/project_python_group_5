<div align="center">

# Personal Assistant

**A small command-line personal assistant for managing contacts and notes locally.**


**English** · [Українська](README.uk.md)

</div>

---

## About

This is a team project for the **Python Programming** course at **Neoversity**.

The application runs in the terminal and works as a local contact book and note manager. It can add, edit, remove, search, sort, and display contacts, show upcoming birthdays, and manage text notes with tags. Data is saved locally and restored the next time the program starts.


---

## Functionality

- add a contact with a name and one or more phone numbers;
- optionally add a birthday, email, and address to contact;
- edit all contact fields or only phone numbers;
- remove contacts;
- search across all contact fields;
- search inside one selected field;
- list contacts and sort them by name, phone, email, address, or birthday;
- show birthdays within a selected number of days;
- validation of phone numbers, emails, birthdays, and addresses during input;
- complete command names with Tab;
- save application state locally after each recognized command;
- add, edit, remove, and display notes;
- assign tags to notes;
- search notes by title, text, or tags;
- search notes by a specific tag;
- sort notes alphabetically by tags;

Most commands can ask for missing values interactively, so there is no need to remember a long list of positional arguments.

---

## Requirements

| | |
|---|---|
| Python | 3.10 or newer |
| Dependencies | `rich`, `prompt_toolkit` (see [requirements.txt](requirements.txt)) |
| Terminal | A real interactive console |

> [!IMPORTANT]
> `prompt_toolkit` needs a real interactive terminal. On Windows, use **PowerShell**, **Command Prompt**, or **Windows Terminal**. Git Bash / MSYS and redirected input may fail because they do not provide the console interface expected by `prompt_toolkit`.

---

## Installation

```bash
git clone https://github.com/NYurakh/project_python_group_5.git
cd project_python_group_5

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Running

```bash
python main.py
```

The program starts with a command list and then waits at the `>>>` prompt.

Type `help` to show the command list again and `exit` to save and quit.

---

## Quick example

Adding a contact is interactive:

```
>>> add-contact
 Name: Olena Kovalchuk 
 Phone: 0501112233 
 Another phone (Enter to finish): 0679876543 
 Another phone (Enter to finish): 
 Birthday DD.MM.YYYY (Enter to skip): 14.09.1994 
 Email (Enter to skip): olena.k@example.com 
 Address (Enter to skip): Lviv 
 ✓ Contact added.
 ```

Only the name and one phone number are required — press Enter to skip anything else.

If a value is invalid, the program shows the validation error and asks for that value again. The previous input is kept in the prompt where possible, so fixing one digit does not mean typing the whole field again.

## Commands

### General

| Command | What it does |
|---|---|
| `help` | Show the command list |
| `hello` | Print a greeting |
| `exit` | Save and exit |

### Contacts

| Command | What it does |
|---|---|
| `add-contact` | Add a new contact through interactive prompts |
| `edit-contact [name]` | Edit the contact name, phones, birthday, email, and address |
| `edit-contact-phones [name]` | Edit only the phone numbers |
| `remove-contact [name]` | Remove a contact |
| `show-all-contacts [field]` | Show all contacts, optionally sorted by a field |
| `show-contact-phones <name>` | Show phone numbers for one contact |
| `search-contacts [text]` | Search for a substring across all contact fields |
| `search-contact-by-field [field] [value]` | Search only in one selected field |
| `upcoming-birthdays [days]` | Show contacts with birthdays in the requested range |

### Notes

| Command | What it does |
|---|---|
| `add-note` | Add a new note with a title, text, and optional tags |
| `show-all-notes` | Show all saved notes |
| `show-note [ID]` | Show one note by its ID |
| `edit-note [ID]` | Edit the title, text, and tags of a note |
| `remove-note [ID]` | Remove a note |
| `search-notes [text]` | Search notes by title, text, or tags |
| `search-notes-by-tag [tag]` | Find notes with a specific tag |
| `sort-notes-by-tags` | Show notes sorted alphabetically by tags |

---

## Validation

| Field | Current rule |
|---|---|
| Name | Required when adding/editing through the CLI; must be unique in the address book |
| Phone | Exactly 10 digits; duplicates inside one contact are rejected; at least one phone is required |
| Email | Must match a normal `name@example.com`-style email format; addresses ending in `.ru`, `.su`, or `.рф` are rejected |
| Birthday | Strict `DD.MM.YYYY` format and a valid calendar date |
| Address | Optional, but if provided it cannot be empty or whitespace-only |

Validation for `Phone`, `Email`, `Birthday`, and `Address` is implemented in their field classes in `models/fields.py`.

---
## Prompt controls
| Key | Behaviour |
|---|---|
|`Tab`| Complete a command name at the main prompt; some choice prompts also provide completion|
|`Enter` on an optional prompt| Skip the value, clear it while editing, or finish entering a list|
|`Ctrl+C` during a command prompt|Cancel the current command and return a `Cancelled.` message|
---
## Data Storage

Application state is stored in `.pkl` file.

The file contains the `AppContext`, including both the `AddressBook` and `NoteBook`.

The `userdata` directory is created automatically when data is saved. The data file is excluded from Git, so personal contacts and notes are not committed to the repository.

The application saves its state after each recognized command and automatically loads it the next time it starts.

---
## Project structure

```text
project_python_group_5/
├── main.py                     # REPL loop, command dispatch, saving
├── app_context.py              # Shared application state
├── requirements.txt
│
├── models/
│   ├── fields.py               # Name, Phone, Email, Birthday, Address
│   ├── contact.py              # Contact record and matching/sorting helpers
│   └── note.py                 # Note model, tags, editing and search matching
│
├── books/
│   ├── address_book.py         # Contact collection, search, sort, birthdays
│   └── note_book.py             # Note collection, search, tags and sorting
│
├── cli/
│   ├── parser.py               # shlex-based command parsing
│   ├── command_registry.py     # Command metadata and command groups
│   ├── command_helpers.py      # Prompt loops and command error handling
│   ├── contact_commands.py     # Contact command handlers
│   ├── note_commands.py        # Note command handlers
│   ├── general_commands.py     # help / hello / exit
│   └── view.py                 # Rich tables and terminal messages
│
└── storage/
│   └── storage.py              # Pickle save/load logic
│
└── userdata/
    └── assistant_data.pkl      # Local application data, created automatically
```

A few implementation details:

- command input is parsed with `shlex`, so quoted names such as `"Olena Kovalchuk"` work as one argument;
- commands are registered in `cli/command_registry.py` together with their usage text and description;
- the help screen and main command completer are built from that registry;
- terminal tables and success/error messages are rendered with `rich`;
- `prompt_toolkit` is used for interactive input and completion.


## Team

Built by group 5 of the Neoversity Python Programming course:

- [Nazar Yurakh](https://github.com/NYurakh)
- [Andrii Dombrovskyi](https://github.com/andrii-dombrovskyi)
- [Andrii Kolotii](https://github.com/KyberxAI)

## License

Educational project created as coursework for Neoversity. Feel free to read, run, and learn from it.
