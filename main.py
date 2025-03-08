from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.containers import Vertical
from textual.widgets import Button as TextualButton, Static, Header, Footer
from textual import on
from screens.auth.auth import Auth
from screens.cli.cli import CLI
from screens.generate.generate import Generate

class Presentation(Widget):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, )
        yield Static("""
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗       
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║       
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║       
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║       
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗  
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝  
                                                                   
██████╗  █████╗ ███████╗███████╗██████╗                            
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗                           
██████╔╝███████║███████╗█████╗  ██║  ██║                           
██╔══██╗██╔══██║╚════██║██╔══╝  ██║  ██║                           
██████╔╝██║  ██║███████║███████╗██████╔╝                           
╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═════╝                            
                                                                   
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                   
███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗      
████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗     
██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝     
██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗     
██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║     
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝     
This password manager is a simple application that allows you to store your passwords in a secure way.
        """, id="ascii_art", classes="static_header")

class Choice(Widget):
    def compose(self) -> ComposeResult:
      yield Static("""
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣠⣀⣀⣀⣠⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⣦⣤⣤⣤⣤⣤⣤⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣤⣤⣤⣤
⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁
⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀
⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""", id="ascii_art")
      with Vertical(id="buttons_container"):
            yield TextualButton(label="Authenticate & start using the password manager", id="authenticate_button", variant="primary")
            yield TextualButton(label="Quit", id="quit_button", variant="error")
            yield TextualButton(label="Generate a random password", id="generate_button", variant="primary")

      yield Footer()

    @on(TextualButton.Pressed, '#authenticate_button')
    def show_auth(self) -> None:
        self.app.push_screen("Auth")

    @on(TextualButton.Pressed, '#quit_button')
    def quit(self) -> None:
        self.exit()

    @on(TextualButton.Pressed, '#generate_button')
    def show_generate(self) -> None:
        self.app.push_screen("Generate")

    

class PasswordManager(App):
    CSS_PATH = "main.tcss"
    SCREENS = {
        "Auth": Auth,
        "CLI": CLI,
        "Generate": Generate
    }
    def compose(self) -> ComposeResult:
        yield Presentation()
        yield Choice()

if __name__ == "__main__":
    app = PasswordManager()
    app.run()