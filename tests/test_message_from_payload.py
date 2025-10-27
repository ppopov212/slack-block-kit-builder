"""Tests for Message.from_payload functionality."""

import json

import pytest

from slack_blocksmith.message import Message


class TestMessageFromPayload:
    """Test cases for Message.from_payload method."""

    def test_from_payload_with_empty_blocks(self):
        """Test parsing payload with empty blocks list."""
        payload = {"blocks": []}
        message = Message.from_payload(payload)
        assert len(message.blocks) == 0
        assert message.response_type is None

    def test_from_payload_with_json_string(self):
        """Test parsing payload from JSON string."""
        payload_dict = {"blocks": []}
        json_payload = json.dumps(payload_dict)
        message = Message.from_payload(json_payload)
        assert len(message.blocks) == 0

    def test_from_payload_with_message_properties(self):
        """Test parsing payload with message-level properties."""
        payload = {
            "blocks": [],
            "response_type": "ephemeral",
            "replace_original": True,
            "delete_original": False,
            "metadata": {"key": "value"},
        }
        message = Message.from_payload(payload)
        assert message.response_type == "ephemeral"
        assert message.replace_original is True
        assert message.delete_original is False
        assert message.metadata == {"key": "value"}

    def test_from_payload_with_header_block(self):
        """Test parsing payload with header block."""
        payload = {
            "blocks": [
                {
                    "type": "header",
                    "block_id": "test_header",
                    "text": {
                        "type": "plain_text",
                        "text": "Test Header",
                        "emoji": True,
                    },
                }
            ]
        }
        message = Message.from_payload(payload)
        assert len(message.blocks) == 1
        assert message.blocks[0].type == "header"
        assert message.blocks[0].block_id == "test_header"
        assert message.blocks[0].text.text == "Test Header"
        # Note: emoji defaults to None if not explicitly set
        assert message.blocks[0].text.emoji is None

    def test_from_payload_with_section_block(self):
        """Test parsing payload with section block."""
        payload = {
            "blocks": [
                {
                    "type": "section",
                    "block_id": "test_section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Bold text*",
                        "verbatim": False,
                    },
                    "fields": [
                        {"type": "plain_text", "text": "Field 1"},
                        {"type": "mrkdwn", "text": "*Field 2*"},
                    ],
                }
            ]
        }
        message = Message.from_payload(payload)
        assert len(message.blocks) == 1
        section = message.blocks[0]
        assert section.type == "section"
        assert section.block_id == "test_section"
        assert section.text.text == "*Bold text*"
        assert section.text.verbatim is False
        assert len(section.fields) == 2
        assert section.fields[0].text == "Field 1"
        assert section.fields[1].text == "*Field 2*"

    def test_from_payload_with_button_element(self):
        """Test parsing payload with button element."""
        payload = {
            "blocks": [
                {
                    "type": "actions",
                    "block_id": "test_actions",
                    "elements": [
                        {
                            "type": "button",
                            "action_id": "test_button",
                            "text": {"type": "plain_text", "text": "Click Me"},
                            "style": "primary",
                            "url": "https://example.com",
                        }
                    ],
                }
            ]
        }
        message = Message.from_payload(payload)
        assert len(message.blocks) == 1
        actions = message.blocks[0]
        assert actions.type == "actions"
        assert len(actions.elements) == 1
        button = actions.elements[0]
        assert button.type == "button"
        assert button.action_id == "test_button"
        assert button.text.text == "Click Me"
        assert button.style == "primary"
        assert button.url == "https://example.com"

    def test_from_payload_with_context_block(self):
        """Test parsing payload with context block."""
        payload = {
            "blocks": [
                {
                    "type": "context",
                    "block_id": "test_context",
                    "elements": [{"type": "mrkdwn", "text": "Context text"}],
                }
            ]
        }
        message = Message.from_payload(payload)
        assert len(message.blocks) == 1
        context = message.blocks[0]
        assert context.type == "context"
        assert len(context.elements) == 1
        assert context.elements[0].text == "Context text"

    def test_from_payload_can_modify_and_rebuild(self):
        """Test that parsed message can be modified and rebuilt."""
        payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "Original Header"},
                }
            ]
        }
        message = Message.from_payload(payload)

        # Modify the message
        modified_message = message.add_section("New section added!")

        # Build back to dictionary
        built = modified_message.build()
        assert len(built["blocks"]) == 2
        assert built["blocks"][0]["type"] == "header"
        assert built["blocks"][1]["type"] == "section"

    def test_from_payload_invalid_json_raises_error(self):
        """Test that invalid JSON raises ValueError."""
        with pytest.raises(ValueError, match="Invalid JSON payload"):
            Message.from_payload("invalid json")

    def test_from_payload_invalid_payload_type_raises_error(self):
        """Test that non-dict payload raises ValueError."""
        with pytest.raises(ValueError, match="Invalid JSON payload"):
            Message.from_payload("not a dict")

    def test_from_payload_invalid_blocks_type_raises_error(self):
        """Test that non-list blocks raises ValueError."""
        with pytest.raises(ValueError, match="Blocks must be a list"):
            Message.from_payload({"blocks": "not a list"})

    def test_from_payload_invalid_block_structure_raises_error(self):
        """Test that invalid block structure raises ValueError."""
        with pytest.raises(ValueError, match="Each block must be a dictionary"):
            Message.from_payload({"blocks": ["not a dict"]})

    def test_from_payload_missing_block_type_raises_error(self):
        """Test that missing block type raises ValueError."""
        with pytest.raises(ValueError, match="Block must have a type"):
            Message.from_payload({"blocks": [{"not_type": "test"}]})

    def test_from_payload_unsupported_block_type_raises_error(self):
        """Test that unsupported block type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported block type"):
            Message.from_payload({"blocks": [{"type": "unsupported_block"}]})

    def test_from_payload_complex_example(self):
        """Test parsing a complex real-world example."""
        payload = {
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
                        "text": {
                            "type": "plain_text",
                            "text": ":github-white:",
                            "emoji": True,
                        },
                        "url": "https://example.com",
                    },
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": ":x: qa_platform *0.00%* (0/0)",
                            "verbatim": False,
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Something went wrong*",
                            "verbatim": False,
                        },
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

        message = Message.from_payload(payload)
        assert len(message.blocks) == 5

        # Verify header
        assert message.blocks[0].type == "header"
        assert message.blocks[0].text.text == ":api2: Integration Tests Results :api2:"

        # Verify context
        assert message.blocks[1].type == "context"
        assert len(message.blocks[1].elements) == 1

        # Verify divider
        assert message.blocks[2].type == "divider"

        # Verify section with accessory
        section = message.blocks[3]
        assert section.type == "section"
        assert section.accessory.type == "button"
        assert section.accessory.action_id == "workflow_btn_clicked"
        assert section.accessory.style == "danger"
        assert len(section.fields) == 2

        # Verify actions
        actions = message.blocks[4]
        assert actions.type == "actions"
        assert len(actions.elements) == 2
        assert actions.elements[0].action_id == "workflow_btn_clicked"
        assert actions.elements[1].action_id == "ai_analysis_clicked"
