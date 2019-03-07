# -*- coding: utf-8 -*-
import unittest
import pkg_resources
import os
from pathlib import Path


class TestRequirements(unittest.TestCase):
    def setUp(self):
        self.basedir = os.path.abspath(
                    os.path.dirname(  # root
                        os.path.dirname(  # project
                            os.path.dirname(  # server
                                os.path.dirname(  # api
                                    os.path.dirname(__file__))))))  # tests

    def test_all_requirements_are_installed(self):
        requirements = Path(f'{self.basedir}/requirements.txt') \
            .read_text() \
            .strip() \
            .split('\n')

        pkg_resources.require(requirements)
