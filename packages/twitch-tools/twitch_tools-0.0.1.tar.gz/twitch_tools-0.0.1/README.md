# Twitch Tools

## Instalation
    ```
    pip install twitch_tools
    ```

## Usage

Following a user on twitch:
```py
from twitch_tools import follow
follow("<username>", "<account token>")
```

Unfollowing a user on twitch:
```py
from twitch_tools import unfollow
unfollow("<username>", "<account token>")
```

Sending a friend request to a user on twitch:
```py
from twitch_tools import friend
friend("<username>", "<account token>")
```