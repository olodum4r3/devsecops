#!/usr/local/bin/python3

count = 0

while count < 10:
    if count % 2 == 0:
        count += 1
        continue
    print(f"we are counting odd numbers: {count}")
    count += 1