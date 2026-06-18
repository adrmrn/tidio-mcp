import json

import pytest
import responses

from tidio_client import TidioApiError
from tools.contacts import (
    create_contact,
    delete_contact,
    get_contact_details,
    get_contact_properties,
    get_contacts,
    update_contact,
)


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
    @pytest.mark.parametrize(
        "cursor,email,expected_endpoint",
        [
            (
                "aWRfX2U2YTgyYTc0LTExNzAtNGY1Ny1hMDMxLWIzNmYzZjZiYzA5Mw==",
                None,
                "/contacts?cursor=aWRfX2U2YTgyYTc0LTExNzAtNGY1Ny1hMDMxLWIzNmYzZjZiYzA5Mw==",
            ),
            (
                None,
                "alice@example.com",
                "/contacts?email=alice@example.com",
            ),
            (
                "aWRfX2U2YTgyYTc0LTExNzAtNGY1Ny1hMDMxLWIzNmYzZjZiYzA5Mw==",
                "alice@example.com",
                "/contacts?cursor=aWRfX2U2YTgyYTc0LTExNzAtNGY1Ny1hMDMxLWIzNmYzZjZiYzA5Mw==&email=alice@example.com",
            ),
        ],
    )
    def test_get_contacts_by_filters(
        self, cursor: str | None, email: str | None, expected_endpoint: str
    ):
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
            ],
            "meta": {
                "cursor": "next_cursor_value",
                "limit": 100,
            },
        }
        responses.add(
            responses.GET,
            f"https://api.tidio.com{expected_endpoint}",
            json=contacts_data,
            status=200,
        )

        # Act
        result = get_contacts(cursor=cursor, email=email)

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


class TestGetContactProperties:
    @pytest.mark.unit
    @responses.activate
    def test_get_contact_properties_success(self):
        # Arrange
        properties_data = {
            "properties": [
                {"name": "name", "label": "Name", "type": "text"},
                {"name": "email", "label": "Email", "type": "email"},
                {"name": "phone", "label": "Phone", "type": "phone"},
                {"name": "company_size", "label": "Company Size", "type": "number"},
                {"name": "website", "label": "Website", "type": "url"},
            ],
            "meta": {
                "cursor": None,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/contact-properties",
            json=properties_data,
            status=200,
        )

        # Act
        result = get_contact_properties()

        # Assert
        assert result == {"status": "ok", "data": properties_data}

    @pytest.mark.unit
    @responses.activate
    def test_get_contact_properties_empty_response(self):
        # Arrange
        properties_data = {
            "properties": [],
            "meta": {
                "cursor": None,
            },
        }
        responses.add(
            responses.GET,
            "https://api.tidio.com/contact-properties",
            json=properties_data,
            status=200,
        )

        # Act
        result = get_contact_properties()

        # Assert
        assert result == {"status": "ok", "data": properties_data}

    @pytest.mark.unit
    @responses.activate
    def test_get_contact_properties_with_cursor(self):
        # Arrange
        cursor = "aWRfX2U2YTgyYTc0LTExNzAtNGY1Ny1hMDMxLWIzNmYzZjZiYzA5Mw=="
        properties_data = {
            "properties": [
                {"name": "custom_field", "label": "Custom Field", "type": "text"},
            ],
            "meta": {
                "cursor": "next_cursor_value",
            },
        }
        responses.add(
            responses.GET,
            f"https://api.tidio.com/contact-properties?cursor={cursor}",
            json=properties_data,
            status=200,
        )

        # Act
        result = get_contact_properties(cursor=cursor)

        # Assert
        assert result == {"status": "ok", "data": properties_data}


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


class TestCreateContact:
    @pytest.mark.unit
    @responses.activate
    def test_create_contact_with_all_data(self):
        # Arrange
        contact_data = {"id": "535eb95e-107c-440a-8720-53649368a26a"}
        responses.add(
            responses.POST,
            "https://api.tidio.com/contacts",
            json=contact_data,
            status=201,
        )

        # Act
        result = create_contact(
            distinct_id="ext-123",
            email="john@example.com",
            phone="+1234567890",
            first_name="John",
            last_name="Doe",
            email_consent="subscribed",
            properties=[{"name": "plan", "value": "premium"}],
        )

        # Assert
        assert result == {"status": "ok", "data": contact_data}
        assert len(responses.calls) == 1
        assert json.loads(responses.calls[0].request.body) == {
            "distinct_id": "ext-123",
            "email": "john@example.com",
            "phone": "+1234567890",
            "first_name": "John",
            "last_name": "Doe",
            "email_consent": "subscribed",
            "properties": [{"name": "plan", "value": "premium"}],
        }

    @pytest.mark.unit
    @responses.activate
    def test_create_contact_with_only_required_fields(self):
        # Arrange
        contact_data = {"id": "535eb95e-107c-440a-8720-53649368a26a"}
        responses.add(
            responses.POST,
            "https://api.tidio.com/contacts",
            json=contact_data,
            status=201,
        )

        # Act
        result = create_contact(distinct_id="ext-123", email="john@example.com")

        # Assert
        assert result == {"status": "ok", "data": contact_data}
        assert json.loads(responses.calls[0].request.body) == {
            "distinct_id": "ext-123",
            "email": "john@example.com",
        }

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "kwargs,expected_error",
        [
            (
                {"distinct_id": "", "email": "a@b.com"},
                "Distinct ID must not be empty",
            ),
            (
                {"distinct_id": "x" * 56, "email": "a@b.com"},
                "Distinct ID must not exceed 55 characters",
            ),
            (
                {"distinct_id": "ext-123"},
                "At least one of email, first_name, last_name, or phone must be provided",
            ),
            (
                {
                    "distinct_id": "ext-123",
                    "email": "a@b.com",
                    "email_consent": "invalid",
                },
                "Email consent must be one of: subscribed, unsubscribed",
            ),
            (
                {
                    "distinct_id": "ext-123",
                    "email": "a@b.com",
                    "properties": "not_a_list",
                },
                "Properties must be a list of objects",
            ),
            (
                {
                    "distinct_id": "ext-123",
                    "email": "a@b.com",
                    "properties": ["not_a_dict"],
                },
                "Each property must be a dictionary object",
            ),
            (
                {
                    "distinct_id": "ext-123",
                    "email": "a@b.com",
                    "properties": [{"name": "plan"}],
                },
                "Each property must contain both 'name' and 'value' fields",
            ),
            (
                {
                    "distinct_id": "ext-123",
                    "email": "a@b.com",
                    "properties": [{"name": "x" * 129, "value": "v"}],
                },
                "Property name must not exceed 128 characters",
            ),
            (
                {
                    "distinct_id": "ext-123",
                    "email": "a@b.com",
                    "properties": [{"name": "plan", "value": "x" * 1001}],
                },
                "Property value must not exceed 1000 characters",
            ),
        ],
    )
    def test_create_contact_validation_errors(self, kwargs, expected_error):
        # Act & Assert
        with pytest.raises(ValueError, match=expected_error):
            create_contact(**kwargs)

    @pytest.mark.unit
    @pytest.mark.parametrize("email_consent", ["subscribed", "unsubscribed"])
    @responses.activate
    def test_create_contact_valid_email_consent_values(self, email_consent):
        # Arrange
        contact_data = {"id": "535eb95e-107c-440a-8720-53649368a26a"}
        responses.add(
            responses.POST,
            "https://api.tidio.com/contacts",
            json=contact_data,
            status=201,
        )

        # Act
        result = create_contact(
            distinct_id="ext-123",
            email="john@example.com",
            email_consent=email_consent,
        )

        # Assert
        assert result == {"status": "ok", "data": contact_data}
        assert (
            json.loads(responses.calls[0].request.body)["email_consent"]
            == email_consent
        )

    @pytest.mark.unit
    @responses.activate
    def test_create_contact_accepts_max_length_values(self):
        # Arrange
        contact_data = {"id": "535eb95e-107c-440a-8720-53649368a26a"}
        responses.add(
            responses.POST,
            "https://api.tidio.com/contacts",
            json=contact_data,
            status=201,
        )

        # Act
        result = create_contact(
            distinct_id="x" * 55,
            email="john@example.com",
            properties=[{"name": "x" * 128, "value": "x" * 1000}],
        )

        # Assert
        assert result == {"status": "ok", "data": contact_data}
        assert json.loads(responses.calls[0].request.body) == {
            "distinct_id": "x" * 55,
            "email": "john@example.com",
            "properties": [{"name": "x" * 128, "value": "x" * 1000}],
        }

    @pytest.mark.unit
    @responses.activate
    def test_create_contact_omits_none_fields(self):
        # Arrange
        contact_data = {"id": "535eb95e-107c-440a-8720-53649368a26a"}
        responses.add(
            responses.POST,
            "https://api.tidio.com/contacts",
            json=contact_data,
            status=201,
        )

        # Act
        create_contact(distinct_id="ext-123", email="a@b.com", phone=None)

        # Assert
        assert json.loads(responses.calls[0].request.body) == {
            "distinct_id": "ext-123",
            "email": "a@b.com",
        }

    @pytest.mark.unit
    @pytest.mark.parametrize("field", ["phone", "first_name", "last_name"])
    @responses.activate
    def test_create_contact_accepts_single_identity_field(self, field):
        # Arrange
        contact_data = {"id": "535eb95e-107c-440a-8720-53649368a26a"}
        responses.add(
            responses.POST,
            "https://api.tidio.com/contacts",
            json=contact_data,
            status=201,
        )

        # Act
        create_contact(distinct_id="ext-123", **{field: "value"})

        # Assert
        assert json.loads(responses.calls[0].request.body) == {
            "distinct_id": "ext-123",
            field: "value",
        }

    @pytest.mark.unit
    @responses.activate
    def test_create_contact_accepts_numeric_property_value(self):
        # Arrange
        contact_data = {"id": "535eb95e-107c-440a-8720-53649368a26a"}
        responses.add(
            responses.POST,
            "https://api.tidio.com/contacts",
            json=contact_data,
            status=201,
        )

        # Act
        create_contact(
            distinct_id="ext-123",
            email="a@b.com",
            properties=[{"name": "score", "value": 42}],
        )

        # Assert
        body = json.loads(responses.calls[0].request.body)
        assert body["properties"] == [{"name": "score", "value": 42}]

    @pytest.mark.unit
    @responses.activate
    def test_create_contact_propagates_api_error(self):
        # Arrange
        responses.add(
            responses.POST,
            "https://api.tidio.com/contacts",
            status=422,
        )

        # Act & Assert
        with pytest.raises(TidioApiError):
            create_contact(distinct_id="ext-123", email="a@b.com")


class TestUpdateContact:
    @pytest.mark.unit
    @responses.activate
    def test_update_contact_with_all_data(self):
        # Arrange
        contact_id = "535eb95e-107c-440a-8720-53649368a26a"
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=204,
        )

        # Act
        result = update_contact(
            contact_id=contact_id,
            email="john@example.com",
            phone="+1234567890",
            first_name="John",
            last_name="Doe",
            email_consent="subscribed",
            distinct_id="ext-123",
            properties=[{"name": "plan", "value": "premium"}],
        )

        # Assert
        assert result == {"status": "ok", "data": {}}
        assert len(responses.calls) == 1
        assert json.loads(responses.calls[0].request.body) == {
            "email": "john@example.com",
            "phone": "+1234567890",
            "first_name": "John",
            "last_name": "Doe",
            "email_consent": "subscribed",
            "distinct_id": "ext-123",
            "properties": [{"name": "plan", "value": "premium"}],
        }

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "kwargs,expected_error",
        [
            (
                {"contact_id": ""},
                "Contact ID must not be empty",
            ),
            (
                {"contact_id": "   "},
                "Contact ID must not be empty",
            ),
            (
                {"contact_id": "uuid", "email_consent": "invalid"},
                "Email consent must be one of: subscribed, unsubscribed",
            ),
            (
                {"contact_id": "uuid", "distinct_id": "x" * 56},
                "Distinct ID must not exceed 55 characters",
            ),
            (
                {"contact_id": "uuid", "distinct_id": None},
                "Distinct ID must not be empty",
            ),
            (
                {"contact_id": "uuid", "email": "a@b.com", "properties": "not_a_list"},
                "Properties must be a list of objects",
            ),
            (
                {
                    "contact_id": "uuid",
                    "email": "a@b.com",
                    "properties": ["not_a_dict"],
                },
                "Each property must be a dictionary object",
            ),
            (
                {
                    "contact_id": "uuid",
                    "email": "a@b.com",
                    "properties": [{"name": "plan"}],
                },
                "Each property must contain both 'name' and 'value' fields",
            ),
            (
                {
                    "contact_id": "uuid",
                    "email": "a@b.com",
                    "properties": [{"name": "x" * 129, "value": "v"}],
                },
                "Property name must not exceed 128 characters",
            ),
            (
                {
                    "contact_id": "uuid",
                    "email": "a@b.com",
                    "properties": [{"name": "plan", "value": "x" * 1001}],
                },
                "Property value must not exceed 1000 characters",
            ),
            (
                {"contact_id": "uuid"},
                "At least one parameter must be provided",
            ),
        ],
    )
    def test_update_contact_validation_errors(self, kwargs, expected_error):
        # Act & Assert
        with pytest.raises(ValueError, match=expected_error):
            update_contact(**kwargs)

    @pytest.mark.unit
    @pytest.mark.parametrize("email_consent", ["subscribed", "unsubscribed"])
    @responses.activate
    def test_update_contact_valid_email_consent_values(self, email_consent):
        # Arrange
        contact_id = "535eb95e-107c-440a-8720-53649368a26a"
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=204,
        )

        # Act
        result = update_contact(contact_id=contact_id, email_consent=email_consent)

        # Assert
        assert result == {"status": "ok", "data": {}}
        assert json.loads(responses.calls[0].request.body) == {
            "email_consent": email_consent
        }

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "kwargs,expected_payload",
        [
            (
                {"contact_id": "uuid", "email": None},
                {"email": None},
            ),
            (
                {"contact_id": "uuid", "phone": None},
                {"phone": None},
            ),
            (
                {"contact_id": "uuid", "first_name": None},
                {"first_name": None},
            ),
            (
                {"contact_id": "uuid", "last_name": None},
                {"last_name": None},
            ),
            (
                {"contact_id": "uuid", "email_consent": None},
                {"email_consent": None},
            ),
            (
                {"contact_id": "uuid", "properties": None},
                {"properties": None},
            ),
        ],
    )
    @responses.activate
    def test_update_contact_null_clears_field(self, kwargs, expected_payload):
        contact_id = kwargs["contact_id"]
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=204,
        )

        result = update_contact(**kwargs)

        assert result == {"status": "ok", "data": {}}
        assert json.loads(responses.calls[0].request.body) == expected_payload

    @pytest.mark.unit
    @responses.activate
    def test_update_contact_omitted_field_not_in_payload(self):
        contact_id = "535eb95e-107c-440a-8720-53649368a26a"
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=204,
        )

        update_contact(contact_id=contact_id, first_name="John")

        payload = json.loads(responses.calls[0].request.body)
        assert "email" not in payload
        assert "phone" not in payload
        assert payload == {"first_name": "John"}

    @pytest.mark.unit
    @responses.activate
    def test_update_contact_distinct_id_only(self):
        contact_id = "535eb95e-107c-440a-8720-53649368a26a"
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=204,
        )

        result = update_contact(contact_id=contact_id, distinct_id="ext-456")

        assert result == {"status": "ok", "data": {}}
        assert json.loads(responses.calls[0].request.body) == {"distinct_id": "ext-456"}

    @pytest.mark.unit
    @responses.activate
    def test_update_contact_accepts_max_length_values(self):
        contact_id = "535eb95e-107c-440a-8720-53649368a26a"
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=204,
        )

        result = update_contact(
            contact_id=contact_id,
            distinct_id="x" * 55,
            email="john@example.com",
            properties=[{"name": "x" * 128, "value": "x" * 1000}],
        )

        assert result == {"status": "ok", "data": {}}
        assert json.loads(responses.calls[0].request.body) == {
            "distinct_id": "x" * 55,
            "email": "john@example.com",
            "properties": [{"name": "x" * 128, "value": "x" * 1000}],
        }

    @pytest.mark.unit
    @responses.activate
    def test_update_contact_mixes_set_and_clear(self):
        contact_id = "535eb95e-107c-440a-8720-53649368a26a"
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=204,
        )

        update_contact(contact_id=contact_id, email="new@x.com", phone=None)

        assert json.loads(responses.calls[0].request.body) == {
            "email": "new@x.com",
            "phone": None,
        }

    @pytest.mark.unit
    @responses.activate
    def test_update_contact_sends_empty_properties_list(self):
        contact_id = "535eb95e-107c-440a-8720-53649368a26a"
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=204,
        )

        update_contact(contact_id=contact_id, properties=[])

        assert json.loads(responses.calls[0].request.body) == {"properties": []}

    @pytest.mark.unit
    @responses.activate
    def test_update_contact_propagates_api_error(self):
        contact_id = "535eb95e-107c-440a-8720-53649368a26a"
        responses.add(
            responses.PATCH,
            f"https://api.tidio.com/contacts/{contact_id}",
            status=422,
        )

        with pytest.raises(TidioApiError):
            update_contact(contact_id=contact_id, email="a@b.com")
