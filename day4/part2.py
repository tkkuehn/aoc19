def meets_criteria(num, min_, max_):
    if num < min_:
        return False

    if num > max_:
        return False

    digit_list = [int(i) for i in str(num)]

    if len(digit_list) != 6:
        return False

    cur_adjacent_same = 1
    adjacent_blocks = []

    for i in range(5):
        if digit_list[i + 1] < digit_list[i]:
            return False

        if digit_list[i + 1] == digit_list[i]:
            cur_adjacent_same += 1
        else:
            adjacent_blocks.append(cur_adjacent_same)
            cur_adjacent_same = 1

    adjacent_blocks.append(cur_adjacent_same)

    return 2 in adjacent_blocks

meet_count = 0

min_ = int(input('Min: '))
max_ = int(input('Max: ')) 

for i in range(min_, max_ + 1):
    if meets_criteria(i, min_, max_):
        meet_count += 1

print(meet_count)

