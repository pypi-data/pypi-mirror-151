from pathlib import Path

import pytest

from .intermediate_repr import create_internal_repr_texfile

path_package = Path(__file__).absolute().parent
path_cases_test = path_package.parent.parent / "cases_test"

print(path_cases_test)
cases = sorted(path_cases_test.glob("*.tex"))

@pytest.mark.parametrize("index_case", range(len(cases)))
def test_dump(index_case):

    path_input = cases[index_case]

    if any(letter in path_input.name for letter in "27"):
        pytest.xfail("Bugs texsoup!")

    repr = create_internal_repr_texfile(path_input, verbose=True)
    repr.dump(check=True)
