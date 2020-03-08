def solution(l, t):
    s = 0
    i = 0
    x = 1
    
    if s == t:
        return (0, 0)

    while i < x and x < len(l) + 1:
        if l[i] == t:
            return (i, i)
        s = sum(l[i:x])
        if s < t:
            x += 1
        elif s > t:
            i += 1
        else:
            return (i, x - 1)
        # print(l[i:x])
    return (-1, -1)

print(solution([1, 0, 0, 0, 0, 4], 5))