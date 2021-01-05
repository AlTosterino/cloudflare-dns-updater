from unittest.mock import patch

import httpx
import pytest

from cloudflare_dns_updater.queries import get_device_ip


@pytest.mark.vcr
def test_should_get_device_ip():
    # When
    result = get_device_ip()
    # Then
    assert result == "83.29.68.27"


@pytest.mark.vcr
@patch("cloudflare_dns_updater.queries.Settings")
def test_should_raise_for_status_in_get_device_ip(settings_mock):
    # Given
    settings_mock.IP_API_URL = "https://reqres.in/api/users/23"
    # Then
    with pytest.raises(httpx.HTTPStatusError):
        # When
        get_device_ip()
