from __future__ import annotations

import io
import unittest
from unittest.mock import patch

from chatmock import cli


class CliOutputTests(unittest.TestCase):
    def test_progress_bar_is_ascii(self) -> None:
        bar = cli._render_progress_bar(52.5)
        self.assertEqual(bar, "[###############=--------------]")
        bar.encode("ascii")

    @patch("chatmock.cli._print_usage_limits_block")
    @patch("chatmock.cli.read_auth_file", return_value={})
    @patch("chatmock.cli.load_chatgpt_tokens", return_value=(None, None, None))
    def test_info_output_is_ascii_when_not_signed_in(self, _load_tokens, _read_auth, _print_limits) -> None:
        output = io.StringIO()
        with patch("sys.stdout", output), patch("sys.argv", ["chatmock", "info"]):
            with self.assertRaises(SystemExit) as ctx:
                cli.main()
        self.assertEqual(ctx.exception.code, 0)
        rendered = output.getvalue()
        rendered.encode("ascii")
        self.assertIn("Account", rendered)
        self.assertIn("Run: chatmock login", rendered)

    @patch("chatmock.cli._print_usage_limits_block")
    @patch("chatmock.cli.read_auth_file", return_value={"tokens": {}})
    @patch(
        "chatmock.cli.load_chatgpt_tokens",
        return_value=("access-token", "acct-123", "id-token"),
    )
    @patch(
        "chatmock.cli.parse_jwt_claims",
        side_effect=[
            {"email": "nclay@p3adaptive.com"},
            {"https://api.openai.com/auth": {"chatgpt_plan_type": "pro"}},
        ],
    )
    def test_info_output_is_ascii_when_signed_in(
        self,
        _parse_claims,
        _load_tokens,
        _read_auth,
        _print_limits,
    ) -> None:
        output = io.StringIO()
        with patch("sys.stdout", output), patch("sys.argv", ["chatmock", "info"]):
            with self.assertRaises(SystemExit) as ctx:
                cli.main()
        self.assertEqual(ctx.exception.code, 0)
        rendered = output.getvalue()
        rendered.encode("ascii")
        self.assertIn("Signed in with ChatGPT", rendered)
        self.assertIn("Login: nclay@p3adaptive.com", rendered)
        self.assertIn("Plan: Pro", rendered)


if __name__ == "__main__":
    unittest.main()
