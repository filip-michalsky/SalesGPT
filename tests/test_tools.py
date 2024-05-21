import pytest
from unittest.mock import patch, MagicMock
from salesgpt.tools import generate_stripe_payment_link, send_email_tool, generate_calendly_invitation_link
import os
import json

@pytest.fixture
def mock_requests_post():
    with patch("salesgpt.tools.requests.request") as mock_post:
        yield mock_post

@pytest.fixture
def mock_smtplib():
    with patch("salesgpt.tools.smtplib.SMTP_SSL") as mock_smtp:
        yield mock_smtp

@pytest.fixture
def mock_requests():
    with patch("salesgpt.tools.requests.post") as mock_post:
        yield mock_post

def test_generate_stripe_payment_link(mock_requests_post):
    # Mock the response of the requests.post call within your tool function
    mock_response = MagicMock()
    mock_response.text = "https://mocked_payment_link.com"
    mock_response.status_code = 200
    mock_requests_post.return_value = mock_response

    # Mock the get_product_id_from_query function to return a valid JSON string
    with patch("salesgpt.tools.get_product_id_from_query", return_value=json.dumps({"price_id": "price_123"})):
        # Call the function you're testing
        result = generate_stripe_payment_link("query about a product")

        # Assert that the result is as expected
        assert result == "https://mocked_payment_link.com", "The function should return the URL from the mocked response."

        # Additionally, you can assert that the requests.post was called with the correct arguments
        mock_requests_post.assert_called_once()

def test_send_email_tool(mock_smtplib):
    # Mock the SMTP server object and its methods
    mock_server = MagicMock()
    mock_smtplib.return_value = mock_server

    # Mock the email details extraction
    email_details = {
        "recipient": "test@example.com",
        "subject": "Test Subject",
        "body": "Test Body"
    }
    with patch("salesgpt.tools.get_mail_body_subject_from_query", return_value=json.dumps(email_details)):
        result = send_email_tool("query about sending an email")
        assert result == "Email sent successfully.", "The function should return a success message."

        mock_smtplib.assert_called_once_with('smtp.gmail.com', 465)
        mock_server.login.assert_called_once_with(os.getenv("GMAIL_MAIL"), os.getenv("GMAIL_APP_PASSWORD"))
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

def test_generate_calendly_invitation_link(mock_requests):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "resource": {
            "booking_url": "https://mocked_calendly_link.com"
        }
    }
    mock_requests.return_value = mock_response
    result = generate_calendly_invitation_link("query about a meeting")

    assert result == "url: https://mocked_calendly_link.com", "The function should return the URL from the mocked response."
    mock_requests.assert_called_once()