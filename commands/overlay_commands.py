from threading import Thread
from typing import Optional
from discord import (
    Attachment,
    app_commands,
    Interaction,
    Client,
)
from config import YAMLConfig as Config
import logging
from enum import Enum

from controllers.overlay_controller import OverlayController
from views.overlay.configure_modal import OverlayConfigurationModal

LOG = logging.getLogger(__name__)


class TextFields(Enum):
    title = "title"
    headerLeft = "headerLeft"
    headerRight = "headerRight"
    scrollingText = "scrollingText"
    sideBannerTextOne = "sideBannerTextOne"
    sideBannerTextTwo = "sideBannerTextTwo"
    sideBannerTextThree = "sideBannerTextThree"


class MediaFields(Enum):
    title = "title"
    headerIcon = "headerIcon"
    sideBannerIcon = "sideBannerIcon"
    backgroundVideo = "backgroundVideo"
    preRollVideo = "preRollVideo"


class AllFields(Enum):
    title = "title"
    timer = "timer"
    headerLeft = "headerLeft"
    headerRight = "headerRight"
    scrollingText = "scrollingText"
    sideBannerTextOne = "sideBannerTextOne"
    sideBannerTextTwo = "sideBannerTextTwo"
    sideBannerTextThree = "sideBannerTextThree"
    headerIcon = "headerIcon"
    sideBannerIcon = "sideBannerIcon"
    backgroundVideo = "backgroundVideo"
    preRollVideo = "preRollVideo"


class Switch(Enum):
    on = "on"
    off = "off"


@app_commands.guild_only()
class OverlayCommands(app_commands.Group, name="overlay"):
    def __init__(self, tree: app_commands.CommandTree, client: Client) -> None:
        super().__init__()
        self.tree = tree
        self.client = client

    @app_commands.command(name="set_text")
    @app_commands.checks.has_role("Mod")
    @app_commands.describe(field="Overlay field to set")
    @app_commands.describe(text="Text to set field to")
    async def set_text(self, interaction: Interaction, field: TextFields, text: str):
        """Set overlay text field to specified value"""
        OverlayController.publish_overlay({field.value: text})
        await interaction.response.send_message(
            "Overlay text update sent!", ephemeral=True
        )

    @app_commands.command(name="set_media")
    @app_commands.checks.has_role("Mod")
    @app_commands.describe(field="Overlay field to set")
    @app_commands.describe(media_url="URL of image to send to frontend")
    @app_commands.describe(media="Attachment image to send to frontend")
    async def set_media(
        self,
        interaction: Interaction,
        field: MediaFields,
        media_url: Optional[str] = None,
        media: Optional[Attachment] = None,
    ):
        """Set overlay image field to provided image"""
        if media is not None:
            media_url = media.url

        OverlayController.publish_overlay({field.value: media_url})
        await interaction.response.send_message(
            "Overlay image update sent!", ephemeral=True
        )

    @app_commands.command(name="clear_field")
    @app_commands.checks.has_role("Mod")
    @app_commands.describe(field="Overlay field to set")
    async def clear_field(self, interaction: Interaction, field: AllFields):
        """Clear value of field off overlay"""
        OverlayController.publish_overlay({field.value: None})
        await interaction.response.send_message(
            "Overlay clear update sent!", ephemeral=True
        )

    @app_commands.command(name="timer")
    @app_commands.checks.has_role("Mod")
    @app_commands.describe(duration="Duration in seconds of timer")
    async def timer(self, interaction: Interaction, duration: int):
        """Start timer on overlay for specified seconds"""
        OverlayController.publish_overlay({"timer": duration})
        await interaction.response.send_message("Overlay update sent!", ephemeral=True)

    @app_commands.command(name="toggle")
    @app_commands.checks.has_role("Mod")
    @app_commands.describe(switch="On/Off")
    async def toggle_overlay(self, interaction: Interaction, switch: Switch):
        """Toggle overlay to be on or off"""
        display = True
        if switch == Switch.off:
            display = False

        OverlayController.publish_overlay({"display": display})
        await interaction.response.send_message(
            f"Overlay toggled {switch.value}!", ephemeral=True
        )

    @app_commands.command(name="configure")
    @app_commands.checks.has_role("Mod")
    async def configure(self, interaction: Interaction):
        """Paste JSON configuration for overlay directly into modal"""
        await interaction.response.send_modal(OverlayConfigurationModal())
