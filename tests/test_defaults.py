from __future__ import annotations

import unittest

from chatmock.app import create_app
from chatmock.responses_api import normalize_responses_payload


class DefaultLockTests(unittest.TestCase):
    def test_app_defaults_lock_model_and_reasoning(self) -> None:
        app = create_app()
        self.assertEqual(app.config["DEBUG_MODEL"], "gpt-5.4")
        self.assertEqual(app.config["REASONING_EFFORT"], "xhigh")
        self.assertTrue(app.config["LOCK_REQUEST_REASONING"])

    def test_normalize_responses_payload_ignores_requested_model_and_reasoning(self) -> None:
        app = create_app()
        payload = {
            "model": "gpt-5.3-codex-low",
            "input": "Reply with exactly: LOCKED",
            "reasoning": {"effort": "low", "summary": "none"},
        }
        normalized = normalize_responses_payload(payload, config=app.config)
        self.assertEqual(normalized.normalized_model, "gpt-5.4")
        self.assertEqual(normalized.payload["model"], "gpt-5.4")
        self.assertEqual(normalized.payload["reasoning"]["effort"], "xhigh")
        self.assertEqual(normalized.payload["reasoning"]["summary"], "auto")


if __name__ == "__main__":
    unittest.main()
