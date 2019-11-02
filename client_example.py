from lambda_executor import Lambda


def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


if __name__ == "__main__":
    executor = Lambda()
    res = [executor.run(fib, n=i) for i in range(10)]
    print('Got results:', res)
    executor.stop()
