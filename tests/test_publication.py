import importlib.util
from pathlib import Path
import tempfile
import unittest

CHECKER = Path(__file__).resolve().parents[1] / 'tools/check_publication.py'
spec = importlib.util.spec_from_file_location('publication', CHECKER)
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)


class PublicationTests(unittest.TestCase):
    def check_text(self, content, filename='example.md'):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / filename).write_text(content, encoding='utf-8')
            return publication.scan(root)[1]

    def test_documentation_address_allowed(self):
        self.assertEqual(self.check_text('Example: 192.0.2.4'), [])

    def test_non_documentation_address_rejected(self):
        address = '.'.join(['10', '42', '0', '1'])
        self.assertTrue(self.check_text(address))

    def test_token_rejected(self):
        token = 'gh' + 'p_' + 'A' * 36
        self.assertTrue(self.check_text(token))

    def test_secret_assignment_rejected(self):
        self.assertTrue(self.check_text('pass' + 'word = example-value'))

    def test_unapproved_binary_extension_rejected(self):
        self.assertTrue(self.check_text('not a real archive', 'export.zip'))


if __name__ == '__main__':
    unittest.main()
