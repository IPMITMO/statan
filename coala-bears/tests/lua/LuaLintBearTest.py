from bears.lua.LuaLintBear import LuaLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """
print("Hello World!")
"""


bad_file = """
function factorial(n)
  local x = 1
  for i = 2, n do;
    x = x * i
  end
  return x
end
"""


LuaLintBearTest = verify_local_bear(LuaLintBear,
                                    valid_files=(good_file,),
                                    invalid_files=(bad_file,))
