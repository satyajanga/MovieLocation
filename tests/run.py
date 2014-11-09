#!/usr/bin/python
import unittest
import sys
import test_movies

def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(test_movies))
    return unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    if main().wasSuccessful():
        sys.exit(0)
    sys.exit(1)
