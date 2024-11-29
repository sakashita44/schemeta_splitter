import unittest
import subprocess


class TestCLI(unittest.TestCase):
    def test_cli(self):
        result = subprocess.run(
            ["schemeta_splitter", "-h"], capture_output=True, text=True
        )
        self.assertIn("usage", result.stdout)


if __name__ == "__main__":
    unittest.main()
