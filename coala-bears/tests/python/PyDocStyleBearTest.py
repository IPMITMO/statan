from bears.python.PyDocStyleBear import PyDocStyleBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = '''
"""example module level docstring."""


def hello():
    """Print hello world."""
    print("hello world")

'''


bad_file = '''
"""
example module level docstring
"""

def hello():
    print("hello world")

'''

PyDocStyleBearTest = verify_local_bear(
    PyDocStyleBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,),
    tempfile_kwargs={'suffix': '.py'})

PyDocStyleBearIgnoreAllTest = verify_local_bear(
    PyDocStyleBear,
    valid_files=(good_file, bad_file,),
    invalid_files=(),
    settings={'pydocstyle_ignore': 'D400, D200, D103, D212'},
    tempfile_kwargs={'suffix': '.py'})

# Checks if an invalid file yields results when only some errors are ignored.
PyDocStyleBearIgnoreSomeTest = verify_local_bear(
    PyDocStyleBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,),
    settings={'pydocstyle_ignore': 'D400, D200'},
    tempfile_kwargs={'suffix': '.py'})

# Checks the functionality of add-ignore
PyDocStyleBearAddIgnoreTest = verify_local_bear(
    PyDocStyleBear,
    valid_files=(good_file, bad_file,),
    invalid_files=(),
    settings={'pydocstyle_add_ignore': 'D400, D200, D103'},
    tempfile_kwargs={'suffix': '.py'})

# Checks if an invalid file yields results when a particular error is selected.
PyDocStyleBearSelectSomeTest = verify_local_bear(
    PyDocStyleBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,),
    settings={'pydocstyle_select': 'D200'},
    tempfile_kwargs={'suffix': '.py'})

# Checks if an invalid file yields nothing when the selected error never
# occurs.
PyDocStyleBearSelectAbsentErrorTest = verify_local_bear(
    PyDocStyleBear,
    valid_files=(good_file, bad_file,),
    invalid_files=(),
    settings={'pydocstyle_select': 'D500'},
    tempfile_kwargs={'suffix': '.py'})

# Checks the functionality of add-select
PyDocStyleBearAddSelectTest = verify_local_bear(
    PyDocStyleBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,),
    settings={'pydocstyle_add_select': 'D212'},
    tempfile_kwargs={'suffix': '.py'})

PyDocStyleBearSelectAndIgnoreTest = verify_local_bear(
    PyDocStyleBear,
    valid_files=(good_file, bad_file,),
    invalid_files=(),
    settings={'pydocstyle_select': 'D200',
              'pydocstyle_ignore': 'D400'},
    tempfile_kwargs={'suffix': '.py'})
