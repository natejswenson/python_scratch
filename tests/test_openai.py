"""Unit tests for openAI module."""
import pytest
from unittest.mock import patch, Mock
from openAI import main


class TestOpenAIMain:
    """Tests for main function."""

    @patch('openAI.config')
    @patch('openAI.OpenAI')
    def test_main_success(self, mock_openai_class, mock_config):
        """Test successful OpenAI API call."""
        mock_config.return_value = 'test-api-key'

        # Mock OpenAI client and response
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = 'Paris'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create.return_value = mock_response

        # Call main (will print but we just test it doesn't error)
        main()

        mock_config.assert_called_once_with('open_ai_pat')
        mock_openai_class.assert_called_once_with(api_key='test-api-key')
        mock_client.chat.completions.create.assert_called_once()

    @patch('openAI.config')
    @patch('openAI.OpenAI')
    def test_main_with_different_response(self, mock_openai_class, mock_config):
        """Test OpenAI API with different response content."""
        mock_config.return_value = 'test-api-key'

        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = 'The capital of France is Paris, a beautiful city known for...'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create.return_value = mock_response

        main()

        # Verify the create method was called with correct parameters
        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs['model'] == 'gpt-3.5-turbo'
        assert len(call_args.kwargs['messages']) == 1
        assert call_args.kwargs['messages'][0]['role'] == 'user'
        assert 'France' in call_args.kwargs['messages'][0]['content']

    @patch('openAI.config')
    @patch('openAI.OpenAI')
    def test_main_api_error(self, mock_openai_class, mock_config):
        """Test OpenAI API error handling."""
        mock_config.return_value = 'test-api-key'

        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with pytest.raises(Exception):
            main()

    @patch('openAI.config')
    @patch('openAI.OpenAI')
    def test_main_invalid_api_key(self, mock_openai_class, mock_config):
        """Test with invalid API key."""
        mock_config.return_value = 'invalid-key'

        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("Invalid API key")

        with pytest.raises(Exception):
            main()
