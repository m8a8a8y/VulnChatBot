import unittest
from unittest.mock import MagicMock
import os

from app import create_chat_completion_with_fallback, ask_ai_api, ask_ai_deep_search

class TestGroqFallback(unittest.TestCase):
    def test_fallback_on_404_not_found(self):
        mock_client = MagicMock()

        # Simulate 404 for first model, success for second
        def side_effect(**kwargs):
            if kwargs.get('model') == 'llama-3.3-70b-versatile':
                raise Exception("Error code: 404 - {'error': {'message': 'The model `llama-3.3-70b-versatile` does not exist or you do not have access to it.', 'type': 'invalid_request_error', 'code': 'model_not_found'}}")
            mock_resp = MagicMock()
            mock_resp.choices = [MagicMock()]
            mock_resp.choices[0].message.content = "Success response"
            return mock_resp

        mock_client.chat.completions.create.side_effect = side_effect

        result = create_chat_completion_with_fallback(mock_client, messages=[{"role": "user", "content": "hello"}])
        self.assertEqual(result.choices[0].message.content, "Success response")

        # Verify call count and model parameters attempted
        calls = mock_client.chat.completions.create.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].kwargs['model'], 'llama-3.3-70b-versatile')
        self.assertEqual(calls[1].kwargs['model'], 'llama-3.1-70b-versatile')

    def test_custom_groq_model_env_var(self):
        os.environ['GROQ_MODEL'] = 'custom-model-x'
        try:
            mock_client = MagicMock()
            mock_resp = MagicMock()
            mock_resp.choices = [MagicMock()]
            mock_resp.choices[0].message.content = "Custom model response"
            mock_client.chat.completions.create.return_value = mock_resp

            result = create_chat_completion_with_fallback(mock_client, messages=[{"role": "user", "content": "hello"}])
            self.assertEqual(result.choices[0].message.content, "Custom model response")
            calls = mock_client.chat.completions.create.call_args_list
            self.assertEqual(calls[0].kwargs['model'], 'custom-model-x')
        finally:
            os.environ.pop('GROQ_MODEL', None)

    def test_non_404_error_raises_immediately(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = ValueError("Authentication Error")

        with self.assertRaises(ValueError):
            create_chat_completion_with_fallback(mock_client, messages=[{"role": "user", "content": "hello"}])
        self.assertEqual(mock_client.chat.completions.create.call_count, 1)

if __name__ == '__main__':
    unittest.main()
