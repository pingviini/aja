import unittest
# import docopt

from aja.main import Aja


class TestMain(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        aja = Aja({'<name>': ['test']})
        self.assertTrue(aja)
        self.assertTrue(aja.configs)
        self.assertEqual(len(aja.configs), 1)

    def test_actions(self):
        aja = Aja({'<name>': 'test'})
        actions = ['info', 'register', 'buildout', 'show-config',
                   'list-plugins', 'deploy', 'clone', 'bootstrap', 'list',
                   'update']
        self.assertEqual(actions, aja.actions.keys())
        self.assertEqual(aja.actions['info'], aja.show_info)
        self.assertEqual(aja.actions['register'], aja.register)
        self.assertEqual(aja.actions['buildout'], aja.run_buildout)
        self.assertEqual(aja.actions['show-config'], aja.show_config)
        self.assertEqual(aja.actions['deploy'], aja.deploy)
        self.assertEqual(aja.actions['clone'], aja.clone_buildout)
        self.assertEqual(aja.actions['bootstrap'], aja.bootstrap_buildout)
        self.assertEqual(aja.actions['list'], aja.list_buildouts)
        self.assertEqual(aja.actions['update'], aja.update_buildout)


if __name__ == '__main__':
    unittest.main()
