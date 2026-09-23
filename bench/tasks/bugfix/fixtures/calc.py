def running_sum(nums):
    """Prefix sums: running_sum([1,2,3]) == [1, 3, 6]."""
    total = 0
    result = []
    for i in range(len(nums) - 1):
        total += nums[i]
        result.append(total)
    return result
