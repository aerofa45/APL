func sum(values, count) {
    let total = 0;
    for (let i = 0; i < count; i = i + 1) {
        total = total + values[i];
    }
    return total;
}
let scores = [90, 85, 100];
scores[1] = 95;
print(scores);
print(sum(scores, 3));
