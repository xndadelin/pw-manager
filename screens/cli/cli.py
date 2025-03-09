import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Footer, Header, Input, RichLog, Button as TextualButton
from textual.screen import Screen
from rich.table import Table
import sqlite3

load_dotenv()

class CLI(Screen):
    CSS_PATH = "main.tcss"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="cli_container"):
            yield TextualButton(label="Go back", id="back_button", variant="primary")
            yield Static("Command line interface", id="cli_title")
            yield RichLog(id="command_history", highlight=True, markup=True)
            with Horizontal(id="command_prompt_container"):
                yield Static("$ ", id="prompt")
                yield Input(placeholder="Enter command", id="command_input")
        yield Footer()

    @on(TextualButton.Pressed, "#back_button")
    def handle_back_button_pressed(self) -> None:
        self.app.pop_screen()
        
    def on_mount(self) -> None:
        self.query_one("#command_input").focus()
        self.query_one("#command_history", RichLog).write("Welcome to CLI mode. Type 'help' to see available commands.")
        key = os.getenv("FERNET_KEY")
        print(f"FERNET_KEY: {key}")

    def encrypt(self, data: str) -> str:
        try:
            key = os.getenv("FERNET_KEY")
            if not key:
                raise ValueError("FERNET_KEY environment variable not set")
            fernet = Fernet(key.encode())
            encrypted_data = fernet.encrypt(data.encode()).decode()
            return encrypted_data
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")

    def decrypt(self, data: str) -> str:
        try:
            key = os.getenv("FERNET_KEY")
            if not key:
                raise ValueError("FERNET_KEY environment variable not set")
            fernet = Fernet(key.encode())
            decrypted_data = fernet.decrypt(data.encode()).decode()
            return decrypted_data
        except Exception as e:
            print(f"Decryption failed for data: {data}")
            raise ValueError(f"Decryption failed: {str(e)}")

    def clear(self) -> None:
        history = self.query_one("#command_history", RichLog)
        history.clear()
        history.write("Terminal cleared.\nWelcome to CLI mode. Type 'help' to see available commands.")

    def exit(self) -> None:
        history = self.query_one("#command_history", RichLog)
        history.write("Exiting CLI mode...")
        self.app.pop_screen()

    def add(self, args=None) -> None:
        history = self.query_one("#command_history", RichLog)
        if args is None:
            command_text = self.query_one("#command_input", Input).value
            args = command_text.split(" ")[1:] if len(command_text.split(" ")) > 1 else []
        parsed_args = {}
        current_key = None
        for arg in args:
            if arg.startswith("--"):
                current_key = arg[2:]
                parsed_args[current_key] = ""
            elif current_key:
                parsed_args[current_key] = arg
        required_fields = ["password", "service", "username"]
        missing_fields = [field for field in required_fields if field not in parsed_args]
        if missing_fields:
            history.write("[red]Error: Missing required fields: " + ", ".join(missing_fields) + "[/red]")
            history.write("[yellow]Usage: add --password [password] --username [username] --service [service] [--notes [notes]][/yellow]")
            return
        if "notes" not in parsed_args:
            parsed_args["notes"] = ""
        try:
            db = sqlite3.connect('passwords.db')
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS entries (service TEXT, username TEXT, password TEXT, notes TEXT)")
            parsed_args["password"] = self.encrypt(parsed_args["password"])
            cursor.execute("INSERT INTO entries (service, username, password, notes) VALUES (?, ?, ?, ?)", (parsed_args["service"], parsed_args["username"], parsed_args["password"], parsed_args["notes"]))
            db.commit()
            history.write(f"[green]Password for {parsed_args['service']} added successfully.[/green]")
        except Exception as e:
            history.write(f"[red]Error adding password: {str(e)}[/red]")

    def list(self) -> None:
        history = self.query_one("#command_history", RichLog)
        try:
            db = sqlite3.connect('passwords.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM entries")
            entries = cursor.fetchall()
            if not entries:
                history.write("[yellow]No passwords saved yet.[/yellow]")
                return
            lines = []
            for entry in entries:
                service, username, password, notes = entry
                lines.append(f"{service}|{username}|{password}|{notes}\n")
            
            table = Table("ID", "Service", "Username", "Password", "Notes", title="Password entries")
            for i, line in enumerate(lines, 1):
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) >= 4:
                        service, username, password, notes = parts[0], parts[1], parts[2], parts[3]
                        password = self.decrypt(password)
                        table.add_row(f"{i}", f"[green]{service}[/green]", f"[yellow]{username}[/yellow]", f"[red]{password}[/red]", notes)
            history.write(table)
        except Exception as e:
            history.write(f"[red]Error reading passwords: {str(e)}[/red]")

    def delete(self) -> None:
        history = self.query_one("#command_history", RichLog)
        command_text = self.query_one("#command_input", Input).value
        args = command_text.split(" ")[1:] if len(command_text.split(" ")) > 1 else []
        if not args:
            history.write("[red]Error: Missing entry ID[/red]")
            history.write("[yellow]Usage: delete ID[/yellow]")
            return
        try:
            entry_id = int(args[0])
            db = sqlite3.connect('passwords.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM entries")
            entries = cursor.fetchall()
            if not entries or entry_id < 1 or entry_id > len(entries):
                history.write(f"[red]Error: Entry #{entry_id} does not exist[/red]")
                return
            service = entries[entry_id - 1][0]
            cursor.execute("DELETE FROM entries WHERE rowid = ?", (entry_id,))
            db.commit()
            history.write(f"[green]Password for {service} deleted successfully.[/green]")
        except ValueError:
            history.write("[red]Error: ID must be a number[/red]")
        except Exception as e:
            history.write(f"[red]Error deleting password: {str(e)}[/red]")

    def edit(self) -> None:
        history = self.query_one("#command_history", RichLog)
        command_text = self.query_one("#command_input", Input).value
        args = command_text.split(" ")[1:] if len(command_text.split(" ")) > 1 else []
        if not args:
            history.write("[red]Error: Missing entry ID[/red]")
            history.write("[yellow]Usage: edit ID --field value [--field value ...][/yellow]")
            return
        try:
            entry_id = int(args[0])
            args = args[1:]
            parsed_args = {}
            current_key = None
            for arg in args:
                if arg.startswith("--"):
                    current_key = arg[2:]
                    parsed_args[current_key] = ""
                elif current_key:
                    parsed_args[current_key] = arg
            if not parsed_args:
                history.write("[red]Error: No fields to update[/red]")
                history.write("[yellow]Usage: edit ID --field value [--field value ...][/yellow]")
                return
            db = sqlite3.connect('passwords.db')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM entries")
            entries = cursor.fetchall()
            if not entries or entry_id < 1 or entry_id > len(entries):
                history.write(f"[red]Error: Entry #{entry_id} does not exist[/red]")
                return
            service, username, password, notes = entries[entry_id - 1]
            if "service" in parsed_args:
                service = parsed_args["service"]
            if "username" in parsed_args:
                username = parsed_args["username"]
            if "password" in parsed_args:
                password = self.encrypt(parsed_args["password"])
            if "notes" in parsed_args:
                notes = parsed_args["notes"]
            cursor.execute("UPDATE entries SET service = ?, username = ?, password = ?, notes = ? WHERE rowid = ?", (service, username, password, notes, entry_id))
            db.commit()
            history.write(f"[green]Password entry updated successfully.[/green]")
        except ValueError:
            history.write("[red]Error: ID must be a number[/red]")
        except Exception as e:
            history.write(f"[red]Error updating password: {str(e)}[/red]")

    def search(self) -> None:
        history = self.query_one("#command_history", RichLog)
        command_text = self.query_one("#command_input", Input).value
        args = command_text.split(" ")[1:] if len(command_text.split(" ")) > 1 else []
        if not args:
            history.write("[red]Error: Missing search term[/red]")
            history.write("[yellow]Usage: search term[/yellow]")
            return
        search_term = " ".join(args).lower()
        try:
            db = sqlite3.connect('passwords.db')
            cursor = db.cursor()
            cursor.execute("SELECT rowid, * FROM entries")
            entries = cursor.fetchall()
            if not entries:
                history.write("[yellow]No passwords saved yet.[/yellow]")
                return
            table = Table("ID", "Service", "Username", "Password", "Notes", title=f"Search Results for '{search_term}'")
            found = False
            for entry in entries:
                rowid, service, username, password, notes = entry
                if (search_term in service.lower() or search_term in username.lower() or search_term in notes.lower()):
                    password = self.decrypt(password)
                    table.add_row(f"{rowid}", f"[green]{service}[/green]", f"[yellow]{username}[/yellow]", f"[red]{password}[/red]", notes)
                    found = True
            if found:
                history.write(table)
            else:
                history.write(f"[yellow]No entries found matching '{search_term}'[/yellow]")
        except Exception as e:
            history.write(f"[red]Error searching passwords: {str(e)}[/red]")

    def help(self) -> None:
        history = self.query_one("#command_history", RichLog)
        history.write("[bold blue]Available commands:[/bold blue]")
        history.write("[green]help[/green]: Show this help message")
        history.write("[green]clear[/green]: Clear the terminal")
        history.write("[green]exit[/green]: Exit CLI mode")
        history.write("[green]add[/green]: Add a new password entry")
        history.write("[green]list[/green]: List all password entries")
        history.write("[green]delete[/green]: Delete a password entry")
        history.write("[green]edit[/green]: Edit a password entry")
        history.write("[green]search[/green]: Search for password entries")
        history.write("[green]generate[/green]: Generate a random password")

    def generate(self) -> None:
        history = self.query_one("#command_history", RichLog)
        history.write("Generating random password...")
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        special = "!@#$%^&*()_+"
        all_chars = lowercase + uppercase + digits + special
        password = []
        for _ in range(3):
            password.append(random.choice(lowercase))
            password.append(random.choice(uppercase))
            password.append(random.choice(digits))
            password.append(random.choice(special))
        for _ in range(4):
            password.append(random.choice(all_chars))
        random.shuffle(password)
        password = "".join(password)
        history.write(f"[green]Random password generated: {password}[/green]")

    @on(Input.Submitted, "#command_input")
    def handle_command(self) -> None:
        input_field = self.query_one("#command_input", Input)
        command_text = input_field.value
        command = command_text.split(" ")[0] if command_text else ""
        history = self.query_one("#command_history", RichLog)
        history.write(f"[bold green]$[/bold green] [yellow]{command_text}[/yellow]")
        available_commands = {
            "help": self.help,
            "clear": self.clear,
            "exit": self.exit,
            "add": self.add,
            "list": self.list,
            "delete": self.delete,
            "edit": self.edit,
            "search": self.search,
            "generate": self.generate
        }
        try:
            if command in available_commands:
                available_commands[command]()
            else:
                history.write(f"[red]Command not found: {command}[/red]")
        except Exception as e:
            history.write(f"[bold red]Error:[/bold red] {str(e)}")
        input_field.value = ""
        input_field.focus()