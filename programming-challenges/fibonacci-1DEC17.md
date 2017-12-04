## Write a function `fib()` that a takes an integer n and returns the nth Fibonacci number.

Let's say our Fibonacci series is 0-indexed and starts with 0. So:

```
fib(0)  # => 0
fib(1)  # => 1
fib(2)  # => 1
fib(3)  # => 2
fib(4)  # => 3
```

### Tim

Python

```
def fib(total_iter, curr_iter=0, prev_val=0, curr_val=0):
    if curr_iter < 2:
        prev_val, curr_val, output = 0, 1, curr_iter
    else:
        prev_val, curr_val, output = curr_val, (prev_val + curr_val), (prev_val + curr_val)

   if curr_iter != total_iter:
        fib(total_iter, curr_iter + 1, prev_val, curr_val)
    else:
        print(output)
```

### Addam

Javascript. Memoized

```
function fib(n) {
  function fibMemo(n, memo) {
    if (memo[n]) {
      return memo[n];
    }

    let fibNum = fibMemo(n - 1, memo) + fibMemo(n -2, memo);
    memo[n] = fibNum;
    return fibNum;
  }

  let memo = { 1: 1, 2: 1 };
  return fibMemo(n, memo)
}
```
