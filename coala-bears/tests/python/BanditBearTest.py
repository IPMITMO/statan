from queue import Queue
import os.path

from coalib.settings.Section import Section
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.testing.LocalBearTestHelper import (
    LocalBearTestHelper, verify_local_bear)

from bears.python.BanditBear import BanditBear


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__), 'bandit_test_files', name)


def load_testfile(name, splitlines=False):
    with open(get_testfile_path(name)) as fl:
        contents = fl.read()

    if splitlines:
        contents = contents.splitlines(True)

    return contents


def test(testfilename, expected_results):
    def test_function(self):
        bear = BanditBear(Section(''), Queue())
        self.check_results(bear, load_testfile(testfilename, True),
                           expected_results, get_testfile_path(testfilename),
                           create_tempfile=False)
    return test_function


class BanditBearTest(LocalBearTestHelper):
    test_assert = test(
        'assert.py',
        [Result.from_values('B101', 'Use of assert detected. The enclosed '
                            'code will be removed when compiling to optimised '
                            'byte code.', get_testfile_path('assert.py'), 1,
                            end_line=1, severity=RESULT_SEVERITY.INFO,
                            confidence=90)])

    test_exec_py2_py = test(
        'exec-py2.py',
        [Result.from_values('BanditBear', 'syntax error while parsing AST '
                            'from file', get_testfile_path('exec-py2.py'),
                            severity=RESULT_SEVERITY.MAJOR)])

    test_jinja2_templating = test(
        'jinja2_templating.py',
        [Result.from_values('B701', 'Using jinja2 templates with '
                            'autoescape=False is dangerous and can lead to '
                            'XSS. Ensure autoescape=True to mitigate XSS '
                            'vulnerabilities.',
                            get_testfile_path('jinja2_templating.py'), 9,
                            end_line=9, severity=RESULT_SEVERITY.MAJOR,
                            confidence=70),
         Result.from_values('B701', 'Using jinja2 templates with '
                            'autoescape=False is dangerous and can lead to '
                            'XSS. Use autoescape=True to mitigate XSS '
                            'vulnerabilities.',
                            get_testfile_path('jinja2_templating.py'), 10,
                            end_line=10, severity=RESULT_SEVERITY.MAJOR,
                            confidence=90),
         Result.from_values('B701', 'Using jinja2 templates with '
                            'autoescape=False is dangerous and can lead to '
                            'XSS. Use autoescape=True to mitigate XSS '
                            'vulnerabilities.',
                            get_testfile_path('jinja2_templating.py'), 11,
                            end_line=13, severity=RESULT_SEVERITY.MAJOR,
                            confidence=90),
         Result.from_values('B701', 'By default, jinja2 sets autoescape to '
                            'False. Consider using autoescape=True to '
                            'mitigate XSS vulnerabilities.',
                            get_testfile_path('jinja2_templating.py'), 15,
                            end_line=16, severity=RESULT_SEVERITY.MAJOR,
                            confidence=90)])

# The following test will ignore some error codes, so "good" and "bad" doesn't
# reflect the actual code quality.


good_files = ('good_file.py', 'assert.py')

bad_files = ('exec-py2.py', 'httpoxy_cgihandler.py', 'jinja2_templating.py',
             'skip.py')
skipped_error_codes = ['B105', 'B106', 'B107', 'B404', 'B606', 'B607', 'B101']

BanditBearSkipErrorCodesTest1 = verify_local_bear(
    BanditBear,
    valid_files=tuple(load_testfile(file) for file in good_files),
    invalid_files=tuple(load_testfile(file) for file in bad_files),
    settings={'bandit_skipped_tests': ','.join(skipped_error_codes)},
    tempfile_kwargs={'suffix': '.py'})


good_files = ('good_file.py',)
bad_files = ('exec-py2.py', 'httpoxy_cgihandler.py', 'jinja2_templating.py',
             'skip.py', 'assert.py')

BanditBearSkipErrorCodesTest2 = verify_local_bear(
    BanditBear,
    valid_files=tuple(load_testfile(file) for file in good_files),
    invalid_files=tuple(load_testfile(file) for file in bad_files),
    settings={'bandit_skipped_tests': ''},
    tempfile_kwargs={'suffix': '.py'})
