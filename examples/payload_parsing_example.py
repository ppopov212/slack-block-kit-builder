#!/usr/bin/env python3
"""Example usage of Message.from_payload functionality."""

import json

from slack_blocksmith.message import Message

# Example payload from Slack
slack_payload = {
    "blocks": [
        {
            "type": "header",
            "block_id": "K67Rr",
            "text": {
                "type": "plain_text",
                "text": ":api2: Integration Tests Results :api2:",
                "emoji": True,
            },
        },
        {
            "type": "context",
            "block_id": "pA80d",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "&gt;*Environment*: `staging`  |  *Branch*: `master`",
                    "verbatim": False,
                }
            ],
        },
        {"type": "divider", "block_id": "6MYH6"},
        {
            "type": "section",
            "block_id": "LIdd9",
            "accessory": {
                "type": "button",
                "action_id": "workflow_btn_clicked",
                "style": "danger",
                "text": {"type": "plain_text", "text": ":github-white:", "emoji": True},
                "url": "https://example.com",
            },
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": ":x: qa_platform *0.00%* (0/0)",
                    "verbatim": False,
                },
                {"type": "mrkdwn", "text": "*Something went wrong*", "verbatim": False},
            ],
        },
        {
            "type": "actions",
            "block_id": "Xt2Cs",
            "elements": [
                {
                    "type": "button",
                    "action_id": "workflow_btn_clicked",
                    "text": {
                        "type": "plain_text",
                        "text": ":github-white: Workflow",
                        "emoji": True,
                    },
                    "style": "primary",
                    "url": "https://example.com",
                },
                {
                    "type": "button",
                    "action_id": "ai_analysis_clicked",
                    "text": {
                        "type": "plain_text",
                        "text": ":robot_face: AI Analysis",
                        "emoji": True,
                    },
                    "style": "primary",
                },
            ],
        },
    ]
}


def main():
    """Demonstrate the usage of Message.from_payload."""
    print("=== Slack Blocksmith: Message.from_payload Example ===\n")

    # Parse the Slack payload into a Message object
    print("1. Parsing Slack payload into Message object...")
    message = Message.from_payload(slack_payload)
    print(f"   ✓ Parsed {len(message.blocks)} blocks successfully")

    # You can also parse from JSON string
    print("\n2. Parsing from JSON string...")
    json_payload = json.dumps(slack_payload)
    message_from_json = Message.from_payload(json_payload)
    print(f"   ✓ Parsed {len(message_from_json.blocks)} blocks from JSON string")

    # Modify the message
    print("\n3. Modifying the message...")
    modified_message = message.add_section("This is a new section added after parsing!")
    print(f"   ✓ Added new section, total blocks: {len(modified_message.blocks)}")

    # Build back to dictionary for Slack API
    print("\n4. Building back to dictionary for Slack API...")
    built_message = modified_message.build()
    print(f"   ✓ Built message with {len(built_message['blocks'])} blocks")

    # Show the structure
    print("\n5. Message structure:")
    for i, block in enumerate(built_message["blocks"]):
        print(f"   Block {i + 1}: {block['type']} (id: {block.get('block_id', 'N/A')})")

    print("\n=== Example Complete ===")
    print("\nUsage in your Slack app:")
    print("```python")
    print("# In your action handler:")
    print("def handle_button_click(payload):")
    print("    # Parse the message from Slack payload")
    print("    message = Message.from_payload(payload['message'])")
    print("    ")
    print("    # Modify the message")
    print("    updated_message = message.add_section('Button was clicked!')")
    print("    ")
    print("    # Update the message in Slack")
    print("    slack_client.chat_update(")
    print("        channel=payload['channel']['id'],")
    print("        ts=payload['message']['ts'],")
    print("        blocks=updated_message.build()['blocks']")
    print("    )")
    print("```")


if __name__ == "__main__":
    main()
