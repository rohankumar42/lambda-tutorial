from lambda_executor import Lambda


def double(x):
    return 2 * x


if __name__ == "__main__":
    executor = Lambda()
    res = [executor.run(double, i) for i in range(10)]
    print('Got results:', res)
    executor.stop()
