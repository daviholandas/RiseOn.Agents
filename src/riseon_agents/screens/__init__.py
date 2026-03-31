"""Textual screens for RiseOn.Agents.

This package contains screen definitions for the TUI application.
"""

from riseon_agents.screens.dialogs import (
    ConfirmDialog,
    EmptyAgentsDialog,
    ErrorDialog,
    ResultDialog,
)
from riseon_agents.screens.main import MainScreen
from riseon_agents.screens.splash import SplashScreen
from riseon_agents.screens.target_dialog import TargetSelectionDialog

__all__ = [
    "MainScreen",
    "ErrorDialog",
    "EmptyAgentsDialog",
    "ConfirmDialog",
    "ResultDialog",
    "SplashScreen",
    "TargetSelectionDialog",
]
