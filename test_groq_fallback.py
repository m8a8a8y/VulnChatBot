import unittest
from unittest.mock import MagicMock, patch
import os
from app import create_groq_completion

class TestGroqFallback(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock()

    @patch.dict(os.environ, {}, clear=True)
    def test_fallback_on_404_success(self):
        # First model fails with 404 model_not_found error, second model succeeds
        error_response = Exception("Error code: 404 - {'error': {'message': 'The model `llama-3.3-70b-versatile` does not exist or you do not have access to it.', 'type': 'invalid_request_error', 'code': 'model_not_found'}}")

        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content="Success"))]

        self.mock_client.chat.completions.create.side_effect = [
            error_response,
            mock_completion
        ]

        res = create_groq_completion(self.mock_client, messages=[{"role": "user", "content": "hi"}])

        self.assertEqual(res.choices[0].message.content, "Success")
        self.assertEqual(self.mock_client.chat.completions.create.call_count, 2)

        # Verify call arguments
        calls = self.mock_client.chat.completions.create.call_args_list
        self.assertEqual(calls[0].kwargs["model"], "llama-3.3-70b-versatile")
        self.assertEqual(calls[1].kwargs["model"], "llama-3.1-70b-versatile")

    @patch.dict(os.environ, {"GROQ_MODEL": "custom-groq-model"})
    def test_groq_model_env_var_prioritized(self):
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content="Custom Model Success"))]
        self.mock_client.chat.completions.create.return_value = mock_completion

        res = create_groq_completion(self.mock_client, messages=[{"role": "user", "content": "hi"}])

        self.assertEqual(res.choices[0].message.content, "Custom Model Success")
        self.mock_client.chat.completions.create.assert_called_once()
        self.assertEqual(self.mock_client.chat.completions.create.call_args.kwargs["model"], "custom-groq-model")

    @patch.dict(os.environ, {}, clear=True)
    def test_other_exception_raises_immediately(self):
        auth_error = Exception("Error code: 401 - Invalid API key")
        self.mock_client.chat.completions.create.side_effect = auth_error

        with self.assertRaises(Exception) as cm:
            create_groq_completion(self.mock_client, messages=[{"role": "user", "content": "hi"}])

        self.assertIn("Invalid API key", str(cm.exception))
        self.assertEqual(self.mock_client.chat.completions.create.call_count, 1)

    @patch.dict(os.environ, {}, clear=True)
    def test_all_models_404_raises_last_exception(self):
        error_response = Exception("Error code: 404 - model_not_found")
        self.mock_client.chat.completions.create.side_effect = error_response

        with self.assertRaises(Exception) as cm:
            create_groq_completion(self.mock_client, messages=[{"role": "user", "content": "hi"}])

        self.assertIn("model_not_found", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
