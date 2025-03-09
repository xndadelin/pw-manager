from textual.app import ComposeResult
from textual.widgets import Button as TextualButton, Static, Header, Footer
from textual import on
from textual.screen import Screen
from textual.containers import Vertical

class Generate(Screen):
    CSS_PATH = "main.tcss"
    password = ""
    
    def on_mount(self) -> None:
        self.password = ""
        self.generate_password()

    def generate_password(self) -> None:
        import random
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
        self.password = "".join(password)

        if hasattr(self, "password_display"):
            self.password_display.update(f"Your password is: {self.password}")

    def compose(self) -> ComposeResult:
        with Vertical(id="auth_container"):
            yield Header()
            self.password_display = Static(f"Your password is: {self.password}", id="password_display")
            yield self.password_display
            yield TextualButton("Generate", id="generate")
            yield TextualButton(label="Go back", id="back_button", variant="primary")
            yield Footer()

    @on(TextualButton.Pressed, "#generate")
    def on_generate(self) -> None:
        self.generate_password()
    
    @on(TextualButton.Pressed, "#back_button")
    def handle_back_button_pressed(self) -> None:
        self.app.pop_screen()
