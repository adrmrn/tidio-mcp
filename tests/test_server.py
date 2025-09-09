import json

import pytest
import responses

from server import (
    add_internal_note_to_a_ticket,
    create_ticket,
    delete_contact,
    delete_ticket,
    get_contact_details,
    get_contacts,
    get_departments,
    get_operators,
    get_ticket_details,
    get_tickets,
    reply_to_a_ticket,
    unassign_ticket,
    update_ticket,
)


class TestGetDepartments:
    @pytest.mark.unit
    @responses.activate
    def test_get_departments_success(self):
        # Arrange
        departments_data = {
            "departments": [
                {"id": "535eb95e-107c-440a-8720-53649368a26a", "name": "Finances"},
                {"id": "7f14e5f9-1df0-439d-9b39-bd7e1e82fac5", "name": "Sales"},
            ]
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/departments",
            json=departments_data,
            status=200,
        )

        # Act
        result = get_departments()

        # Assert
        assert result == {"status": "ok", "data": departments_data}

    @pytest.mark.unit
    @responses.activate
    def test_get_departments_empty_response(self):
        # Arrange
        departments_data = {"departments": []}
        responses.add(
            responses.GET,
            "https://api.tidio.com/departments",
            json=departments_data,
            status=200,
        )

        # Act
        result = get_departments()

        # Assert
        assert result == {"status": "ok", "data": departments_data}


class TestGetOperators:
    @pytest.mark.unit
    @responses.activate
    def test_get_operators_success(self):
        # Arrange
        operators_data = {
            "operators": [
                {
                    "id": "fe7df646-6881-4d44-bcd5-639501a32bfe",
                    "active": True,
                    "email": "john.smith@company.com",
                    "name": "John Smith",
                    "role": "owner",
                    "picture": "https://example.com/avatars/john.jpg",
                    "last_seen": "2025-09-06T14:29:31+00:00",
                },
                {
                    "id": "dc017931-764b-4921-a8d6-bd967e91c955",
                    "active": False,
                    "email": "jane.doe@company.com",
                    "name": None,
                    "role": "chat_agent",
                    "picture": None,
                    "last_seen": None,
                },
            ],
            "meta": {
                "cursor": None,
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/operators",
            json=operators_data,
            status=200,
        )

        # Act
        result = get_operators()

        # Assert
        assert result == {"status": "ok", "data": operators_data}

    @pytest.mark.unit
    @responses.activate
    def test_get_operators_empty_response(self):
        # Arrange
        operators_data = {
            "operators": [],
            "meta": {
                "cursor": None,
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/operators",
            json=operators_data,
            status=200,
        )

        # Act
        result = get_operators()

        # Assert
        assert result == {"status": "ok", "data": operators_data}


class TestGetContacts:
    @pytest.mark.unit
    @responses.activate
    def test_get_contacts_success(self):
        # Arrange
        contacts_data = {
            "contacts": [
                {
                    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                    "distinct_id": "ext_123456",
                    "first_name": "Alice",
                    "last_name": "Johnson",
                    "email": "alice@example.com",
                    "phone": "+1234567890",
                    "language": "en",
                    "country": "US",
                    "city": "New York",
                    "messenger_id": None,
                    "instagram_id": None,
                    "created_at": "2025-09-06T10:30:00+00:00",
                    "email_consent": "subscribed",
                    "properties": [{"name": "company", "value": "Acme Corp"}],
                },
                {
                    "id": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
                    "distinct_id": None,
                    "first_name": None,
                    "last_name": None,
                    "email": "bob@example.com",
                    "phone": None,
                    "language": None,
                    "country": None,
                    "city": None,
                    "messenger_id": None,
                    "instagram_id": None,
                    "created_at": "2025-09-05T09:20:00+00:00",
                    "email_consent": "unsubscribed",
                    "properties": [],
                },
            ],
            "meta": {
                "cursor": None,
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/contacts",
            json=contacts_data,
            status=200,
        )

        # Act
        result = get_contacts()

        # Assert
        assert result == {"status": "ok", "data": contacts_data}

    @pytest.mark.unit
    @responses.activate
    def test_get_contacts_empty_response(self):
        # Arrange
        contacts_data = {
            "contacts": [],
            "meta": {
                "cursor": None,
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/contacts",
            json=contacts_data,
            status=200,
        )

        # Act
        result = get_contacts()

        # Assert
        assert result == {"status": "ok", "data": contacts_data}


class TestGetContactDetails:
    @pytest.mark.unit
    @responses.activate
    def test_get_contact_details_success(self):
        # Arrange
        contact_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        contact_data = {
            "id": contact_id,
            "distinct_id": "ext_123456",
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice@example.com",
            "phone": "+1234567890",
            "language": "en",
            "country": "US",
            "city": "New York",
            "messenger_id": None,
            "instagram_id": None,
            "created_at": "2025-09-06T10:30:00+00:00",
            "email_consent": "subscribed",
            "properties": [{"name": "company", "value": "Acme Corp"}],
        }
        responses.add(
            responses.GET,
            f"https://api.tidio.com/contacts/{contact_id}",
            json=contact_data,
            status=200,
        )

        # Act
        result = get_contact_details(contact_id)

        # Assert
        assert result == {"status": "ok", "data": contact_data}


class TestDeleteContact:
    @pytest.mark.unit
    @responses.activate
    def test_delete_contact_success(self):
        # Arrange
        contact_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        responses.add(
            responses.DELETE,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=204,
        )

        # Act
        result = delete_contact(contact_id)

        # Assert
        assert result == {"status": "ok", "data": {}}


class TestGetTickets:
    @pytest.mark.unit
    @responses.activate
    def test_get_tickets_success(self):
        # Arrange
        tickets_data = {
            "tickets": [
                {
                    "id": 10009,
                    "link": "https://www.tidio.com/panel/inbox/tickets/10009",
                    "subject": "Unable to process payment",
                    "contact_id": "27206142-57a3-40c0-8c76-707cdf05cd32",
                    "contact_email": "customer@example.com",
                    "priority": "urgent",
                    "status": "open",
                    "assigned_operator_id": "fe7df646-6881-4d44-bcd5-639501a32bfe",
                    "assigned_department_id": "535eb95e-107c-440a-8720-53649368a26a",
                },
                {
                    "id": 10007,
                    "link": "https://www.tidio.com/panel/inbox/tickets/10007",
                    "subject": "Account login issues",
                    "contact_id": "d4b50687-51be-476d-8624-7344d6734156",
                    "contact_email": "user@example.com",
                    "priority": "normal",
                    "status": "pending",
                    "assigned_operator_id": None,
                    "assigned_department_id": "436401bc-7477-458e-98a9-c39ca80940bc",
                },
            ],
            "meta": {
                "cursor": None,
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/tickets",
            json=tickets_data,
            status=200,
        )

        # Act
        result = get_tickets()

        # Assert
        assert result == {"status": "ok", "data": tickets_data}

    @pytest.mark.unit
    @responses.activate
    def test_get_tickets_empty_response(self):
        # Arrange
        tickets_data = {
            "tickets": [],
            "meta": {
                "cursor": None,
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/tickets",
            json=tickets_data,
            status=200,
        )

        # Act
        result = get_tickets()

        # Assert
        assert result == {"status": "ok", "data": tickets_data}


class TestGetTicketDetails:
    @pytest.mark.unit
    @responses.activate
    def test_get_ticket_details_success(self):
        # Arrange
        ticket_id = 10009
        ticket_data = {
            "id": ticket_id,
            "link": "https://www.tidio.com/panel/inbox/tickets/10009",
            "subject": "Unable to process payment",
            "contact_id": "27206142-57a3-40c0-8c76-707cdf05cd32",
            "contact_email": "customer@example.com",
            "priority": "urgent",
            "status": "open",
            "assigned_operator_id": "fe7df646-6881-4d44-bcd5-639501a32bfe",
            "assigned_department_id": "535eb95e-107c-440a-8720-53649368a26a",
            "messages": [
                {
                    "message_id": "01K4JT3B8KST23PAS1H20AF2HR",
                    "created_at": "2025-09-07T10:30:00+00:00",
                    "author_type": "contact",
                    "author_id": "3b367d4a-c31a-435b-be08-8d3a1ed0a857",
                    "message_type": "public",
                    "message_content": "Dear support team, ...",
                    "attachments": [],
                },
                {
                    "message_id": "01K4JT3E7J62VQQX23WVSDXZB1",
                    "created_at": "2025-09-07T11:15:00+00:00",
                    "author_type": "operator",
                    "author_id": "dc8e09de-95b5-4aba-b6d6-320b323fe34b",
                    "message_type": "internal",
                    "message_content": "Checked the payment gateway, ...",
                    "attachments": [],
                },
                {
                    "message_id": "01K4JT3E7J62VQQX23WVSDXZB1",
                    "created_at": "2025-09-07T11:25:00+00:00",
                    "author_type": "operator",
                    "author_id": "dc8e09de-95b5-4aba-b6d6-320b323fe34b",
                    "message_type": "public",
                    "message_content": "Dear customer, ...",
                    "attachments": [
                        "https://example.com/attachments/invoice.pdf",
                    ],
                },
            ],
        }
        responses.add(
            responses.GET,
            f"https://api.tidio.com/tickets/{ticket_id}",
            json=ticket_data,
            status=200,
        )

        # Act
        result = get_ticket_details(ticket_id)

        # Assert
        assert result == {"status": "ok", "data": ticket_data}


class TestDeleteTicket:
    @pytest.mark.unit
    @responses.activate
    def test_delete_ticket_success(self):
        # Arrange
        ticket_id = 10009
        responses.add(
            responses.DELETE,
            f"https://api.tidio.com/tickets/{ticket_id}",
            status=204,
        )

        # Act
        result = delete_ticket(ticket_id)

        # Assert
        assert result == {"status": "ok", "data": {}}


class TestCreateTicket:
    @pytest.mark.unit
    @responses.activate
    def test_create_ticket_minimal_data(self):
        # Arrange
        contact_email = "customer@example.com"
        subject = "Test ticket subject"
        message_content = "This is a test ticket message"

        ticket_response = {"id": 10010}
        responses.add(
            responses.POST,
            "https://api.tidio.com/tickets/as-contact",
            json=ticket_response,
            status=201,
        )

        # Act
        result = create_ticket(
            contact_email,
            subject,
            message_content,
        )

        # Assert
        assert result == {"status": "ok", "data": ticket_response}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == {
            "contact_email": contact_email,
            "subject": subject,
            "message_content": message_content,
        }

    @pytest.mark.unit
    @responses.activate
    def test_create_ticket_with_all_data(self):
        # Arrange
        contact_email = "customer@example.com"
        subject = "Test ticket with department"
        message_content = "This is a test ticket with department assignment"
        department_id = "535eb95e-107c-440a-8720-53649368a26a"

        ticket_response = {"id": 10011}
        responses.add(
            responses.POST,
            "https://api.tidio.com/tickets/as-contact",
            json=ticket_response,
            status=201,
        )

        # Act
        result = create_ticket(
            contact_email,
            subject,
            message_content,
            department_id,
        )

        # Assert
        assert result == {"status": "ok", "data": ticket_response}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == {
            "contact_email": contact_email,
            "subject": subject,
            "message_content": message_content,
            "assigned_department_id": department_id,
        }


class TestUpdateTicket:
    @pytest.mark.unit
    @responses.activate
    def test_update_ticket_with_all_data(self):
        # Arrange
        ticket_id = 10009
        status = "pending"
        priority = "urgent"
        assigned = {"type": "operator", "id": "fe7df646-6881-4d44-bcd5-639501a32bfe"}

        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/tickets/{ticket_id}",
            status=204,
        )

        # Act
        result = update_ticket(ticket_id, status, priority, assigned)

        # Assert
        assert result == {"status": "ok", "data": {}}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == {
            "status": status,
            "priority": priority,
            "assigned": assigned,
        }

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "update_data,expected_error",
        [
            ({"status": "invalid"}, "Status must be one of: open, pending, solved"),
            ({"priority": "invalid"}, "Priority must be one of: low, normal, urgent"),
            ({"assigned": "not_a_dict"}, "Assigned must be a dictionary object"),
            ({"assigned": {}}, "Assigned must contain both 'type' and 'id' fields"),
            (
                {"assigned": {"type": "operator"}},
                "Assigned must contain both 'type' and 'id' fields",
            ),
            (
                {"assigned": {"id": "123"}},
                "Assigned must contain both 'type' and 'id' fields",
            ),
            (
                {
                    "assigned": {
                        "type": "invalid",
                        "id": "36fe7ec4-0d3c-43ae-ad1a-d38ffbf8ef57",
                    }
                },
                "Assigned type must be either 'operator' or 'department'",
            ),
            (
                {"assigned": {"type": "operator", "id": 123}},
                "Assigned id must be a string",
            ),
        ],
    )
    def test_update_ticket_validation_errors(self, update_data, expected_error):
        # Arrange
        ticket_id = 10009

        # Act & Assert
        with pytest.raises(ValueError, match=expected_error):
            update_ticket(ticket_id, **update_data)

    @pytest.mark.unit
    @pytest.mark.parametrize("status", ["open", "pending", "solved"])
    @responses.activate
    def test_update_ticket_valid_status_values(self, status):
        # Arrange
        ticket_id = 10009
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/tickets/{ticket_id}",
            status=204,
        )

        # Act
        result = update_ticket(ticket_id, status=status)

        # Assert
        assert result == {"status": "ok", "data": {}}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == {"status": status}

    @pytest.mark.unit
    @pytest.mark.parametrize("priority", ["low", "normal", "urgent"])
    @responses.activate
    def test_update_ticket_valid_priority_values(self, priority):
        # Arrange
        ticket_id = 10009
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/tickets/{ticket_id}",
            status=204,
        )

        # Act
        result = update_ticket(ticket_id, priority=priority)

        # Assert
        assert result == {"status": "ok", "data": {}}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == {"priority": priority}

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "assigned",
        [
            {"type": "operator", "id": "fe7df646-6881-4d44-bcd5-639501a32bfe"},
            {"type": "department", "id": "535eb95e-107c-440a-8720-53649368a26a"},
        ],
    )
    @responses.activate
    def test_update_ticket_valid_assigned_values(self, assigned):
        # Arrange
        ticket_id = 10009
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/tickets/{ticket_id}",
            status=204,
        )

        # Act
        result = update_ticket(ticket_id, assigned=assigned)

        # Assert
        assert result == {"status": "ok", "data": {}}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == {"assigned": assigned}

    @pytest.mark.unit
    def test_update_ticket_no_parameters_error(self):
        # Arrange
        ticket_id = 10009

        # Act & Assert
        with pytest.raises(
            ValueError,
            match="At least one parameter \\(status, priority, or assigned\\) must be provided",
        ):
            update_ticket(ticket_id)


class TestUnassignTicket:
    @pytest.mark.unit
    @responses.activate
    def test_unassign_ticket_success(self):
        # Arrange
        ticket_id = 10009
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/tickets/{ticket_id}",
            status=204,
        )

        # Act
        result = unassign_ticket(ticket_id)

        # Assert
        assert result == {"status": "ok", "data": {}}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == {"assigned": None}


class TestReplyToATicket:
    @pytest.mark.unit
    @responses.activate
    def test_reply_to_a_ticket_success(self):
        # Arrange
        ticket_id = 10009
        content = "Thank you for contacting us. We'll look into this issue right away."
        operator_id = "fe7df646-6881-4d44-bcd5-639501a32bfe"

        reply_response = {"id": "01K4JT3B8KST23PAS1H20AF2HR"}
        responses.add(
            responses.POST,
            f"https://api.tidio.com/tickets/{ticket_id}/reply",
            json=reply_response,
            status=201,
        )

        # Act
        result = reply_to_a_ticket(ticket_id, content, operator_id)

        # Assert
        assert result == {"status": "ok", "data": reply_response}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == {
            "content": content,
            "operator_id": operator_id,
            "message_type": "public",
            "author_type": "operator",
        }

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "content,operator_id,expected_error",
        [
            ("", "fe7df646-6881-4d44-bcd5-639501a32bfe", "Content cannot be empty"),
            (None, "fe7df646-6881-4d44-bcd5-639501a32bfe", "Content cannot be empty"),
            ("Valid content", "", "Operator ID cannot be empty"),
            ("Valid content", None, "Operator ID cannot be empty"),
        ],
    )
    def test_reply_to_a_ticket_validation_errors(
        self, content, operator_id, expected_error
    ):
        # Arrange
        ticket_id = 10009

        # Act & Assert
        with pytest.raises(ValueError, match=expected_error):
            reply_to_a_ticket(ticket_id, content, operator_id)


class TestAddInternalNoteToATicket:
    @pytest.mark.unit
    @responses.activate
    def test_add_internal_note_to_a_ticket_success(self):
        # Arrange
        ticket_id = 10009
        content = "Internal note: Customer has been escalated to priority support."
        operator_id = "fe7df646-6881-4d44-bcd5-639501a32bfe"

        note_response = {"id": "01K4JT3C9LST23PAS1H20AF2HR"}
        responses.add(
            responses.POST,
            f"https://api.tidio.com/tickets/{ticket_id}/reply",
            json=note_response,
            status=201,
        )

        # Act
        result = add_internal_note_to_a_ticket(ticket_id, content, operator_id)

        # Assert
        assert result == {"status": "ok", "data": note_response}
        assert len(responses.calls) == 1

        request = responses.calls[0].request
        assert json.loads(request.body) == {
            "content": content,
            "operator_id": operator_id,
            "message_type": "internal",
            "author_type": "operator",
        }

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "content,operator_id,expected_error",
        [
            ("", "fe7df646-6881-4d44-bcd5-639501a32bfe", "Content cannot be empty"),
            (None, "fe7df646-6881-4d44-bcd5-639501a32bfe", "Content cannot be empty"),
            ("Valid content", "", "Operator ID cannot be empty"),
            ("Valid content", None, "Operator ID cannot be empty"),
        ],
    )
    def test_add_internal_note_to_a_ticket_validation_errors(
        self, content, operator_id, expected_error
    ):
        # Arrange
        ticket_id = 10009

        # Act & Assert
        with pytest.raises(ValueError, match=expected_error):
            add_internal_note_to_a_ticket(ticket_id, content, operator_id)
