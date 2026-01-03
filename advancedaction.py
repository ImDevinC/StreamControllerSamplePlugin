"""
Sample Advanced Action for StreamController
"""

from loguru import logger as log
from src.backend.PluginManager.ActionCore import ActionCore
from src.backend.DeckManagement.InputIdentifier import InputEvent, Input
from src.backend.PluginManager.PluginSettings.Asset import Icon
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.PluginManager.InputBases import Input

from GtkHelper.GenerativeUI.EntryRow import EntryRow


from gi.repository import Gtk, Adw
import gi


class AdvancedAction(ActionCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._state = 0

        # Register for icon change events
        self.icon_keys = ["main"]
        self.current_icon = self.get_icon("main")
        self.icon_name = "main"
        self.plugin_base.asset_manager.icons.add_listener(self._icon_changed)

        # Add event assigner for pressing the button
        self.add_event_assigner(
            EventAssigner(
                id="advanced-action",  # Unique ID for the event
                ui_label="Trigger Event",  # Label shown in the UI, must match the locales.csv
                default_event=Input.Key.Events.DOWN,  # Default event for the action
                callback=self._on_toggle,  # What should happen when the event is triggered
            )
        )

        # Add an entry row for chat message text
        self.message_row = EntryRow(
            action_core=self,
            var_name="chat.message_text",
            default_value="",
            title="chat-message-text",
            on_change=self._on_text_change,
            auto_add=False,
            complex_var_name=True,
        )

    def get_config_rows(self):
        """Return a list of configuration rows for the action settings UI."""
        return [self.message_row.widget]

    def on_ready(self):
        """Called when the action is fully initialized and ready."""
        super().on_ready()
        self.display_icon() # We can't display the icon until the action is ready

        # Subscribe to a custom event from the plugin. Do this is on-ready since it only gets called once
        log.debug("Subscribing to advanced event from plugin backend")
        self.plugin_base.connect_to_event(
            event_id="com_imdevinc_StreamControllerSamplePlugin::AdvancedEvent",
            callback=self._on_callback_event
        )

    def on_remove(self):
        """Called when the action is being removed.
        NOTE: This doesn't work currently, need to research why
        """
        super().on_remove()
        log.debug("Unsubscribing from advanced event from plugin backend")
        self.plugin_base.disconnect_from_event(
            event_id="com_imdevinc_StreamControllerSamplePlugin::AdvancedEvent",
            callback=self._on_callback_event
        )


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
        log.info("Advanced Action Triggered!")
        self.plugin_base.backend.on_advanced_action_triggered()

    def _on_callback_event(self, *args, **kwargs):
        """Handle the custom event from the plugin.
          Parameters:
            *args: A tuple where the first object is the event ID
            **kwargs: A dictionary containing the event ID and data payload in the format {"event_id": str, "data": dict}
        """

        log.info(
            f"Advanced Action received callback event from plugin backend! args: {args} kwargs: {kwargs}")

    def _on_text_change(self, widget: Gtk.Widget, new_value: str, old_value: str):
        """Handle text change in the entry row."""
        log.info(f"Chat message text changed to: {widget.get_text()}")
        log.info(f"New value: {new_value}, Old value: {old_value}")
