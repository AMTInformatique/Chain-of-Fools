from hashlib import sha512
x = 3
y = 0  # We don't know what y should be yet...
while sha512(f'{x*y}'.encode()).hexdigest()[:4] != "abcd":
    print(f'{x*y}')
    print(f'{x*y}'.encode())
    print(sha512(f'{x*y}'.encode()).hexdigest())
    y += 1
print(f'The solution is y = {y}')