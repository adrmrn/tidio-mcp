from urllib.parse import urlencode

from core import _tool_call_succeed, mcp, tidio_api_client

_UNSET = object()

MAX_DISTINCT_ID_LENGTH = 55
MAX_PROPERTY_NAME_LENGTH = 128
MAX_PROPERTY_VALUE_LENGTH = 1000
EMAIL_CONSENT_VALUES = ("subscribed", "unsubscribed")


def strip_unset(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not _UNSET}


def strip_none(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def _validate_distinct_id(value) -> None:
    if not value:
        raise ValueError("Distinct ID must not be empty")
    if len(value) > MAX_DISTINCT_ID_LENGTH:
        raise ValueError(
            f"Distinct ID must not exceed {MAX_DISTINCT_ID_LENGTH} characters"
        )


def _validate_email_consent(value) -> None:
    if value not in EMAIL_CONSENT_VALUES:
        raise ValueError(
            f"Email consent must be one of: {', '.join(EMAIL_CONSENT_VALUES)}"
        )


def _validate_properties(properties) -> None:
    if not isinstance(properties, list):
        raise ValueError("Properties must be a list of objects")
    for prop in properties:
        if not isinstance(prop, dict):
            raise ValueError("Each property must be a dictionary object")
        if "name" not in prop or "value" not in prop:
            raise ValueError(
                "Each property must contain both 'name' and 'value' fields"
            )
        if len(str(prop["name"])) > MAX_PROPERTY_NAME_LENGTH:
            raise ValueError(
                f"Property name must not exceed {MAX_PROPERTY_NAME_LENGTH} characters"
            )
        if len(str(prop["value"])) > MAX_PROPERTY_VALUE_LENGTH:
            raise ValueError(
                f"Property value must not exceed {MAX_PROPERTY_VALUE_LENGTH} characters"
            )


@mcp.tool(title="Get Contacts")
def get_contacts(cursor: str = None, email: str = None) -> dict:
    """
    Get all contacts from Tidio. Contacts are customers that have contacted company via chat or email.

    This endpoint supports pagination. If the response contains meta.cursor with a non-null value,
    there are more results available. Pass that cursor value to the next request to fetch the next page.
    When meta.cursor is null, you've reached the end of the list.

    Args:
        cursor (str, optional): Pagination cursor from previous response. Use the value from meta.cursor
            to fetch the next page of results.
        email (str, optional): Filter contacts by email address. Must be a full, valid email address
            (wildcards not supported).

    Returns:
        Dict: A dictionary containing contacts information and pagination metadata.
    """
    endpoint = "/contacts"
    query_params = {}

    if cursor is not None:
        query_params["cursor"] = cursor

    if email is not None:
        query_params["email"] = email

    if query_params:
        endpoint += f"?{urlencode(query_params)}"

    response = tidio_api_client.get(endpoint)

    return _tool_call_succeed(data=response)


@mcp.tool(title="Get Contact details")
def get_contact_details(contact_id: str) -> dict:
    """
    Get details of a specific contact (customer) from Tidio.

    Args:
        contact_id (str): Required. The UUID of the contact to retrieve.

    Returns:
        Dict: A dictionary containing the contact details.
    """
    response = tidio_api_client.get(f"/contacts/{contact_id}")

    return _tool_call_succeed(data=response)


@mcp.tool(title="Create Contact")
def create_contact(
    distinct_id: str,
    email: str | None = None,
    phone: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email_consent: str | None = None,
    properties: list | None = None,
) -> dict:
    """
    Create a new contact in Tidio. Always creates a new contact; existing data is never overwritten.
    At least one of email, first_name, last_name, or phone must be provided.

    distinct_id is required and identifies the contact in your external system.
    If the user has not supplied a distinct_id, ASK them for it. Do NOT invent one
    or copy it from any other field — not from email, phone, name, email_consent, or
    any custom property.

    Args:
        distinct_id (str): Required. ID of the contact in the external system. Maximum 55 characters.
            Must be a real external-system identifier provided by the user. Never copy it
            from email, phone, name, or any other property. Ask the user if it is missing.
        email (str, optional): Contact email address in RFC822 format.
        phone (str, optional): Contact phone number.
        first_name (str, optional): Contact's first name.
        last_name (str, optional): Contact's last name.
        email_consent (str, optional): Email consent status.
            Must be one of: 'subscribed', 'unsubscribed'.
        properties (list, optional): List of custom contact properties.
            Each item must be a dict with 'name' (max 128 chars) and 'value' (max 1000 chars) fields.
            Example: [{"name": "plan", "value": "premium"}, {"name": "score", "value": 42}]

    Returns:
        Dict: A dictionary containing the created contact ID.

    Raises:
        ValueError: If any of the provided arguments have invalid values.
    """
    _validate_distinct_id(distinct_id)

    no_field_provided = all(
        field is None for field in (email, phone, first_name, last_name)
    )
    if no_field_provided:
        raise ValueError(
            "At least one of email, first_name, last_name, or phone must be provided"
        )

    if email_consent is not None:
        _validate_email_consent(email_consent)

    if properties is not None:
        _validate_properties(properties)

    contact_data = strip_none(
        distinct_id=distinct_id,
        email=email,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        email_consent=email_consent,
        properties=properties,
    )

    response = tidio_api_client.post("/contacts", json_data=contact_data)

    return _tool_call_succeed(data=response)


@mcp.tool(title="Update Contact")
def update_contact(
    contact_id: str,
    email: str | None = _UNSET,
    phone: str | None = _UNSET,
    first_name: str | None = _UNSET,
    last_name: str | None = _UNSET,
    email_consent: str | None = _UNSET,
    distinct_id: str = _UNSET,
    properties: list | None = _UNSET,
) -> dict:
    """
    Update a specific contact in Tidio. Pass only the fields you want to update.
    Omitted fields remain unchanged; null clears the field
    (except distinct_id, which cannot be cleared).

    Args:
        contact_id (str): Required. The UUID of the contact to update.
        email (str, optional): Contact email address in RFC822 format.
        phone (str, optional): Contact phone number.
        first_name (str, optional): Contact's first name.
        last_name (str, optional): Contact's last name.
        email_consent (str, optional): Email consent status.
            Must be one of: 'subscribed', 'unsubscribed'.
        distinct_id (str, optional): External system identifier. Maximum 55 characters.
            Cannot be cleared (null is not accepted).
        properties (list, optional): List of custom contact properties to update.
            Each item must be a dict with 'name' (max 128 chars) and 'value' (max 1000 chars) fields.
            Example: [{"name": "plan", "value": "premium"}, {"name": "score", "value": 42}]

    Returns:
        Dict: A dictionary with success status.

    Raises:
        ValueError: If any of the provided arguments have invalid values.
    """
    if not contact_id or not contact_id.strip():
        raise ValueError("Contact ID must not be empty")

    if email_consent is not _UNSET and email_consent is not None:
        _validate_email_consent(email_consent)

    if distinct_id is not _UNSET:
        _validate_distinct_id(distinct_id)

    if properties is not _UNSET and properties is not None:
        _validate_properties(properties)

    update_data = strip_unset(
        email=email,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        email_consent=email_consent,
        distinct_id=distinct_id,
        properties=properties,
    )

    if not update_data:
        raise ValueError("At least one parameter must be provided")

    tidio_api_client.patch(f"/contacts/{contact_id}", json_data=update_data)

    return _tool_call_succeed()


@mcp.tool(title="Delete Contact")
def delete_contact(contact_id: str) -> dict:
    """
    Delete a specific contact (customer) from Tidio.

    Args:
        contact_id (str): Required. The UUID of the contact to delete.

    Returns:
        Dict: A dictionary with success status.
    """
    tidio_api_client.delete(f"/contacts/{contact_id}")

    return _tool_call_succeed()


@mcp.tool(title="Get Contact Properties")
def get_contact_properties(cursor: str = None) -> dict:
    """
    Get all contact properties from Tidio. Contact properties are fields that can be associated
    with contacts, including default properties (name, email, phone, etc.) and custom ones.

    This endpoint supports pagination. If the response contains meta.cursor with a non-null value,
    there are more results available. Pass that cursor value to the next request to fetch the next page.
    When meta.cursor is null, you've reached the end of the list.

    Args:
        cursor (str, optional): Pagination cursor from previous response. Use the value from meta.cursor
            to fetch the next page of results.

    Returns:
        Dict: A dictionary containing contact properties and pagination metadata.
            Each property has: name (internal identifier), label (human-readable), and
            type (one of: text, number, email, phone, url).
    """
    endpoint = "/contact-properties"

    if cursor is not None:
        endpoint += f"?{urlencode({'cursor': cursor})}"

    response = tidio_api_client.get(endpoint)

    return _tool_call_succeed(data=response)
