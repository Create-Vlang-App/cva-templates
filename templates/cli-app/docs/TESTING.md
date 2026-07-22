# Testing

```bash
v test .
v vet .
v run . --name Alice
v run . --help
```

Feature tests live beside each module (`greet/greet_test.v`). Keep CLI wiring tests in `main_test.v`.
