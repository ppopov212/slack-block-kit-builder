"""Message builders for Slack Block Kit."""

import json
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator

from .blocks import (
    Actions,
    Block,
    Context,
    Divider,
    File,
    Header,
    ImageBlock,
    Input,
    RichText,
    Section,
    Video,
)
from .composition import MrkdwnText, PlainText
from .elements import Element
from .validators import SlackConstraints


class Message(BaseModel):
    """Message builder for Slack Block Kit."""

    blocks: List[Block] = Field(default_factory=list)
    response_type: Optional[Literal["in_channel", "ephemeral"]] = None
    replace_original: Optional[bool] = None
    delete_original: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

    @field_validator("blocks")
    @classmethod
    def validate_blocks(cls, v: List[Block]) -> List[Block]:
        """Validate number of blocks."""
        if len(v) > SlackConstraints.MAX_BLOCKS_PER_MESSAGE:
            raise ValueError(
                f"Number of blocks {len(v)} exceeds maximum of {SlackConstraints.MAX_BLOCKS_PER_MESSAGE}"
            )
        return v

    def build(self) -> Dict[str, Any]:
        """Build the message as a dictionary."""
        result = {"blocks": [block.build() for block in self.blocks]}
        if self.response_type is not None:
            result["response_type"] = self.response_type  # type: ignore[assignment]
        if self.replace_original is not None:
            result["replace_original"] = self.replace_original  # type: ignore[assignment]
        if self.delete_original is not None:
            result["delete_original"] = self.delete_original  # type: ignore[assignment]
        if self.metadata is not None:
            result["metadata"] = self.metadata  # type: ignore[assignment]
        return result

    @classmethod
    def create(cls) -> "Message":
        """Create a message with builder pattern."""
        return cls()

    def add_block(self, block: Block) -> "Message":
        """Add a block and return self for chaining."""
        self.blocks.append(block)
        return self

    def add_section(
        self,
        text: Optional[Union[str, PlainText, MrkdwnText]] = None,
        fields: Optional[List[Union[str, PlainText, MrkdwnText]]] = None,
        accessory: Optional[Element] = None,
        block_id: Optional[str] = None,
    ) -> "Message":
        """Add a section block and return self for chaining."""
        section = Section.create(
            text=text, fields=fields, accessory=accessory, block_id=block_id
        )
        self.blocks.append(section)
        return self

    def add_divider(self, block_id: Optional[str] = None) -> "Message":
        """Add a divider block and return self for chaining."""
        divider = Divider.create(block_id=block_id)
        self.blocks.append(divider)
        return self

    def add_image(
        self,
        image_url: str,
        alt_text: str,
        title: Optional[str] = None,
        block_id: Optional[str] = None,
    ) -> "Message":
        """Add an image block and return self for chaining."""
        image = ImageBlock.create(
            image_url=image_url,
            alt_text=alt_text,
            title=title,
            block_id=block_id,
        )
        self.blocks.append(image)
        return self

    def add_actions(
        self, elements: List[Element], block_id: Optional[str] = None
    ) -> "Message":
        """Add an actions block and return self for chaining."""
        actions = Actions.create(elements=elements, block_id=block_id)
        self.blocks.append(actions)
        return self

    def add_context(
        self,
        elements: List[Union[Element, str]],
        block_id: Optional[str] = None,
    ) -> "Message":
        """Add a context block and return self for chaining."""
        context_elements: List[Union[PlainText, MrkdwnText, Element]] = []
        for element in elements:
            if isinstance(element, str):
                context_elements.append(PlainText.create(element))
            else:
                context_elements.append(element)

        context = Context.create(elements=context_elements, block_id=block_id)
        self.blocks.append(context)
        return self

    def add_input(
        self,
        label: str,
        element: Element,
        hint: Optional[str] = None,
        optional: Optional[bool] = None,
        dispatch_action: Optional[bool] = None,
        block_id: Optional[str] = None,
    ) -> "Message":
        """Add an input block and return self for chaining."""
        input_block = Input.create(
            label=label,
            element=element,
            hint=hint,
            optional=optional,
            dispatch_action=dispatch_action,
            block_id=block_id,
        )
        self.blocks.append(input_block)
        return self

    def add_file(self, external_id: str, block_id: Optional[str] = None) -> "Message":
        """Add a file block and return self for chaining."""
        file_block = File.create(external_id=external_id, block_id=block_id)
        self.blocks.append(file_block)
        return self

    def add_header(self, text: str, block_id: Optional[str] = None) -> "Message":
        """Add a header block and return self for chaining."""
        header = Header.create(text=text, block_id=block_id)
        self.blocks.append(header)
        return self

    def add_video(
        self,
        title: str,
        video_url: str,
        title_url: Optional[str] = None,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        alt_text: Optional[str] = None,
        author_name: Optional[str] = None,
        provider_name: Optional[str] = None,
        provider_icon_url: Optional[str] = None,
        block_id: Optional[str] = None,
    ) -> "Message":
        """Add a video block and return self for chaining."""
        video = Video.create(
            title=title,
            video_url=video_url,
            title_url=title_url,
            description=description,
            thumbnail_url=thumbnail_url,
            alt_text=alt_text,
            author_name=author_name,
            provider_name=provider_name,
            provider_icon_url=provider_icon_url,
            block_id=block_id,
        )
        self.blocks.append(video)
        return self

    def add_rich_text(
        self, elements: List[Dict[str, Any]], block_id: Optional[str] = None
    ) -> "Message":
        """Add a rich text block and return self for chaining."""
        rich_text = RichText.create(elements=elements, block_id=block_id)
        self.blocks.append(rich_text)
        return self

    def set_response_type(
        self, response_type: Literal["in_channel", "ephemeral"]
    ) -> "Message":
        """Set response type and return self for chaining."""
        self.response_type = response_type
        return self

    def set_replace_original(self, replace: bool) -> "Message":
        """Set replace original and return self for chaining."""
        self.replace_original = replace
        return self

    def set_delete_original(self, delete: bool) -> "Message":
        """Set delete original and return self for chaining."""
        self.delete_original = delete
        return self

    def set_metadata(self, metadata: Dict[str, Any]) -> "Message":
        """Set metadata and return self for chaining."""
        self.metadata = metadata
        return self

    # Direct object methods
    def add_section_block(self, section: Section) -> "Message":
        """Add a section block directly and return self for chaining."""
        self.blocks.append(section)
        return self

    def add_divider_block(self, divider: Divider) -> "Message":
        """Add a divider block directly and return self for chaining."""
        self.blocks.append(divider)
        return self

    def add_image_block(self, image: ImageBlock) -> "Message":
        """Add an image block directly and return self for chaining."""
        self.blocks.append(image)
        return self

    def add_actions_block(self, actions: Actions) -> "Message":
        """Add an actions block directly and return self for chaining."""
        self.blocks.append(actions)
        return self

    def add_context_block(self, context: Context) -> "Message":
        """Add a context block directly and return self for chaining."""
        self.blocks.append(context)
        return self

    def add_input_block(self, input_block: Input) -> "Message":
        """Add an input block directly and return self for chaining."""
        self.blocks.append(input_block)
        return self

    def add_file_block(self, file_block: File) -> "Message":
        """Add a file block directly and return self for chaining."""
        self.blocks.append(file_block)
        return self

    def add_header_block(self, header: Header) -> "Message":
        """Add a header block directly and return self for chaining."""
        self.blocks.append(header)
        return self

    def add_video_block(self, video: Video) -> "Message":
        """Add a video block directly and return self for chaining."""
        self.blocks.append(video)
        return self

    def add_rich_text_block(self, rich_text: RichText) -> "Message":
        """Add a rich text block directly and return self for chaining."""
        self.blocks.append(rich_text)
        return self

    @classmethod
    def from_payload(cls, payload: Union[str, Dict[str, Any]]) -> "Message":
        """Create a Message from a Slack payload JSON.

        Args:
            payload: Either a JSON string or a dictionary containing the Slack payload

        Returns:
            A Message object reconstructed from the payload

        Raises:
            ValueError: If the payload is invalid or cannot be parsed
        """
        if isinstance(payload, str):
            try:
                payload_dict = json.loads(payload)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON payload: {e}") from e
        else:
            payload_dict = payload

        if not isinstance(payload_dict, dict):
            raise ValueError("Payload must be a dictionary")

        # Extract blocks from payload
        blocks_data = payload_dict.get("blocks", [])
        if blocks_data is not None and not isinstance(blocks_data, list):
            raise ValueError("Blocks must be a list")

        # Parse blocks
        parsed_blocks = []
        for block_data in blocks_data:
            if not isinstance(block_data, dict):
                raise ValueError("Each block must be a dictionary")
            parsed_block = cls._parse_block(block_data)
            parsed_blocks.append(parsed_block)

        # Create message with parsed blocks
        message = cls(blocks=parsed_blocks)

        # Set other message properties if present
        if "response_type" in payload_dict:
            message.response_type = payload_dict["response_type"]
        if "replace_original" in payload_dict:
            message.replace_original = payload_dict["replace_original"]
        if "delete_original" in payload_dict:
            message.delete_original = payload_dict["delete_original"]
        if "metadata" in payload_dict:
            message.metadata = payload_dict["metadata"]

        return message

    @staticmethod
    def _parse_block(block_data: Dict[str, Any]) -> Block:
        """Parse a single block from JSON data."""
        block_type = block_data.get("type")
        if not block_type:
            raise ValueError("Block must have a type")

        block_id = block_data.get("block_id")

        if block_type == "section":
            return Message._parse_section_block(block_data, block_id)
        elif block_type == "divider":
            return Divider.create(block_id=block_id)
        elif block_type == "image":
            return Message._parse_image_block(block_data, block_id)
        elif block_type == "actions":
            return Message._parse_actions_block(block_data, block_id)
        elif block_type == "context":
            return Message._parse_context_block(block_data, block_id)
        elif block_type == "input":
            return Message._parse_input_block(block_data, block_id)
        elif block_type == "file":
            return Message._parse_file_block(block_data, block_id)
        elif block_type == "header":
            return Message._parse_header_block(block_data, block_id)
        elif block_type == "video":
            return Message._parse_video_block(block_data, block_id)
        elif block_type == "rich_text":
            return Message._parse_rich_text_block(block_data, block_id)
        else:
            raise ValueError(f"Unsupported block type: {block_type}")

    @staticmethod
    def _parse_section_block(
        block_data: Dict[str, Any], block_id: Optional[str]
    ) -> Section:
        """Parse a section block from JSON data."""
        text = None
        if "text" in block_data:
            text = Message._parse_text_object(block_data["text"])

        fields = None
        if "fields" in block_data:
            fields = [
                Message._parse_text_object(field) for field in block_data["fields"]
            ]

        accessory = None
        if "accessory" in block_data:
            accessory = Message._parse_element(block_data["accessory"])

        return Section.create(
            text=text, fields=fields, accessory=accessory, block_id=block_id
        )

    @staticmethod
    def _parse_image_block(
        block_data: Dict[str, Any], block_id: Optional[str]
    ) -> ImageBlock:
        """Parse an image block from JSON data."""
        image_url = block_data.get("image_url")
        alt_text = block_data.get("alt_text")

        if not image_url or not alt_text:
            raise ValueError("Image block must have image_url and alt_text")

        title = None
        if "title" in block_data:
            title = Message._parse_text_object(block_data["title"])

        return ImageBlock.create(
            image_url=image_url,
            alt_text=alt_text,
            title=title.text if title else None,
            block_id=block_id,
        )

    @staticmethod
    def _parse_actions_block(
        block_data: Dict[str, Any], block_id: Optional[str]
    ) -> Actions:
        """Parse an actions block from JSON data."""
        elements_data = block_data.get("elements", [])
        elements = [Message._parse_element(elem) for elem in elements_data]
        return Actions.create(elements=elements, block_id=block_id)

    @staticmethod
    def _parse_context_block(
        block_data: Dict[str, Any], block_id: Optional[str]
    ) -> Context:
        """Parse a context block from JSON data."""
        elements_data = block_data.get("elements", [])
        elements = []
        for elem_data in elements_data:
            if elem_data.get("type") in ["plain_text", "mrkdwn"]:
                elements.append(Message._parse_text_object(elem_data))
            else:
                elements.append(Message._parse_element(elem_data))
        return Context.create(elements=elements, block_id=block_id)

    @staticmethod
    def _parse_input_block(
        block_data: Dict[str, Any], block_id: Optional[str]
    ) -> Input:
        """Parse an input block from JSON data."""
        label_data = block_data.get("label")
        if not label_data:
            raise ValueError("Input block must have a label")
        label = Message._parse_text_object(label_data)

        element_data = block_data.get("element")
        if not element_data:
            raise ValueError("Input block must have an element")
        element = Message._parse_element(element_data)

        hint = None
        if "hint" in block_data:
            hint = Message._parse_text_object(block_data["hint"])

        optional = block_data.get("optional")
        dispatch_action = block_data.get("dispatch_action")

        return Input.create(
            label=label.text,
            element=element,
            hint=hint.text if hint else None,
            optional=optional,
            dispatch_action=dispatch_action,
            block_id=block_id,
        )

    @staticmethod
    def _parse_file_block(block_data: Dict[str, Any], block_id: Optional[str]) -> File:
        """Parse a file block from JSON data."""
        external_id = block_data.get("external_id")
        if not external_id:
            raise ValueError("File block must have external_id")
        return File.create(external_id=external_id, block_id=block_id)

    @staticmethod
    def _parse_header_block(
        block_data: Dict[str, Any], block_id: Optional[str]
    ) -> Header:
        """Parse a header block from JSON data."""
        text_data = block_data.get("text")
        if not text_data:
            raise ValueError("Header block must have text")
        text = Message._parse_text_object(text_data)
        return Header.create(text=text.text, block_id=block_id)

    @staticmethod
    def _parse_video_block(
        block_data: Dict[str, Any], block_id: Optional[str]
    ) -> Video:
        """Parse a video block from JSON data."""
        title_data = block_data.get("title")
        video_url = block_data.get("video_url")

        if not title_data or not video_url:
            raise ValueError("Video block must have title and video_url")

        title = Message._parse_text_object(title_data)

        title_url = block_data.get("title_url")
        description = block_data.get("description")
        thumbnail_url = block_data.get("thumbnail_url")
        alt_text = block_data.get("alt_text")
        author_name = block_data.get("author_name")
        provider_name = block_data.get("provider_name")
        provider_icon_url = block_data.get("provider_icon_url")

        return Video.create(
            title=title.text,
            video_url=video_url,
            title_url=title_url,
            description=description,
            thumbnail_url=thumbnail_url,
            alt_text=alt_text,
            author_name=author_name,
            provider_name=provider_name,
            provider_icon_url=provider_icon_url,
            block_id=block_id,
        )

    @staticmethod
    def _parse_rich_text_block(
        block_data: Dict[str, Any], block_id: Optional[str]
    ) -> RichText:
        """Parse a rich text block from JSON data."""
        elements = block_data.get("elements", [])
        return RichText.create(elements=elements, block_id=block_id)

    @staticmethod
    def _parse_text_object(text_data: Dict[str, Any]) -> Union[PlainText, MrkdwnText]:
        """Parse a text object from JSON data."""
        text_type = text_data.get("type")
        text = text_data.get("text")

        if not text_type or not text:
            raise ValueError("Text object must have type and text")

        if text_type == "plain_text":
            emoji = text_data.get("emoji")
            return PlainText.create(text=text, emoji=emoji)
        elif text_type == "mrkdwn":
            verbatim = text_data.get("verbatim")
            return MrkdwnText.create(text=text, verbatim=verbatim)
        else:
            raise ValueError(f"Unsupported text type: {text_type}")

    @staticmethod
    def _parse_element(element_data: Dict[str, Any]) -> Element:
        """Parse an element from JSON data."""
        element_type = element_data.get("type")
        if not element_type:
            raise ValueError("Element must have a type")

        if element_type == "button":
            return Message._parse_button_element(element_data)
        elif element_type == "checkboxes":
            return Message._parse_checkboxes_element(element_data)
        elif element_type == "datepicker":
            return Message._parse_datepicker_element(element_data)
        elif element_type == "timepicker":
            return Message._parse_timepicker_element(element_data)
        elif element_type == "datetimepicker":
            return Message._parse_datetimepicker_element(element_data)
        elif element_type == "email_text_input":
            return Message._parse_email_input_element(element_data)
        elif element_type == "number_input":
            return Message._parse_number_input_element(element_data)
        elif element_type == "plain_text_input":
            return Message._parse_plain_text_input_element(element_data)
        elif element_type == "url_text_input":
            return Message._parse_url_input_element(element_data)
        elif element_type == "radio_buttons":
            return Message._parse_radio_buttons_element(element_data)
        elif element_type == "static_select":
            return Message._parse_static_select_element(element_data)
        elif element_type == "external_select":
            return Message._parse_external_select_element(element_data)
        elif element_type == "users_select":
            return Message._parse_users_select_element(element_data)
        elif element_type == "conversations_select":
            return Message._parse_conversations_select_element(element_data)
        elif element_type == "channels_select":
            return Message._parse_channels_select_element(element_data)
        elif element_type == "multi_static_select":
            return Message._parse_multi_static_select_element(element_data)
        elif element_type == "multi_external_select":
            return Message._parse_multi_external_select_element(element_data)
        elif element_type == "overflow":
            return Message._parse_overflow_element(element_data)
        elif element_type == "file_input":
            return Message._parse_file_input_element(element_data)
        elif element_type == "rich_text_input":
            return Message._parse_rich_text_input_element(element_data)
        elif element_type == "image":
            return Message._parse_image_element(element_data)
        elif element_type == "multi_users_select":
            return Message._parse_multi_users_select_element(element_data)
        elif element_type == "multi_conversations_select":
            return Message._parse_multi_conversations_select_element(element_data)
        elif element_type == "multi_channels_select":
            return Message._parse_multi_channels_select_element(element_data)
        else:
            raise ValueError(f"Unsupported element type: {element_type}")

    @staticmethod
    def _parse_button_element(element_data: Dict[str, Any]) -> "Button":
        """Parse a button element from JSON data."""
        from .elements import Button

        text_data = element_data.get("text")
        action_id = element_data.get("action_id")

        if not text_data or not action_id:
            raise ValueError("Button must have text and action_id")

        text = Message._parse_text_object(text_data)

        url = element_data.get("url")
        value = element_data.get("value")
        style = element_data.get("style")

        return Button.create(
            text=text.text, action_id=action_id, url=url, value=value, style=style
        )

    # Add placeholder methods for other element types
    # For brevity, I'll implement the most common ones and add placeholders for others
    @staticmethod
    def _parse_checkboxes_element(element_data: Dict[str, Any]) -> "Checkboxes":
        """Parse a checkboxes element from JSON data."""
        from .elements import Checkboxes

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("Checkboxes must have action_id")

        options_data = element_data.get("options", [])
        options = [Message._parse_option(opt) for opt in options_data]

        checkbox = Checkboxes.create(action_id=action_id, options=options)

        if "initial_options" in element_data:
            initial_options = [
                Message._parse_option(opt) for opt in element_data["initial_options"]
            ]
            checkbox.initial_options = initial_options

        return checkbox

    @staticmethod
    def _parse_option(option_data: Dict[str, Any]) -> "Option":
        """Parse an option from JSON data."""
        from .elements import Option

        text_data = option_data.get("text")
        value = option_data.get("value")

        if not text_data or not value:
            raise ValueError("Option must have text and value")

        text = Message._parse_text_object(text_data)

        description = None
        if "description" in option_data:
            description = Message._parse_text_object(option_data["description"])

        url = option_data.get("url")

        return Option.create(
            text=text.text,
            value=value,
            description=description.text if description else None,
            url=url,
        )

    # Placeholder methods for other element types - these would be implemented similarly
    @staticmethod
    def _parse_datepicker_element(element_data: Dict[str, Any]) -> "DatePicker":
        """Parse a datepicker element from JSON data."""
        from .elements import DatePicker

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("DatePicker must have action_id")
        return DatePicker.create(action_id=action_id)

    @staticmethod
    def _parse_timepicker_element(element_data: Dict[str, Any]) -> "TimePicker":
        """Parse a timepicker element from JSON data."""
        from .elements import TimePicker

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("TimePicker must have action_id")
        return TimePicker.create(action_id=action_id)

    @staticmethod
    def _parse_datetimepicker_element(element_data: Dict[str, Any]) -> "DatetimePicker":
        """Parse a datetimepicker element from JSON data."""
        from .elements import DatetimePicker

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("DatetimePicker must have action_id")
        return DatetimePicker.create(action_id=action_id)

    @staticmethod
    def _parse_email_input_element(element_data: Dict[str, Any]) -> "EmailInput":
        """Parse an email input element from JSON data."""
        from .elements import EmailInput

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("EmailInput must have action_id")
        return EmailInput.create(action_id=action_id)

    @staticmethod
    def _parse_number_input_element(element_data: Dict[str, Any]) -> "NumberInput":
        """Parse a number input element from JSON data."""
        from .elements import NumberInput

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("NumberInput must have action_id")
        return NumberInput.create(action_id=action_id)

    @staticmethod
    def _parse_plain_text_input_element(
        element_data: Dict[str, Any],
    ) -> "PlainTextInput":
        """Parse a plain text input element from JSON data."""
        from .elements import PlainTextInput

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("PlainTextInput must have action_id")
        return PlainTextInput.create(action_id=action_id)

    @staticmethod
    def _parse_url_input_element(element_data: Dict[str, Any]) -> "URLInput":
        """Parse a URL input element from JSON data."""
        from .elements import URLInput

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("URLInput must have action_id")
        return URLInput.create(action_id=action_id)

    @staticmethod
    def _parse_radio_buttons_element(element_data: Dict[str, Any]) -> "RadioButtons":
        """Parse a radio buttons element from JSON data."""
        from .elements import RadioButtons

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("RadioButtons must have action_id")
        options_data = element_data.get("options", [])
        options = [Message._parse_option(opt) for opt in options_data]
        return RadioButtons.create(action_id=action_id, options=options)

    @staticmethod
    def _parse_static_select_element(element_data: Dict[str, Any]) -> "StaticSelect":
        """Parse a static select element from JSON data."""
        from .elements import StaticSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError("StaticSelect must have action_id and placeholder")
        placeholder = Message._parse_text_object(placeholder_data)
        options_data = element_data.get("options", [])
        options = (
            [Message._parse_option(opt) for opt in options_data]
            if options_data
            else None
        )
        return StaticSelect.create(
            action_id=action_id, placeholder=placeholder.text, options=options
        )

    @staticmethod
    def _parse_external_select_element(
        element_data: Dict[str, Any],
    ) -> "ExternalSelect":
        """Parse an external select element from JSON data."""
        from .elements import ExternalSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError("ExternalSelect must have action_id and placeholder")
        placeholder = Message._parse_text_object(placeholder_data)
        return ExternalSelect.create(action_id=action_id, placeholder=placeholder.text)

    @staticmethod
    def _parse_users_select_element(element_data: Dict[str, Any]) -> "UsersSelect":
        """Parse a users select element from JSON data."""
        from .elements import UsersSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError("UsersSelect must have action_id and placeholder")
        placeholder = Message._parse_text_object(placeholder_data)
        return UsersSelect.create(action_id=action_id, placeholder=placeholder.text)

    @staticmethod
    def _parse_conversations_select_element(
        element_data: Dict[str, Any],
    ) -> "ConversationsSelect":
        """Parse a conversations select element from JSON data."""
        from .elements import ConversationsSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError("ConversationsSelect must have action_id and placeholder")
        placeholder = Message._parse_text_object(placeholder_data)
        return ConversationsSelect.create(
            action_id=action_id, placeholder=placeholder.text
        )

    @staticmethod
    def _parse_channels_select_element(
        element_data: Dict[str, Any],
    ) -> "ChannelsSelect":
        """Parse a channels select element from JSON data."""
        from .elements import ChannelsSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError("ChannelsSelect must have action_id and placeholder")
        placeholder = Message._parse_text_object(placeholder_data)
        return ChannelsSelect.create(action_id=action_id, placeholder=placeholder.text)

    @staticmethod
    def _parse_multi_static_select_element(
        element_data: Dict[str, Any],
    ) -> "MultiStaticSelect":
        """Parse a multi static select element from JSON data."""
        from .elements import MultiStaticSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError("MultiStaticSelect must have action_id and placeholder")
        placeholder = Message._parse_text_object(placeholder_data)
        options_data = element_data.get("options", [])
        options = (
            [Message._parse_option(opt) for opt in options_data]
            if options_data
            else None
        )
        return MultiStaticSelect.create(
            action_id=action_id, placeholder=placeholder.text, options=options
        )

    @staticmethod
    def _parse_multi_external_select_element(
        element_data: Dict[str, Any],
    ) -> "MultiExternalSelect":
        """Parse a multi external select element from JSON data."""
        from .elements import MultiExternalSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError("MultiExternalSelect must have action_id and placeholder")
        placeholder = Message._parse_text_object(placeholder_data)
        return MultiExternalSelect.create(
            action_id=action_id, placeholder=placeholder.text
        )

    @staticmethod
    def _parse_overflow_element(element_data: Dict[str, Any]) -> "OverflowMenu":
        """Parse an overflow element from JSON data."""
        from .elements import OverflowMenu

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("OverflowMenu must have action_id")
        options_data = element_data.get("options", [])
        options = [Message._parse_option(opt) for opt in options_data]
        return OverflowMenu.create(action_id=action_id, options=options)

    @staticmethod
    def _parse_file_input_element(element_data: Dict[str, Any]) -> "FileInput":
        """Parse a file input element from JSON data."""
        from .elements import FileInput

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("FileInput must have action_id")
        return FileInput.create(action_id=action_id)

    @staticmethod
    def _parse_rich_text_input_element(element_data: Dict[str, Any]) -> "RichTextInput":
        """Parse a rich text input element from JSON data."""
        from .elements import RichTextInput

        action_id = element_data.get("action_id")
        if not action_id:
            raise ValueError("RichTextInput must have action_id")
        return RichTextInput.create(action_id=action_id)

    @staticmethod
    def _parse_image_element(element_data: Dict[str, Any]) -> "ImageElement":
        """Parse an image element from JSON data."""
        from .elements import Image as ImageElement

        image_url = element_data.get("image_url")
        alt_text = element_data.get("alt_text")
        if not image_url or not alt_text:
            raise ValueError("Image element must have image_url and alt_text")
        return ImageElement.create(image_url=image_url, alt_text=alt_text)

    @staticmethod
    def _parse_multi_users_select_element(
        element_data: Dict[str, Any],
    ) -> "MultiUsersSelect":
        """Parse a multi users select element from JSON data."""
        from .elements import MultiUsersSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError("MultiUsersSelect must have action_id and placeholder")
        placeholder = Message._parse_text_object(placeholder_data)
        return MultiUsersSelect.create(
            action_id=action_id, placeholder=placeholder.text
        )

    @staticmethod
    def _parse_multi_conversations_select_element(
        element_data: Dict[str, Any],
    ) -> "MultiConversationsSelect":
        """Parse a multi conversations select element from JSON data."""
        from .elements import MultiConversationsSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError(
                "MultiConversationsSelect must have action_id and placeholder"
            )
        placeholder = Message._parse_text_object(placeholder_data)
        return MultiConversationsSelect.create(
            action_id=action_id, placeholder=placeholder.text
        )

    @staticmethod
    def _parse_multi_channels_select_element(
        element_data: Dict[str, Any],
    ) -> "MultiChannelsSelect":
        """Parse a multi channels select element from JSON data."""
        from .elements import MultiChannelsSelect

        action_id = element_data.get("action_id")
        placeholder_data = element_data.get("placeholder")
        if not action_id or not placeholder_data:
            raise ValueError("MultiChannelsSelect must have action_id and placeholder")
        placeholder = Message._parse_text_object(placeholder_data)
        return MultiChannelsSelect.create(
            action_id=action_id, placeholder=placeholder.text
        )


class Modal(BaseModel):
    """Modal builder for Slack Block Kit."""

    type: Literal["modal"] = "modal"
    title: str
    blocks: List[Block] = Field(default_factory=list)
    submit: Optional[str] = None
    close: Optional[str] = None
    private_metadata: Optional[str] = None
    callback_id: Optional[str] = None
    clear_on_close: Optional[bool] = None
    notify_on_close: Optional[bool] = None
    external_id: Optional[str] = None

    @field_validator("blocks")
    @classmethod
    def validate_blocks(cls, v: List[Block]) -> List[Block]:
        """Validate number of blocks."""
        if len(v) > SlackConstraints.MAX_BLOCKS_PER_MODAL:
            raise ValueError(
                f"Number of blocks {len(v)} exceeds maximum of {SlackConstraints.MAX_BLOCKS_PER_MODAL}"
            )
        return v

    def build(self) -> Dict[str, Any]:
        """Build the modal as a dictionary."""
        # Validate block count before building
        if len(self.blocks) > SlackConstraints.MAX_BLOCKS_PER_MODAL:
            raise ValueError(
                f"Number of blocks {len(self.blocks)} exceeds maximum of {SlackConstraints.MAX_BLOCKS_PER_MODAL}"
            )
        result = {
            "type": self.type,
            "title": {"type": "plain_text", "text": self.title},
            "blocks": [block.build() for block in self.blocks],
        }
        if self.submit is not None:
            result["submit"] = {"type": "plain_text", "text": self.submit}
        if self.close is not None:
            result["close"] = {"type": "plain_text", "text": self.close}
        if self.private_metadata is not None:
            result["private_metadata"] = self.private_metadata
        if self.callback_id is not None:
            result["callback_id"] = self.callback_id
        if self.clear_on_close is not None:
            result["clear_on_close"] = self.clear_on_close  # type: ignore[assignment]
        if self.notify_on_close is not None:
            result["notify_on_close"] = self.notify_on_close  # type: ignore[assignment]
        if self.external_id is not None:
            result["external_id"] = self.external_id
        return result

    @classmethod
    def create(
        cls,
        title: str,
        submit: Optional[str] = None,
        close: Optional[str] = None,
        private_metadata: Optional[str] = None,
        callback_id: Optional[str] = None,
        clear_on_close: Optional[bool] = None,
        notify_on_close: Optional[bool] = None,
        external_id: Optional[str] = None,
    ) -> "Modal":
        """Create a modal with builder pattern."""
        return cls(
            title=title,
            submit=submit,
            close=close,
            private_metadata=private_metadata,
            callback_id=callback_id,
            clear_on_close=clear_on_close,
            notify_on_close=notify_on_close,
            external_id=external_id,
        )

    def add_block(self, block: Block) -> "Modal":
        """Add a block and return self for chaining."""
        self.blocks.append(block)
        return self

    def add_section(
        self,
        text: Optional[str] = None,
        fields: Optional[List[str]] = None,
        accessory: Optional[Element] = None,
        block_id: Optional[str] = None,
    ) -> "Modal":
        """Add a section block and return self for chaining."""
        section = Section.create(
            text=text, fields=fields, accessory=accessory, block_id=block_id
        )
        self.blocks.append(section)
        return self

    def add_divider(self, block_id: Optional[str] = None) -> "Modal":
        """Add a divider block and return self for chaining."""
        divider = Divider.create(block_id=block_id)
        self.blocks.append(divider)
        return self

    def add_image(
        self,
        image_url: str,
        alt_text: str,
        title: Optional[str] = None,
        block_id: Optional[str] = None,
    ) -> "Modal":
        """Add an image block and return self for chaining."""
        image = ImageBlock.create(
            image_url=image_url,
            alt_text=alt_text,
            title=title,
            block_id=block_id,
        )
        self.blocks.append(image)
        return self

    def add_actions(
        self, elements: List[Element], block_id: Optional[str] = None
    ) -> "Modal":
        """Add an actions block and return self for chaining."""
        actions = Actions.create(elements=elements, block_id=block_id)
        self.blocks.append(actions)
        return self

    def add_context(
        self,
        elements: List[Union[Element, str]],
        block_id: Optional[str] = None,
    ) -> "Modal":
        """Add a context block and return self for chaining."""
        context_elements: List[Union[PlainText, MrkdwnText, Element]] = []
        for element in elements:
            if isinstance(element, str):
                context_elements.append(PlainText.create(element))
            else:
                context_elements.append(element)

        context = Context.create(elements=context_elements, block_id=block_id)
        self.blocks.append(context)
        return self

    def add_input(
        self,
        label: str,
        element: Element,
        hint: Optional[str] = None,
        optional: Optional[bool] = None,
        dispatch_action: Optional[bool] = None,
        block_id: Optional[str] = None,
    ) -> "Modal":
        """Add an input block and return self for chaining."""
        input_block = Input.create(
            label=label,
            element=element,
            hint=hint,
            optional=optional,
            dispatch_action=dispatch_action,
            block_id=block_id,
        )
        self.blocks.append(input_block)
        return self

    def add_file(self, external_id: str, block_id: Optional[str] = None) -> "Modal":
        """Add a file block and return self for chaining."""
        file_block = File.create(external_id=external_id, block_id=block_id)
        self.blocks.append(file_block)
        return self

    def add_header(self, text: str, block_id: Optional[str] = None) -> "Modal":
        """Add a header block and return self for chaining."""
        header = Header.create(text=text, block_id=block_id)
        self.blocks.append(header)
        return self

    def add_video(
        self,
        title: str,
        video_url: str,
        title_url: Optional[str] = None,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        alt_text: Optional[str] = None,
        author_name: Optional[str] = None,
        provider_name: Optional[str] = None,
        provider_icon_url: Optional[str] = None,
        block_id: Optional[str] = None,
    ) -> "Modal":
        """Add a video block and return self for chaining."""
        video = Video.create(
            title=title,
            video_url=video_url,
            title_url=title_url,
            description=description,
            thumbnail_url=thumbnail_url,
            alt_text=alt_text,
            author_name=author_name,
            provider_name=provider_name,
            provider_icon_url=provider_icon_url,
            block_id=block_id,
        )
        self.blocks.append(video)
        return self

    def add_rich_text(
        self, elements: List[Dict[str, Any]], block_id: Optional[str] = None
    ) -> "Modal":
        """Add a rich text block and return self for chaining."""
        rich_text = RichText.create(elements=elements, block_id=block_id)
        self.blocks.append(rich_text)
        return self

    def set_submit(self, text: str) -> "Modal":
        """Set submit button text and return self for chaining."""
        self.submit = text
        return self

    def set_close(self, text: str) -> "Modal":
        """Set close button text and return self for chaining."""
        self.close = text
        return self

    def set_private_metadata(self, metadata: str) -> "Modal":
        """Set private metadata and return self for chaining."""
        self.private_metadata = metadata
        return self

    def set_callback_id(self, callback_id: str) -> "Modal":
        """Set callback ID and return self for chaining."""
        self.callback_id = callback_id
        return self

    def set_clear_on_close(self, clear: bool) -> "Modal":
        """Set clear on close and return self for chaining."""
        self.clear_on_close = clear
        return self

    def set_notify_on_close(self, notify: bool) -> "Modal":
        """Set notify on close and return self for chaining."""
        self.notify_on_close = notify
        return self

    def set_external_id(self, external_id: str) -> "Modal":
        """Set external ID and return self for chaining."""
        self.external_id = external_id
        return self

    # Direct object methods
    def add_section_block(self, section: Section) -> "Modal":
        """Add a section block directly and return self for chaining."""
        self.blocks.append(section)
        return self

    def add_divider_block(self, divider: Divider) -> "Modal":
        """Add a divider block directly and return self for chaining."""
        self.blocks.append(divider)
        return self

    def add_image_block(self, image: ImageBlock) -> "Modal":
        """Add an image block directly and return self for chaining."""
        self.blocks.append(image)
        return self

    def add_actions_block(self, actions: Actions) -> "Modal":
        """Add an actions block directly and return self for chaining."""
        self.blocks.append(actions)
        return self

    def add_context_block(self, context: Context) -> "Modal":
        """Add a context block directly and return self for chaining."""
        self.blocks.append(context)
        return self

    def add_input_block(self, input_block: Input) -> "Modal":
        """Add an input block directly and return self for chaining."""
        self.blocks.append(input_block)
        return self

    def add_file_block(self, file_block: File) -> "Modal":
        """Add a file block directly and return self for chaining."""
        self.blocks.append(file_block)
        return self

    def add_header_block(self, header: Header) -> "Modal":
        """Add a header block directly and return self for chaining."""
        self.blocks.append(header)
        return self

    def add_video_block(self, video: Video) -> "Modal":
        """Add a video block directly and return self for chaining."""
        self.blocks.append(video)
        return self

    def add_rich_text_block(self, rich_text: RichText) -> "Modal":
        """Add a rich text block directly and return self for chaining."""
        self.blocks.append(rich_text)
        return self


class HomeTab(BaseModel):
    """Home tab builder for Slack Block Kit."""

    type: Literal["home"] = "home"
    blocks: List[Block] = Field(default_factory=list)
    private_metadata: Optional[str] = None
    callback_id: Optional[str] = None
    external_id: Optional[str] = None

    @field_validator("blocks")
    @classmethod
    def validate_blocks(cls, v: List[Block]) -> List[Block]:
        """Validate number of blocks."""
        if len(v) > SlackConstraints.MAX_BLOCKS_PER_HOME_TAB:
            raise ValueError(
                f"Number of blocks {len(v)} exceeds maximum of {SlackConstraints.MAX_BLOCKS_PER_HOME_TAB}"
            )
        return v

    def build(self) -> Dict[str, Any]:
        """Build the home tab as a dictionary."""
        # Validate block count before building
        if len(self.blocks) > SlackConstraints.MAX_BLOCKS_PER_HOME_TAB:
            raise ValueError(
                f"Number of blocks {len(self.blocks)} exceeds maximum of {SlackConstraints.MAX_BLOCKS_PER_HOME_TAB}"
            )
        result = {
            "type": self.type,
            "blocks": [block.build() for block in self.blocks],
        }
        if self.private_metadata is not None:
            result["private_metadata"] = self.private_metadata
        if self.callback_id is not None:
            result["callback_id"] = self.callback_id
        if self.external_id is not None:
            result["external_id"] = self.external_id
        return result

    @classmethod
    def create(
        cls,
        private_metadata: Optional[str] = None,
        callback_id: Optional[str] = None,
        external_id: Optional[str] = None,
    ) -> "HomeTab":
        """Create a home tab with builder pattern."""
        return cls(
            private_metadata=private_metadata,
            callback_id=callback_id,
            external_id=external_id,
        )

    def add_block(self, block: Block) -> "HomeTab":
        """Add a block and return self for chaining."""
        self.blocks.append(block)
        return self

    def add_section(
        self,
        text: Optional[Union[str, PlainText, MrkdwnText]] = None,
        fields: Optional[List[Union[str, PlainText, MrkdwnText]]] = None,
        accessory: Optional[Element] = None,
        block_id: Optional[str] = None,
    ) -> "HomeTab":
        """Add a section block and return self for chaining."""
        section = Section.create(
            text=text, fields=fields, accessory=accessory, block_id=block_id
        )
        self.blocks.append(section)
        return self

    def add_divider(self, block_id: Optional[str] = None) -> "HomeTab":
        """Add a divider block and return self for chaining."""
        divider = Divider.create(block_id=block_id)
        self.blocks.append(divider)
        return self

    def add_image(
        self,
        image_url: str,
        alt_text: str,
        title: Optional[str] = None,
        block_id: Optional[str] = None,
    ) -> "HomeTab":
        """Add an image block and return self for chaining."""
        image = ImageBlock.create(
            image_url=image_url,
            alt_text=alt_text,
            title=title,
            block_id=block_id,
        )
        self.blocks.append(image)
        return self

    def add_actions(
        self, elements: List[Element], block_id: Optional[str] = None
    ) -> "HomeTab":
        """Add an actions block and return self for chaining."""
        actions = Actions.create(elements=elements, block_id=block_id)
        self.blocks.append(actions)
        return self

    def add_context(
        self,
        elements: List[Union[Element, str]],
        block_id: Optional[str] = None,
    ) -> "HomeTab":
        """Add a context block and return self for chaining."""
        context_elements: List[Union[PlainText, MrkdwnText, Element]] = []
        for element in elements:
            if isinstance(element, str):
                context_elements.append(PlainText.create(element))
            else:
                context_elements.append(element)

        context = Context.create(elements=context_elements, block_id=block_id)
        self.blocks.append(context)
        return self

    def add_input(
        self,
        label: str,
        element: Element,
        hint: Optional[str] = None,
        optional: Optional[bool] = None,
        dispatch_action: Optional[bool] = None,
        block_id: Optional[str] = None,
    ) -> "HomeTab":
        """Add an input block and return self for chaining."""
        input_block = Input.create(
            label=label,
            element=element,
            hint=hint,
            optional=optional,
            dispatch_action=dispatch_action,
            block_id=block_id,
        )
        self.blocks.append(input_block)
        return self

    def add_file(self, external_id: str, block_id: Optional[str] = None) -> "HomeTab":
        """Add a file block and return self for chaining."""
        file_block = File.create(external_id=external_id, block_id=block_id)
        self.blocks.append(file_block)
        return self

    def add_header(self, text: str, block_id: Optional[str] = None) -> "HomeTab":
        """Add a header block and return self for chaining."""
        header = Header.create(text=text, block_id=block_id)
        self.blocks.append(header)
        return self

    def add_video(
        self,
        title: str,
        video_url: str,
        title_url: Optional[str] = None,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        alt_text: Optional[str] = None,
        author_name: Optional[str] = None,
        provider_name: Optional[str] = None,
        provider_icon_url: Optional[str] = None,
        block_id: Optional[str] = None,
    ) -> "HomeTab":
        """Add a video block and return self for chaining."""
        video = Video.create(
            title=title,
            video_url=video_url,
            title_url=title_url,
            description=description,
            thumbnail_url=thumbnail_url,
            alt_text=alt_text,
            author_name=author_name,
            provider_name=provider_name,
            provider_icon_url=provider_icon_url,
            block_id=block_id,
        )
        self.blocks.append(video)
        return self

    def add_rich_text(
        self, elements: List[Dict[str, Any]], block_id: Optional[str] = None
    ) -> "HomeTab":
        """Add a rich text block and return self for chaining."""
        rich_text = RichText.create(elements=elements, block_id=block_id)
        self.blocks.append(rich_text)
        return self

    def set_private_metadata(self, metadata: str) -> "HomeTab":
        """Set private metadata and return self for chaining."""
        self.private_metadata = metadata
        return self

    def set_callback_id(self, callback_id: str) -> "HomeTab":
        """Set callback ID and return self for chaining."""
        self.callback_id = callback_id
        return self

    def set_external_id(self, external_id: str) -> "HomeTab":
        """Set external ID and return self for chaining."""
        self.external_id = external_id
        return self

    # Direct object methods
    def add_section_block(self, section: Section) -> "HomeTab":
        """Add a section block directly and return self for chaining."""
        self.blocks.append(section)
        return self

    def add_divider_block(self, divider: Divider) -> "HomeTab":
        """Add a divider block directly and return self for chaining."""
        self.blocks.append(divider)
        return self

    def add_image_block(self, image: ImageBlock) -> "HomeTab":
        """Add an image block directly and return self for chaining."""
        self.blocks.append(image)
        return self

    def add_actions_block(self, actions: Actions) -> "HomeTab":
        """Add an actions block directly and return self for chaining."""
        self.blocks.append(actions)
        return self

    def add_context_block(self, context: Context) -> "HomeTab":
        """Add a context block directly and return self for chaining."""
        self.blocks.append(context)
        return self

    def add_input_block(self, input_block: Input) -> "HomeTab":
        """Add an input block directly and return self for chaining."""
        self.blocks.append(input_block)
        return self

    def add_file_block(self, file_block: File) -> "HomeTab":
        """Add a file block directly and return self for chaining."""
        self.blocks.append(file_block)
        return self

    def add_header_block(self, header: Header) -> "HomeTab":
        """Add a header block directly and return self for chaining."""
        self.blocks.append(header)
        return self

    def add_video_block(self, video: Video) -> "HomeTab":
        """Add a video block directly and return self for chaining."""
        self.blocks.append(video)
        return self

    def add_rich_text_block(self, rich_text: RichText) -> "HomeTab":
        """Add a rich text block directly and return self for chaining."""
        self.blocks.append(rich_text)
        return self
