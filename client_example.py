from lambda_executor import Lambda


def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


if __name__ == "__main__":
    executor = Lambda()
    jobs = [executor.run(fib, n=i) for i in range(10)]
    print('All tasks sent out!')
    results = [executor.get_result(job) for job in jobs]
    print('Got results:', results)
    executor.stop()
