// Sample Program 4: parameters, return values, and scope

func square(n) {
    let result = n * n;
    return result;
}

func add(x, y) {
    return x + y;
}

func hello() {
    print(1);
    return;
}

let answer = add(square(3), square(4));
hello();
print(answer);
