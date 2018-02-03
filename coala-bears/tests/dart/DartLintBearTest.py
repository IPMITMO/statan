from queue import Queue

from bears.dart.DartLintBear import DartLintBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.LocalBearTestHelper import verify_local_bear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator


good_file = """
printNumber(num aNumber) {
  print('The number is $aNumber.');
}

main() {
  var answer = 42;          // The meaning of life.
  printNumber(answer);
}
"""


bad_file = """
printNumber(num aNumber) {
  print('The number is $aNumber.')
}

main() {
  var answer = 42;          // The meaning of life.
  printNumber(answer)
}
"""


DartLintBearTest = verify_local_bear(DartLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,),
                                     tempfile_kwargs={'suffix': '.dart'})


@generate_skip_decorator(DartLintBear)
class DartLintBearConfigTest(LocalBearTestHelper):

    DART_VALUE_ERROR_RE = ('ValueError: DartLintBear only supports '
                           '`use_spaces=True` and `indent_size=2`')

    def test_config_failure_use_spaces(self):
        section = Section('name')
        section.append(Setting('use_spaces', False))
        bear = DartLintBear(section, Queue())

        with self.assertRaisesRegex(AssertionError, self.DART_VALUE_ERROR_RE):
            self.check_validity(bear, [], good_file)

    def test_config_failure_wrong_indent_size(self):
        section = Section('name')
        section.append(Setting('indent_size', 3))
        bear = DartLintBear(section, Queue())

        with self.assertRaisesRegex(AssertionError, self.DART_VALUE_ERROR_RE):
            self.check_validity(bear, [], good_file)
