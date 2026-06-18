import asyncio

import pytest

import server

EXPECTED_TOOL_NAMES = {
    "get_departments",
    "get_operators",
    "get_contacts",
    "get_contact_details",
    "create_contact",
    "update_contact",
    "delete_contact",
    "get_contact_properties",
    "get_tickets",
    "get_ticket_details",
    "delete_ticket",
    "create_ticket",
    "update_ticket",
    "unassign_ticket",
    "reply_to_a_ticket",
    "add_internal_note_to_a_ticket",
}


class TestServerWiring:
    @pytest.mark.unit
    def test_server_exposes_all_expected_tools(self):
        registered = {tool.name for tool in asyncio.run(server.mcp.list_tools())}

        assert registered == EXPECTED_TOOL_NAMES
