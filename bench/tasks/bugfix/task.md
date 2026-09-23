The function `running_sum` in `calc.py` is wrong: `running_sum([1, 2, 3])` returns `[1, 3]` instead of `[1, 3, 6]`, and `running_sum([5])` returns `[]`.

Find the bug and fix it with a minimal change. Do not rename the function, do not change its signature, do not add dependencies. The docstring contract is: prefix sums, so `running_sum([1,2,3]) == [1, 3, 6]`, `running_sum([]) == []`.
