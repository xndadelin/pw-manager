import os
from dotenv import load_dotenv
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button as TextualButton, Static, Footer, Header, Input
from textual import on
from textual.screen import Screen


load_dotenv()

class Auth(Screen):
    CSS_PATH = "main.tcss"
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="auth_container"):
            yield Static("Enter master phrase \n This is supposed to be a locally run application, but in order to get access to this as a demo, use the master phrase: eiffel-africa-musk-kiss-fly-believe", id="auth_title")
            yield Input(placeholder="Phrase", id="phrase_input", password=True)
            yield TextualButton(label="Login", id="login_button", variant="primary")
            yield TextualButton(label="Go back", id="back_button", variant="primary")

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
    
    @on(TextualButton.Pressed, "#back_button")
    def handle_back_button_pressed(self) -> None:
        self.app.pop_screen()