from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Button as TextualButton, Static, Header, Footer
from textual import on
from screens.auth.auth import Auth
from screens.cli.cli import CLI
from screens.generate.generate import Generate

class Presentation(Widget):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
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
This password manager is a simple local application that allows you to store your passwords in a secure way.
It uses a master phrase to encrypt and decrypt your passwords.
It also allows you to generate random passwords.
It uses the Fernet symmetric encryption algorithm to encrypt and decrypt your passwords.
It is a simple terminal application that is easy to use.
The master phrase and Fernet key are stored in a .env file.
The encrypted passwords are stored in a SQLite3 database.
TERMINAL CRAFT
        """, id="ascii_art", classes="static_header")

class Choice(Widget):
    def compose(self) -> ComposeResult:
        yield Static("""
@@@@@@@@@@BGBGP55YYYYYYY555PGGB#&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@P?YYYYYYYYYYYYYYYYYYYYYY55PGB#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&BG&@@@@@
@@@@@@@@5?YYYYYY~:7YYYYYJYYYYYYYYYYYYYYY5PB#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&#BP5YY#@@@@@@
@@@@@@@57YYYYYY7   JYYY~.:JYYYY?7JYYYYYYYYYYY5GB#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&#BGP5YYYYY5&@@@@@@@
@@@@@@57YYYYYYY:   7JJ^  ^YYYJ^  :YYYYYYJYYYYYYYYY5PPGB##&&&&@@@@@@&&&&&##BGGP55YYJYYYYYYY5&@&&&&&&&
@@@@@57JYYYYYY!      .   ?YYJ..!. JYYJ~...:JYYJYYYYYYYYYYYYY55555555YYYYYYYYYYJ!~^:^YYYYYYY5555YY5G&
@@@@G7JYYYYYY?   !J?!   !YY?..7J..YY7  ^?7~JY~ ^YYYYYYYYYYYYYYYYYYYYYYJ7JYY~~Y7 ~?: JYYYYYYYYYY5B&@@
@@@B7?YYYYYYY7.^?YY5?  :YY!      ^YJ. ^YYYYYY: :Y7^:JYYYYYJ~^~JY?.7YYY? ^YY~ !5^ ^!~.7YYYYYY5G#@@@@@
@@&?7YYYYYYYYYYYYYYY!:~JY! :??~  ?5!  JYYYYYJ. .: ^?YYYYY? :!~!Y7 :YYYY~ ?5? :YJ.^7~:?YYY5P#@@@@@@@@
@@57JY5555YYYYYYYYYYYYYYY??YYY: ~YY7  7JYYYY^ .. ^YYYYYYY~ ?5YYYJ. JYYYY..?7 :YY?!!?YY5P#&@@@@@@@@@@
@#7J&&&&&&&&&&##BGGP55YYYYYYYYJJYYYY~. .~YJ: :J?  !YYYYYY~ ~YYYYY^ 7J?7?J!^^~JYYYYY5G#&@@@@@@@@@@@@@
@Y7P@@@@@@@@@@@@@@@@@@&##BGP55YYYYYYYYJJYY?^7YYY: :YYYYYYJ: ^~^!Y7.:^^~7YYYYYYY5PB&@@@@@@@@@@@@@@@@@
#?7#@@@@@@@@@@@@@@@@@@@@@@@@@&&#BGP55YYYYYYYYYYYJ7?YYYYYYYY7~~!JYYYYYYYYYYY5PB#&@@@@@@@@@@@@@@@@@@@@
P7?&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&#BGGP555YYYYYYYYYYYYYYYYYYYYYY55PG#&@@@@@@@@@@@@@@@@@@@@@@@@@
J7J@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&###BBBBGGGGGGGGBB##&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
?7J@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                                                                                                                                                                                                     
""", id="ascii_art")
    
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