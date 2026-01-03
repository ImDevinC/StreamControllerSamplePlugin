"""
Sample Action for StreamController

This action demonstrates a simple toggle functionality. When the assigned input event is triggered,
it toggles a label on the button between "Sample Action Triggered!" and an empty string.
"""

from loguru import logger as log
from src.backend.PluginManager.ActionCore import ActionCore
from src.backend.DeckManagement.InputIdentifier import InputEvent, Input
from src.backend.PluginManager.PluginSettings.Asset import Icon
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.PluginManager.InputBases import Input

from gi.repository import Gtk, Adw
import gi


class SampleAction(ActionCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._state = 0

        # Register for icon change events
        self.icon_keys = ["main"]
        self.current_icon = self.get_icon("main")
        self.icon_name = "main"
        self.plugin_base.asset_manager.icons.add_listener(self._icon_changed)

        # Add event assigner for pressing the button
        self.event_manager.add_event_assigner(
            EventAssigner(
                id="toggle-action",  # Unique ID for the event
                ui_label="Toggle",  # Label shown in the UI
                default_event=Input.Key.Events.DOWN,  # Default event for the action
                callback=self._on_toggle,  # What should happen when the event is triggered
            )
        )

    def on_ready(self):
        """Called when the action is fully initialized and ready."""
        super().on_ready()
        self.display_icon() # We can't display the icon until the action is ready

    def _icon_changed(self, event: str, key: str, asset: Icon):
        """Handle icon change events from the asset manager."""
        if not key in self.icon_keys:
            return
        if key != self.icon_name:
            return
        self.current_icon = asset
        self.icon_name = key
        self.display_icon()

    def display_icon(self):
        """Display the current icon on the button."""
        if self.current_icon is not None:
            _, rendered = self.current_icon.get_values()
            self.set_media(image=rendered)


    def _on_toggle(self, _):
        """Handle the toggle action event."""
        log.info("Sample Action Triggered!")
        if self._state == 0:
            self.set_top_label("Sample Action Triggered!")
            self._state = 1
        else:
            self.set_top_label("")
            self._state = 0
