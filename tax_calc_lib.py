def calc_tax(salary, brackets):
    tax = 0
    for threshold, rate in reversed(brackets.items()):
        threshold = int(threshold)
        if salary > threshold:
            excess = salary - threshold
            tax += excess * rate
            salary -= excess

    return tax
