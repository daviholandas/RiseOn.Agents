"""Splash screen for RiseOn.Agents TUI application.

T605-T606: SplashScreen with ASCII art logo and 1.5s display timer.
Implements US6 - Complete Visual Redesign.
"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

ASCII_LOGO = r"""
██████╗ ██╗███████╗███████╗ ██████╗ ███╗   ██╗     █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗████╗  ██║    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝
██████╔╝██║███████╗█████╗  ██║   ██║██╔██╗ ██║    ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████╗
██╔══██╗██║╚════██║██╔══╝  ██║   ██║██║╚██╗██║    ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
██║  ██║██║███████║███████╗╚██████╔╝██║ ╚████║    ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████║
╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

               RiseOn.Agents — 🤖  Kilo Code Configuration Generator  🤖
"""


class SplashScreen(Screen[None]):
    """Splash screen displayed at application startup.

    T606: Displays ASCII art logo for DISPLAY_DURATION seconds,
    then automatically transitions to the main screen.
    """

    DISPLAY_DURATION: float = 1.5

    DEFAULT_CSS = """
    SplashScreen {
        align: center middle;
        background: $surface;
    }

    SplashScreen #logo {
        width: auto;
        height: auto;
        content-align: center middle;
        color: $success;
        text-style: bold;
    }

    SplashScreen #tagline {
        width: auto;
        height: auto;
        content-align: center middle;
        color: $accent;
        margin-top: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose splash screen with ASCII art logo."""
        yield Static(ASCII_LOGO, id="logo")
        yield Static("Generating Kilo Code configurations...", id="tagline")

    def on_mount(self) -> None:
        """Start the timer to auto-dismiss after DISPLAY_DURATION seconds."""
        self.set_timer(self.DISPLAY_DURATION, self._dismiss_splash)

    def _dismiss_splash(self) -> None:
        """Dismiss the splash screen."""
        self.dismiss()
