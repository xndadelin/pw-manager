# pw-manager

A password manager, which is used through the terminal.

## Features

- **Add Passwords**: Store new passwords with associated service, username, and optional notes.
- **List Passwords**: Display all stored passwords in a tabular format.
- **Edit Passwords**: Update existing password entries.
- **Delete Passwords**: Remove password entries from the database.
- **Search Passwords**: Search for password entries by service, username, or notes.
- **Generate Passwords**: Generate random secure passwords.
- **Clear Terminal**: Clear the terminal screen.
- **Help**: Display available commands and their usage.

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/xndadelin/pw-manager
cd pw-manager
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Textualize

```bash
pip install textual
```
Check this for eventual errors: https://textual.textualize.io/getting_started/

### Set Up Environment Variables

Create a `.env` file in the project root directory and add the following variables:

```properties
PHRASE=
FERNET_KEY=
DB_HOST=
DB_USER=
DB_PASSWORD=
```

### Usage

Run the application:

```bash
python main.py
```

## Commands

- `help`: Show help message
- `clear`: Clear the terminal
- `exit`: Exit CLI mode
- `add`: Add a new password entry
- `list`: List all password entries
- `delete`: Delete a password entry
- `edit`: Edit a password entry
- `search`: Search for password entries
- `generate`: Generate a random password

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.