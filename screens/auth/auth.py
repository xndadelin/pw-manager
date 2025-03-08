import os
from dotenv import load_dotenv
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button as TextualButton, Static, Footer, Header, Input
from textual import on
from textual.screen import Screen

load_dotenv()

class Auth(Screen):
    CSS_PATH = "main.tcss"
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Vertical(id="auth_container"):
            yield Static("Enter master phrase", id="auth_title")
            yield Input(placeholder="Phrase", id="phrase_input", password=True)
            yield TextualButton("Login", id="login_button", variant="primary")
        
        yield Footer()
    
    def on_mount(self) -> None:
        self.query_one("#phrase_input").focus()
    
    @on(Input.Submitted)
    def handle_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "phrase_input":
            self.login()
    
    @on(TextualButton.Pressed, "#login_button")
    def login(self) -> None:
        phrase = self.query_one("#phrase_input", Input).value
        
        if phrase == os.getenv("PHRASE"):
            self.app.pop_screen()
            self.app.push_screen("CLI")
        else:
            self.notify("Incorrect phrase. Please try again.", severity="error")