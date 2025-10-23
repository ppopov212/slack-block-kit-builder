#!/usr/bin/env python3
"""Example demonstrating direct object methods for Message, Modal, and HomeTab.

This example shows how to use the new direct object methods that accept
pre-created block objects directly, providing more flexibility in block creation.

Note: Import directly from the message module to avoid package import issues.
"""

# Import directly from the message module
from slack_blocksmith.blocks import Actions, Divider, Header, Section
from slack_blocksmith.composition import MrkdwnText, PlainText
from slack_blocksmith.elements import Button
from slack_blocksmith.message import HomeTab, Message, Modal


def main():
    """Demonstrate direct object methods."""

    # Example 1: Message with direct object methods
    print("=== Message with Direct Object Methods ===")

    # Create blocks directly
    section = Section.create(
        text=MrkdwnText.create("*Hello World!*"), block_id="section1"
    )

    divider = Divider.create(block_id="divider1")

    header = Header.create(text="My Header", block_id="header1")

    # Create a button for actions
    button = Button.create(text="Click Me", action_id="button_click", value="clicked")

    actions = Actions.create(elements=[button], block_id="actions1")

    # Build message using direct object methods
    message = (
        Message.create()
        .add_section_block(section)
        .add_divider_block(divider)
        .add_header_block(header)
        .add_actions_block(actions)
    )

    print("Message JSON:")
    print(message.build())
    print()

    # Example 2: Modal with direct object methods
    print("=== Modal with Direct Object Methods ===")

    modal_section = Section.create(
        text=PlainText.create("Modal Content"), block_id="modal_section"
    )

    modal = (
        Modal.create("My Modal")
        .add_section_block(modal_section)
        .set_submit("Submit")
        .set_close("Cancel")
    )

    print("Modal JSON:")
    print(modal.build())
    print()

    # Example 3: HomeTab with direct object methods
    print("=== HomeTab with Direct Object Methods ===")

    home_section = Section.create(
        text=MrkdwnText.create("*Welcome to your Home Tab!*"), block_id="home_section"
    )

    home_tab = (
        HomeTab.create()
        .add_section_block(home_section)
        .set_private_metadata("home_data")
    )

    print("HomeTab JSON:")
    print(home_tab.build())


if __name__ == "__main__":
    main()
