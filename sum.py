def read_input():
    # Read the number of test cases
    N = int(input())
    test_cases = []
    for _ in range(N):
        # Read X and the list of integers
        X = int(input())
        integers = list(map(int, input().split()))
        test_cases.append(integers)
    return test_cases

def filter_and_sum_squares(integers):
    # Filter out negative integers and calculate squares
    positive_squares = map(lambda x: x ** 2, filter(lambda x: x >= 0, integers))
    return sum(positive_squares)

def main():
    test_cases = read_input()
    total_sum = sum(filter_and_sum_squares(case) for case in test_cases)
    print(total_sum)

if __name__ == "__main__":
    main()