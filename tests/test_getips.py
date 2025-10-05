"""Unit tests for getips module."""
import pytest
import socket
from unittest.mock import patch, Mock
from getips import discover_roku_devices


class TestDiscoverRokuDevices:
    """Tests for discover_roku_devices function."""

    @patch('getips.socket.socket')
    def test_discover_single_device(self, mock_socket_class):
        """Test discovering a single Roku device."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket

        # Simulate one Roku response then timeout
        def recvfrom_side_effect(buffer_size):
            if not hasattr(recvfrom_side_effect, 'called'):
                recvfrom_side_effect.called = True
                return (b'HTTP/1.1 200 OK\r\nST: roku:ecp\r\n', ('192.168.1.100', 1900))
            raise socket.timeout()

        mock_socket.recvfrom.side_effect = recvfrom_side_effect

        result = discover_roku_devices()

        assert len(result) == 1
        assert '192.168.1.100' in result
        mock_socket.sendto.assert_called_once()
        mock_socket.close.assert_called_once()

    @patch('getips.socket.socket')
    def test_discover_multiple_devices(self, mock_socket_class):
        """Test discovering multiple Roku devices."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket

        responses = [
            (b'HTTP/1.1 200 OK\r\nST: roku:ecp\r\n', ('192.168.1.100', 1900)),
            (b'HTTP/1.1 200 OK\r\nST: roku:ecp\r\n', ('192.168.1.101', 1900)),
            (b'HTTP/1.1 200 OK\r\nST: roku:ecp\r\n', ('192.168.1.102', 1900)),
        ]

        def recvfrom_side_effect(buffer_size):
            if responses:
                return responses.pop(0)
            raise socket.timeout()

        mock_socket.recvfrom.side_effect = recvfrom_side_effect

        result = discover_roku_devices()

        assert len(result) == 3
        assert '192.168.1.100' in result
        assert '192.168.1.101' in result
        assert '192.168.1.102' in result

    @patch('getips.socket.socket')
    def test_discover_no_devices(self, mock_socket_class):
        """Test when no Roku devices are found."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recvfrom.side_effect = socket.timeout()

        result = discover_roku_devices()

        assert len(result) == 0
        assert result == []

    @patch('getips.socket.socket')
    def test_discover_non_roku_response(self, mock_socket_class):
        """Test filtering out non-Roku SSDP responses."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket

        responses = [
            (b'HTTP/1.1 200 OK\r\nST: upnp:rootdevice\r\n', ('192.168.1.100', 1900)),
            (b'HTTP/1.1 200 OK\r\nST: roku:ecp\r\n', ('192.168.1.101', 1900)),
        ]

        def recvfrom_side_effect(buffer_size):
            if responses:
                return responses.pop(0)
            raise socket.timeout()

        mock_socket.recvfrom.side_effect = recvfrom_side_effect

        result = discover_roku_devices()

        assert len(result) == 1
        assert '192.168.1.101' in result
        assert '192.168.1.100' not in result

    @patch('getips.socket.socket')
    def test_discover_duplicate_ips(self, mock_socket_class):
        """Test that duplicate IPs are filtered out."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket

        responses = [
            (b'HTTP/1.1 200 OK\r\nST: roku:ecp\r\n', ('192.168.1.100', 1900)),
            (b'HTTP/1.1 200 OK\r\nST: roku:ecp\r\n', ('192.168.1.100', 1900)),
            (b'HTTP/1.1 200 OK\r\nST: roku:ecp\r\n', ('192.168.1.101', 1900)),
        ]

        def recvfrom_side_effect(buffer_size):
            if responses:
                return responses.pop(0)
            raise socket.timeout()

        mock_socket.recvfrom.side_effect = recvfrom_side_effect

        result = discover_roku_devices()

        assert len(result) == 2
        assert '192.168.1.100' in result
        assert '192.168.1.101' in result

    @patch('getips.socket.socket')
    def test_socket_closed_on_exception(self, mock_socket_class):
        """Test that socket is closed even on exception."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.sendto.side_effect = Exception("Socket error")

        with pytest.raises(Exception):
            discover_roku_devices()

        mock_socket.close.assert_called_once()
