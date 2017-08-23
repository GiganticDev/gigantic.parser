#!/usr/bin/env python
# encoding: utf-8

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


setup(
		name = "gigantic.parser",
		version = "0.0.1",

		description = "",
		long_description = "",
		url = "https://github.com/GiganticDev/gigantic.parser",
		license = "",
		keywords = [],

		packages = find_packages(exclude=['test', 'example', 'conf', 'benchmark', 'tool', 'doc']),
		include_package_data = True,
		package_data = {'': [
				'README.rst',
			]},

		namespace_packages = [
				'gigantic',
			],

		setup_requires = [
				'pytest-runner',
			],

		tests_require = [
				'pytest-runner',
				'coverage',
				'pytest',
				'pytest-cov',
				'pytest-spec',
				'pytest-flakes',
			],

		install_requires = [
				'marrow.schema',
			],

		extras_require = dict(
				development = [
						'pytest-runner',
						'coverage',
						'pytest',
						'pytest-cov',
						'pytest-spec',
						'pytest-flakes',
					],
			),

		zip_safe = True,

		entry_points = {
				},
	)
