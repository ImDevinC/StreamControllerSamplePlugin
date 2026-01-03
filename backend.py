from streamcontroller_plugin_tools import BackendBase

from loguru import logger as log


class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        log.info("Sample Plugin Backend initialized.")

    def on_advanced_action_triggered(self):
        log.info("Advanced Action Triggered in Backend!")
        self.frontend.trigger_event(
            event_id="com_imdevinc_StreamControllerSamplePlugin::AdvancedEvent",
            data={"message": "Advanced Action was triggered!"}
        )


backend = Backend()
