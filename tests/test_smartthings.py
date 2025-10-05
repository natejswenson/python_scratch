"""Unit tests for smartthings module."""
import pytest
from unittest.mock import patch, Mock, AsyncMock
from smartthings import list_devices


class TestListDevices:
    """Tests for list_devices function."""

    @pytest.mark.asyncio
    @patch('smartthings.aiohttp.ClientSession')
    @patch('smartthings.pysmartthings.SmartThings')
    async def test_list_devices_success(self, mock_smartthings, mock_session):
        """Test successful device listing."""
        # Mock devices
        mock_device1 = Mock()
        mock_device1.name = 'Living Room Light'
        mock_device1.device_id = 'device-123'
        mock_device1.capabilities = ['switch', 'level']

        mock_device2 = Mock()
        mock_device2.name = 'Bedroom Thermostat'
        mock_device2.device_id = 'device-456'
        mock_device2.capabilities = ['temperature', 'thermostat']

        # Mock API
        mock_api = AsyncMock()
        mock_api.devices.return_value = [mock_device1, mock_device2]
        mock_smartthings.return_value = mock_api

        result = await list_devices()

        assert len(result) == 2
        assert result[0].name == 'Living Room Light'
        assert result[1].name == 'Bedroom Thermostat'
        mock_api.devices.assert_called_once()

    @pytest.mark.asyncio
    @patch('smartthings.aiohttp.ClientSession')
    @patch('smartthings.pysmartthings.SmartThings')
    async def test_list_devices_empty(self, mock_smartthings, mock_session):
        """Test when no devices are found."""
        mock_api = AsyncMock()
        mock_api.devices.return_value = []
        mock_smartthings.return_value = mock_api

        result = await list_devices()

        assert len(result) == 0
        assert result == []

    @pytest.mark.asyncio
    @patch('smartthings.aiohttp.ClientSession')
    @patch('smartthings.pysmartthings.SmartThings')
    async def test_list_devices_single_device(self, mock_smartthings, mock_session):
        """Test listing a single device."""
        mock_device = Mock()
        mock_device.name = 'Kitchen Switch'
        mock_device.device_id = 'device-789'
        mock_device.capabilities = ['switch']

        mock_api = AsyncMock()
        mock_api.devices.return_value = [mock_device]
        mock_smartthings.return_value = mock_api

        result = await list_devices()

        assert len(result) == 1
        assert result[0].name == 'Kitchen Switch'
        assert result[0].device_id == 'device-789'

    @pytest.mark.asyncio
    @patch('smartthings.aiohttp.ClientSession')
    @patch('smartthings.pysmartthings.SmartThings')
    async def test_list_devices_complex_capabilities(self, mock_smartthings, mock_session):
        """Test device with multiple capabilities."""
        mock_device = Mock()
        mock_device.name = 'Smart Sensor'
        mock_device.device_id = 'device-999'
        mock_device.capabilities = [
            'motion', 'temperature', 'humidity', 'battery', 'refresh'
        ]

        mock_api = AsyncMock()
        mock_api.devices.return_value = [mock_device]
        mock_smartthings.return_value = mock_api

        result = await list_devices()

        assert len(result) == 1
        assert len(result[0].capabilities) == 5
        assert 'motion' in result[0].capabilities
        assert 'battery' in result[0].capabilities
