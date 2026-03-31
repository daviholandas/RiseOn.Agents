"""Target selection dialog for generation.

T207-T214: Target selection dialog implementation.
"""

from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, RadioButton, RadioSet, Static

from riseon_agents.models.generation import GenerationLevel


@dataclass
class TargetSelectionResult:
    """Result of target selection dialog."""

    level: GenerationLevel | None
    cancelled: bool = False

    @classmethod
    def cancelled_result(cls) -> "TargetSelectionResult":
        """Create a cancelled result."""
        return cls(level=None, cancelled=True)

    @classmethod
    def selected(cls, level: GenerationLevel) -> "TargetSelectionResult":
        """Create a successful selection result."""
        return cls(level=level, cancelled=False)


class TargetSelectionDialog(ModalScreen[TargetSelectionResult]):
    """Dialog for selecting generation target (Local vs Global).

    Attributes:
        title: Dialog title
        message: Instructional message
    """

    DEFAULT_CSS = """
    TargetSelectionDialog {
        align: center middle;
    }

    TargetSelectionDialog > Container {
        width: 70;
        height: auto;
        max-height: 30;
        border: solid $primary;
        background: $surface;
        padding: 1 2;
    }

    TargetSelectionDialog > Container > Static {
        text-align: left;
        margin-bottom: 1;
    }

    TargetSelectionDialog > Container > RadioSet {
        margin: 1 0;
    }

    TargetSelectionDialog > Container > #buttons {
        height: auto;
        align: center middle;
    }

    TargetSelectionDialog > Container > #buttons > Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(
        self,
        title: str = "Select Generation Target",
        message: str = "Choose where to generate configuration files:",
    ) -> None:
        """Initialize the target selection dialog.

        Args:
            title: Dialog title.
            message: Instructional message.
        """
        super().__init__()
        self.title = title
        self.message = message
        self.selected_level: GenerationLevel = GenerationLevel.LOCAL

    def compose(self) -> ComposeResult:
        """Compose the dialog."""
        with Container():
            yield Static(self.title)
            yield Static(self.message)

            with RadioSet(id="target-radios"):
                yield RadioButton("Local (.kilo/ and .kilocode/)", id="local", value=True)
                yield RadioButton("Global (~/.kilocode/)", id="global", value=False)

            with Horizontal(id="buttons"):
                yield Button("Generate", id="generate", variant="primary")
                yield Button("Cancel", id="cancel")

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """Handle radio button selection."""
        radio_id = event.pressed.id
        if radio_id == "local":
            self.selected_level = GenerationLevel.LOCAL
        elif radio_id == "global":
            self.selected_level = GenerationLevel.GLOBAL

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "generate":
            self.dismiss(TargetSelectionResult.selected(self.selected_level))
        elif event.button.id == "cancel":
            self.dismiss(TargetSelectionResult.cancelled_result())

    def action_cancel(self) -> None:
        """Handle cancel action (ESC key)."""
        self.dismiss(TargetSelectionResult.cancelled_result())
