"""
This module is used for checking the project code for compliance with PEP8.

"""

from typing import List, Optional
import os

import pylint.lint


DEFAULT_IGNORED_DIRS = {
    'venv', 'env', '.idea', '.pytest_cache', '__pycache__'
}


class PyLinter:
    """
    Class for checking the project code for compliance with PEP8.

    Parameters
    ----------
    is_printed : bool, default: False
        If it is True, pylint options are printed.
    ignored_paths : set, optional
        Set of paths that are ignored by checking.
    ignored_statements : set, optional
        Set of PEP statements that are ignored by checking.
    root_directory : str, optional
        Root directory of checking.
        If it is None, current work directory is used.

    References
    ----------
    https://docs.pylint.org/en/latest/technical_reference/features.html

    Raises
    ------
    FileNotFoundError
        If the path `root_directory` is not found.

    """

    def __init__(
            self,
            is_printed: bool = False,
            ignored_paths: Optional[set] = None,
            ignored_statements: Optional[set] = None,
            root_directory: Optional[str] = None,
    ):
        """Initialize self. See help(type(self)) for accurate signature."""
        self.root_directory = root_directory or os.getcwd()
        self.is_printed = is_printed
        self.ignored_paths = ignored_paths
        self.ignored_statements = ignored_statements
        if not os.path.exists(self.root_directory):
            raise FileNotFoundError(
                f'The path "{self.root_directory}" is not found.'
            )

    def get_inspected_files(self, ignored: List[str]) -> List[str]:
        """
        Return list of files checking for compliance with PEP8.

        Parameters
        ----------
        ignored : list
            List of paths that are ignored by checking.

        Returns
        -------
        list
            List of files checking for compliance with PEP8.

        Raises
        ------
        ValueError
            If the list of inspected files is empty.

        """
        inspected_files = []
        for dir_name, _, files in os.walk(self.root_directory):
            is_ignored = False
            for path in ignored:
                if dir_name.startswith(path):
                    is_ignored = True
                    break
            if is_ignored:
                continue
            for file in files:
                if dir_name not in ignored and file.endswith('.py'):
                    file_name = os.path.join(dir_name, file)
                    if file_name in ignored:
                        continue
                    inspected_files.append(file_name)
        if not inspected_files:
            raise ValueError('The list of inspected files is empty.')
        return inspected_files

    def get_pylint_options(self) -> List[str]:
        """Return list of pylint options."""
        pylint_options = ['--ignore-imports=yes']
        _ignored_paths = self.ignored_paths or set()
        _ignored_paths.update(DEFAULT_IGNORED_DIRS)
        if self.ignored_statements:
            for statement in self.ignored_statements:
                _requirement = (
                        len(statement) == 5
                        and statement[0].isupper()
                        and statement[1:].isdigit()
                )
                if _requirement:
                    pylint_options.append(f'--disable={statement}')
        pylint_options += self.get_inspected_files(
            ignored=[
                os.path.join(self.root_directory, path)
                for path in _ignored_paths
            ],
        )
        if self.is_printed:
            print(*pylint_options, sep='\n')
        return pylint_options

    def check(self):
        """Check the project code for compliance with PEP8."""
        pylint.lint.Run(self.get_pylint_options())
