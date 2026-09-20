let scores = [90, 85, 100];
let empty = [];
scores[1] = 100;
scores[scores[0] - 89] = scores[2] + 1.5;
let first = scores[0];
print(first);

func total(values) {
    let sum = 0;
    for (let i = 0; i < 3; i = i + 1) {
        sum = sum + values[i];
    }
    return sum;
}
print(total([1, 2, 3]));
