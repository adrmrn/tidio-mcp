import os
from urllib.parse import urlencode

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from tidio_client import TidioApiClient

load_dotenv()

mcp = FastMCP("Tidio")

tidio_api_client = TidioApiClient(
    client_id=os.getenv("TIDIO_CLIENT_ID", ""),
    client_secret=os.getenv("TIDIO_CLIENT_SECRET", ""),
)


def _tool_call_succeed(data: dict = None) -> dict:
    return {
        "status": "ok",
        "data": data or {},
    }


@mcp.tool(title="Get Departments")
def get_departments() -> dict:
    """
    Get all departments from Tidio. Departments are a agent groups, and can be assigned to tickets.

    Returns:
        Dict: A dictionary containing departments information.
    """
    response = tidio_api_client.get("/departments")

    return _tool_call_succeed(data=response)


@mcp.tool(title="Get Operators")
def get_operators(cursor: str = None) -> dict:
    """
    Get all operators from Tidio. Operators are agents that manage tickets and contact with customers. Operator can be assigned to tickets.

    This endpoint supports pagination. If the response contains meta.cursor with a non-null value,
    there are more results available. Pass that cursor value to the next request to fetch the next page.
    When meta.cursor is null, you've reached the end of the list.

    Args:
        cursor (str, optional): Pagination cursor from previous response. Use the value from meta.cursor
            to fetch the next page of results.

    Returns:
        Dict: A dictionary containing operator information and pagination metadata.
    """
    endpoint = "/operators"

    if cursor is not None:
        endpoint += f"?{urlencode({'cursor': cursor})}"

    response = tidio_api_client.get(endpoint)

    return _tool_call_succeed(data=response)


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


@mcp.tool(title="Get Tickets")
def get_tickets() -> dict:
    """
    Get all tickets from Tidio. Use this to get tickets overview.

    Returns:
        Dict: A dictionary containing ticket information.
    """
    response = tidio_api_client.get("/tickets")

    return _tool_call_succeed(data=response)


@mcp.tool(title="Get Ticket details")
def get_ticket_details(ticket_id: int) -> dict:
    """
    Get details of a specific ticket from Tidio. Use this to get full ticket information including messages.

    Args:
        ticket_id (int): Required. The ID of the ticket to retrieve.

    Returns:
        Dict: A dictionary containing the ticket details.
    """
    response = tidio_api_client.get(f"/tickets/{ticket_id}")

    return _tool_call_succeed(data=response)


@mcp.tool(title="Delete Ticket")
def delete_ticket(ticket_id: int) -> dict:
    """
    Delete a specific ticket from Tidio.

    Args:
        ticket_id (int): Required. The ID of the ticket to delete.

    Returns:
        Dict: A dictionary with success status.
    """
    tidio_api_client.delete(f"/tickets/{ticket_id}")

    return _tool_call_succeed()


@mcp.tool(title="Create Ticket")
def create_ticket(
    contact_email: str,
    subject: str,
    message_content: str,
    assigned_department_id: str = None,
) -> dict:
    """
    Create a new ticket in Tidio. This tool creates a ticket from a customer's perspective.

    Args:
        contact_email (str): Required. Email of the customer creating the ticket.
        subject (str): Required. Subject of the ticket.
        message_content (str): Required. Ticket message content from the customer.
        assigned_department_id (str, optional): UUID of assigned department. When not provided, the General department is assigned as default.

    Returns:
        Dict: A dictionary containing the created ticket ID.
    """
    ticket_data = {
        "contact_email": contact_email,
        "subject": subject,
        "message_content": message_content,
    }

    if assigned_department_id is not None:
        ticket_data["assigned_department_id"] = assigned_department_id

    response = tidio_api_client.post("/tickets/as-contact", json_data=ticket_data)

    return _tool_call_succeed(data=response)


@mcp.tool(title="Update Ticket")
def update_ticket(
    ticket_id: int,
    status: str = None,
    priority: str = None,
    assigned: dict = None,
) -> dict:
    """
    Update a specific ticket from Tidio with new information.

    Args:
        ticket_id (int): Required. The ID of the ticket to update.
        status (str, optional): The new status for the ticket.
            Must be one of: 'open', 'pending', 'solved'.
        priority (str, optional): The new priority for the ticket.
            Must be one of: 'low', 'normal', 'urgent'.
        assigned (dict, optional): Dictionary with 'type' and 'id' fields
            to assign the ticket. Example: {"type": "operator", "id": "uuid-here"}
            or {"type": "department", "id": "dept-uuid-here"}.
            'type' must be either 'operator' or 'department'.
            'id' must be a string (UUID).

    Returns:
        Dict: A dictionary with success status.

    Raises:
        ValueError: If any of the provided arguments have invalid values.
    """
    update_data = {}
    if status is not None:
        if status not in ["open", "pending", "solved"]:
            raise ValueError("Status must be one of: open, pending, solved")
        update_data["status"] = status

    if priority is not None:
        if priority not in ["low", "normal", "urgent"]:
            raise ValueError("Priority must be one of: low, normal, urgent")
        update_data["priority"] = priority

    if assigned is not None:
        if not isinstance(assigned, dict):
            raise ValueError("Assigned must be a dictionary object")

        if "type" not in assigned or "id" not in assigned:
            raise ValueError("Assigned must contain both 'type' and 'id' fields")

        if assigned["type"] not in ["operator", "department"]:
            raise ValueError("Assigned type must be either 'operator' or 'department'")

        if not isinstance(assigned["id"], str):
            raise ValueError("Assigned id must be a string")

        update_data["assigned"] = assigned

    if not update_data:
        raise ValueError(
            "At least one parameter (status, priority, or assigned) must be provided"
        )

    tidio_api_client.patch(f"/tickets/{ticket_id}", json_data=update_data)

    return _tool_call_succeed()


@mcp.tool(title="Unassign Ticket")
def unassign_ticket(ticket_id: int) -> dict:
    """
    Unassign operator from ticket in Tidio.

    Args:
        ticket_id (int): Required. The ID of the ticket to unassign.

    Returns:
        Dict: A dictionary with success status.
    """
    update_data = {"assigned": None}
    tidio_api_client.patch(f"/tickets/{ticket_id}", json_data=update_data)

    return _tool_call_succeed()


@mcp.tool(title="Reply to a Ticket")
def reply_to_a_ticket(ticket_id: int, content: str, operator_id: str) -> dict:
    """
    Send a public reply to a specific ticket in Tidio. This reply will be visible to the customer and sent to them.

    Args:
        ticket_id (int): Required. The ID of the ticket to reply to.
        content (str): Required. The content of the reply. Can be HTML.
        operator_id (str): Required. The UUID of the operator who is sending the reply.

    Returns:
        Dict: A dictionary with success status and created message ID.
    """
    if not content:
        raise ValueError("Content cannot be empty")

    if not operator_id:
        raise ValueError("Operator ID cannot be empty")

    reply_data = {
        "content": content,
        "operator_id": operator_id,
        "message_type": "public",
        "author_type": "operator",
    }

    response = tidio_api_client.post(
        f"/tickets/{ticket_id}/reply", json_data=reply_data
    )

    return _tool_call_succeed(data=response)


@mcp.tool(title="Add internal note to a Ticket")
def add_internal_note_to_a_ticket(
    ticket_id: int, content: str, operator_id: str
) -> dict:
    """
    Add an internal note to a specific ticket in Tidio. This note is only visible to operators and not sent to the customer.

    Args:
        ticket_id (int): Required. The ID of the ticket to add a note to.
        content (str): Required. The content of the internal note. Must be plain text.
        operator_id (str): Required. The UUID of the operator who is adding the note.

    Returns:
        Dict: A dictionary with success status and created message ID.

    Raises:
        ValueError: If any of the provided arguments have invalid values.
    """
    if not content:
        raise ValueError("Content cannot be empty")

    if not operator_id:
        raise ValueError("Operator ID cannot be empty")

    note_data = {
        "content": content,
        "operator_id": operator_id,
        "message_type": "internal",
        "author_type": "operator",
    }

    response = tidio_api_client.post(f"/tickets/{ticket_id}/reply", json_data=note_data)

    return _tool_call_succeed(data=response)


if __name__ == "__main__":
    mcp.run(transport="stdio")
