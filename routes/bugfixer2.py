def max_bugsfixed(bug_seq):
    bug_seq.sort(key=lambda x: x[1])
    current_time = 0
    max_bugs = 0

    for bug in bug_seq:
        if bug[1] >= current_time + bug[0]:
            current_time += bug[0]
            max_bugs += 1

    return max_bugs

# Test cases
print(max_bugsfixed([[20,30],[30,150],[110,135],[210,330]]))  # Output: 3
print(max_bugsfixed([[3,2],[4,3]]))  # Output: 0
print(max_bugsfixed([[5,7]]))  # Output: 1