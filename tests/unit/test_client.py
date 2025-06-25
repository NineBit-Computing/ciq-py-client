import pytest
from unittest.mock import Mock, patch
from ninebit_ciq.client import NineBitCIQClient
import requests  # noqa: F403 F401
import time  # noqa: F403 F401


# ─────────────────────────────────────────────────────────────
def test_client_instantiation():
    client = NineBitCIQClient("https://example.com", "fake-token")
    assert client.base_url == "https://example.com"


# ─────────────────────────────────────────────────────────────
@patch("ninebit_ciq.client.requests.Session.get")
@pytest.mark.skip(reason="Temporarily disabled for debugging")
def test_get_status_success(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {"status": "ok"}
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    client = NineBitCIQClient("http://fake-url", "fake-key")
    result = client.get_status()

    assert result == {"status": "ok"}
    mock_get.assert_called_once_with("http://fake-url/status")


# ─────────────────────────────────────────────────────────────
@patch("ninebit_ciq.client.requests.Session.get")
def test_get_design_time_workflow_success(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {"content": {"workflow": "abc"}}
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    client = NineBitCIQClient("http://fake-url", "fake-key")
    result = client.get_design_time_workflow()

    assert "content" in result
    mock_get.assert_called_once()


# ─────────────────────────────────────────────────────────────
@patch("ninebit_ciq.client.requests.Session.post")
def test_trigger_workflow_success(mock_post):
    mock_resp = Mock()
    mock_resp.json.return_value = {"wf_id": "1234"}
    mock_resp.raise_for_status = Mock()
    mock_post.return_value = mock_resp

    client = NineBitCIQClient("http://fake-url", "fake-key")
    result = client.trigger_workflow({"input": "data"})

    assert result == "1234"
    mock_post.assert_called_once()


# ─────────────────────────────────────────────────────────────
@patch("ninebit_ciq.client.requests.Session.get")
def test_get_workflow_status_success(mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {"status": "completed", "result": {"output": "done"}}
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    client = NineBitCIQClient("http://fake-url", "fake-key")
    result = client.get_workflow_status("1234")

    assert result["status"] == "completed"
    assert "result" in result
    mock_get.assert_called_once()


# ─────────────────────────────────────────────────────────────
@patch("time.sleep", return_value=None)  # Skip real sleep
@patch("ninebit_ciq.client.requests.Session.get")
def test_wait_for_completion_retries_until_done(mock_get, _):
    # Simulate two in-progress responses, then a completed one
    in_progress = Mock()
    in_progress.json.return_value = {"status": "running"}
    in_progress.raise_for_status = Mock()

    done = Mock()
    done.json.return_value = {"status": "completed", "result": {"output": "final"}}
    done.raise_for_status = Mock()

    mock_get.side_effect = [in_progress, in_progress, done]

    client = NineBitCIQClient("http://fake-url", "fake-key")
    result = client.wait_for_completion("1234", interval=1)

    assert result["status"] == "completed"
    assert result["result"]["output"] == "final"
    assert mock_get.call_count == 3
