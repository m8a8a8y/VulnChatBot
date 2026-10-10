import os
import unittest
from unittest.mock import MagicMock, patch
import json

import app


class TestAppGroqIntegration(unittest.TestCase):

    def setUp(self):
        self.app_client = app.app.test_client()

    @patch('app.client')
    def test_ask_ai_api_uses_env_model(self, mock_groq_client):
        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(content="Mocked response"))
        ]
        mock_groq_client.chat.completions.create.return_value = mock_completion

        with patch.dict(os.environ, {"GROQ_MODEL": "custom-test-model"}):
            res = app.ask_ai_api("test query")
            self.assertEqual(res, "Mocked response")
            mock_groq_client.chat.completions.create.assert_called_once()
            call_kwargs = mock_groq_client.chat.completions.create.call_args[1]
            self.assertEqual(call_kwargs["model"], "custom-test-model")

    @patch('app.client')
    def test_ask_ai_api_default_model(self, mock_groq_client):
        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(message=MagicMock(content="Default model response"))
        ]
        mock_groq_client.chat.completions.create.return_value = mock_completion

        with patch.dict(os.environ, {}, clear=True):
            res = app.ask_ai_api("test query")
            self.assertEqual(res, "Default model response")
            call_kwargs = mock_groq_client.chat.completions.create.call_args[1]
            self.assertEqual(call_kwargs["model"], "openai/gpt-oss-120b")

    @patch('app.client')
    def test_ask_ai_deep_search_valid_cve(self, mock_groq_client):
        mock_completion = MagicMock()
        mock_completion.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "analysis": "Log4Shell vulnerability",
                        "exploits": [{"title": "Log4j PoC", "url": "https://github.com/example"}]
                    })
                )
            )
        ]
        mock_groq_client.chat.completions.create.return_value = mock_completion

        res = app.ask_ai_deep_search("CVE-2021-44228")
        self.assertTrue(res["valid"])
        self.assertIn("data", res)
        self.assertEqual(res["data"]["analysis"], "Log4Shell vulnerability")

    def test_ask_ai_deep_search_invalid_input(self):
        res = app.ask_ai_deep_search("invalid search term")
        self.assertFalse(res["valid"])
        self.assertIn("error", res)

    @patch('app.ask_ai_api')
    def test_api_ask_ai_endpoint(self, mock_ask_ai_api):
        mock_ask_ai_api.return_value = "AI response string"
        response = self.app_client.post(
            '/api/ask_ai',
            data=json.dumps({"query": "apache"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["ai_interpretation"], "AI response string")


if __name__ == '__main__':
    unittest.main()
