"""Dialog screens for the TUI.

Implements T033: User Story 1 - Error screens for missing/empty agents folder.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static


class ErrorDialog(ModalScreen):
    """Generic error dialog with message and actions.

    Attributes:
        title: Dialog title
        message: Error message to display
        actions: List of (label, action_id) tuples for buttons
    """

    DEFAULT_CSS = """
    ErrorDialog {
        align: center middle;
    }
    
    ErrorDialog > Container {
        width: 60;
        height: auto;
        max-height: 20;
        border: solid $error;
        background: $surface;
        padding: 1 2;
    }
    
    ErrorDialog > Container > Label {
        text-align: center;
        text-style: bold;
        color: $error;
        margin-bottom: 1;
    }
    
    ErrorDialog > Container > Static {
        text-align: center;
        margin-bottom: 1;
    }
    
    ErrorDialog > Container > Vertical {
        height: auto;
        align: center middle;
    }
    
    ErrorDialog > Container > Vertical > Button {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        title: str,
        message: str,
        actions: list[tuple[str, str]] = None,
    ) -> None:
        """Initialize the error dialog.

        Args:
            title: Dialog title.
            message: Error message to display.
            actions: List of (label, action_id) tuples for buttons.
                     Defaults to [("OK", "ok")].
        """
        super().__init__()
        self.title = title
        self.message = message
        self.actions = actions or [("OK", "ok")]

    def compose(self) -> ComposeResult:
        """Compose the dialog."""
        with Container():
            yield Label(f"⚠ {self.title}")
            yield Static(self.message)

            with Vertical():
                for label, action_id in self.actions:
                    yield Button(label, id=action_id)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        self.dismiss(event.button.id)


class EmptyAgentsDialog(ErrorDialog):
    """Dialog shown when agents folder is empty or missing."""

    def __init__(self) -> None:
        """Initialize the empty agents dialog."""
        super().__init__(
            title="No Agents Found",
            message=(
                "The agents/ folder is empty or missing.\n\n"
                "Please create agent definitions in the agents/ folder "
                "before running this tool."
            ),
            actions=[
                ("Exit", "exit"),
            ],
        )


class ConfirmDialog(ModalScreen):
    """Confirmation dialog with Yes/No options.

    Attributes:
        title: Dialog title
        message: Message to display
    """

    DEFAULT_CSS = """
    ConfirmDialog {
        align: center middle;
    }
    
    ConfirmDialog > Container {
        width: 60;
        height: auto;
        max-height: 20;
        border: solid $primary;
        background: $surface;
        padding: 1 2;
    }
    
    ConfirmDialog > Container > Label {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    
    ConfirmDialog > Container > Static {
        text-align: center;
        margin-bottom: 1;
    }
    
    ConfirmDialog > Container > Vertical {
        height: auto;
        align: center middle;
    }
    
    ConfirmDialog > Container > Vertical > Button {
        margin: 0 1;
    }
    """

    def __init__(self, title: str, message: str) -> None:
        """Initialize the confirmation dialog.

        Args:
            title: Dialog title.
            message: Message to display.
        """
        super().__init__()
        self.title = title
        self.message = message

    def compose(self) -> ComposeResult:
        """Compose the dialog."""
        with Container():
            yield Label(self.title)
            yield Static(self.message)

            with Vertical():
                yield Button("Yes", id="yes", variant="primary")
                yield Button("No", id="no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        self.dismiss(event.button.id)


class ResultDialog(ModalScreen):
    """Dialog showing generation results.

    Attributes:
        title: Dialog title
        summary: Summary text to display
    """

    DEFAULT_CSS = """
    ResultDialog {
        align: center middle;
    }
    
    ResultDialog > Container {
        width: 70;
        height: auto;
        max-height: 30;
        border: solid $success;
        background: $surface;
        padding: 1 2;
    }
    
    ResultDialog > Container > Label {
        text-align: center;
        text-style: bold;
        color: $success;
        margin-bottom: 1;
    }
    
    ResultDialog > Container > Static {
        margin-bottom: 1;
    }
    
    ResultDialog > Container > Button {
        margin: 1 auto;
    }
    """

    def __init__(self, title: str, summary: str) -> None:
        """Initialize the result dialog.

        Args:
            title: Dialog title.
            summary: Summary text to display.
        """
        super().__init__()
        self.title = title
        self.summary = summary

    def compose(self) -> ComposeResult:
        """Compose the dialog."""
        with Container():
            yield Label(f"✓ {self.title}")
            yield Static(self.summary)
            yield Button("OK", id="ok", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        self.dismiss("ok")
