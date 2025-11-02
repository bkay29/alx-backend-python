
#!/usr/bin/python3
from itertools import islice
stream_users = __import__('0-stream_users')

# Print the first six streamed rows
for user in islice(stream_users.stream_users(), 6):
    print(user)
