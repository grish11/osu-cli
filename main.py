from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static, Label, Button
from textual.containers import Center, Vertical, Horizontal
from textual.screen import Screen

from screens.audio import AudioLatencyScreen
from screens.system import SystemLatencyScreen
from screens.osu import OsuLatencyScreen

LOGO = r"""
               .x+=:.                       s                              
              z`    ^%                     :8                              
       u.        .   <k    x.    .        .88           u.    .d``         
 ...ue888b     .@8Ned8"  .@88k  z88u     :888ooo  ...ue888b   @8Ne.   .u   
 888R Y888r  .@^%8888"  ~"8888 ^8888   -*8888888  888R Y888r  %8888:u@88N  
 888R I888> x88:  `)8b.   8888  888R     8888     888R I888>   `888I  888. 
 888R I888> 8888N=*8888   8888  888R     8888     888R I888>    888I  888I 
 888R I888>  %8"    R88   8888  888R     8888     888R I888>    888I  888I 
u8888cJ888    @8Wou 9%    8888 ,888B .  .8888Lu= u8888cJ888   uW888L  888' 
 "*888*P"   .888888P`    "8888Y 8888"   ^%888*    "*888*P"   '*88888Nu88P  
   'Y"      `   ^"F       `Y"   'YP       'Y"       'Y"      ~ '88888F`    
                                                                888 ^      
                                                                *8E        
                                                                '8>        
                                                                 "         
"""

class osuLatencyApp(App):
    CSS_PATH = "main.tcss"
    BINDINGS = [("q", "quit", "Quit")]
    SCREENS = {
        "audio": AudioLatencyScreen,
        "system": SystemLatencyScreen,
        "osu": OsuLatencyScreen,
    }

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(LOGO, id="logo", markup=False)
        with Vertical(id="box"):
            yield Label(
                "please click the following buttons"
                " to explore the latency of your system,\n"
                "in correspondence to osu!lazer :)\n"
                " ** make sure your osu!lazer is running"
                " in the background! **"
            )
            with Horizontal():
                yield Button("Audio", id="audio", flat=True)
                yield Button("System", id="system", flat=True)
                yield Button("Osu", id="osu", flat=True)
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "flexoki"
        self.screen.set_focus(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.push_screen(event.button.id)


if __name__ == "__main__":
    app = osuLatencyApp()
    app.run()
