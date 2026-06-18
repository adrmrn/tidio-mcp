from urllib.parse import urlencode

from core import _tool_call_succeed, mcp, tidio_api_client


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
