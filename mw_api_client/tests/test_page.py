"""Test various aspects of Pages."""
from unittest import TestCase
from sys import version_info
import mw_api_client as mw

if version_info[0] > 2:
    basestring = str # pylint: disable=invalid-name

WP = mw.Wiki('https://en.wikipedia.org/w/api.php', 'Test suite')
class TestPage(TestCase):
    """Test Pages."""
    def test_revisions(self):
        """Test getting Revisions of a Page."""
        sandbox = WP.page('Project:Sandbox')
        for rev in sandbox.revisions(limit=10, rvprop='content'):
            self.assertIsInstance(rev.content, basestring)
    def test_read_is_string(self):
        """Assert that reading content returns a string (or basestring)."""
        sandbox = WP.page('Project:Sandbox')
        content = sandbox.read()
        self.assertIsInstance(content, basestring)
    def test_edit_success(self):
        """Assert successful edits return result 'Success'."""
        sandbox = WP.page('Project:Sandbox')
        try:
            result = sandbox.edit(sandbox.read() + '\n\nTesting edit',
                                  'Testing API edit')
        except mw.WikiError.blocked:
            self.skipTest('This IP is blocked from editing')
            return
        # pylint: disable=unsubscriptable-object
        self.assertEqual(result['edit']['result'], 'Success')
    def test_missing_page(self):
        """Assert that nonexistant pages have the 'missing' attribute set."""
        nonexistant = WP.page('asdfasdfasdfasdfasdfasdfsadfhjklhjklhkjhjkhjkh', getinfo=True)
        self.assertTrue(hasattr(nonexistant, 'missing'))
    def test_user_contribs(self):
        """Assert that User.contribs generates Revisions."""
        jimbo = WP.user('Jimbo Wales')
        for rev in jimbo.contribs(limit=10):
            self.assertIsInstance(rev, mw.Revision)
