let x=10; func read(){return x;} func caller(){let x=99; return read();} print(caller());
