import os
from loguru import logger as log

from gi.repository import Gtk, Adw
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.EventHolder import EventHolder


from .sampleaction import SampleAction
from .advancedaction import AdvancedAction


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')


class SamplePlugin(PluginBase):
    def __init__(self):
        super().__init__(use_legacy_locale=False)
        self.name = "Sample Stream Controller Plugin"
        self.description = "A sample plugin for Stream Controller demonstrating basic functionality."
        self.version = "0.0.1"
        self.author = "Devin Collins <me@imdevinc.com>"

        # Add icons for the plugin using the icon manager
        self.add_icon("main", self.get_asset_path("info.png"))

        # Create sample action and register it
        sample_action = ActionHolder(
            plugin_base=self,
            action_base=SampleAction,
            action_id_suffix="sample_action",
            action_name="Sample Action"
        )
        self.add_action_holder(sample_action)
        log.debug("added sample action")

        advanced_action = ActionHolder(
            plugin_base=self,
            action_base=AdvancedAction,
            action_id_suffix="advanced_action",
            action_name="Advanced Action"
        )
        self.add_action_holder(advanced_action)
        log.debug("added advanced action")

        # Create event holder for callback events
        self._event_holder = EventHolder(
            plugin_base=self,
            event_id="com_imdevinc_StreamControllerSamplePlugin::AdvancedEvent",
        )
        self.add_event_holder(self._event_holder)

        # Initialize our backend and load it
        backend_path = os.path.join(self.PATH, "backend.py")
        self.launch_backend(
            backend_path=backend_path,
            venv_path=os.path.join(self.PATH, ".venv")
        )

        self.register(
            plugin_name="Sample Plugin",
            github_repo="https://github.com/imdevinc/StreamControllerSamplePlugin",
            plugin_version="0.0.1",
            app_version="1.6.0"
        )

    def trigger_event(self, event_id: str, data: dict):
        self._event_holder.trigger_event(event_id=event_id, data=data)
