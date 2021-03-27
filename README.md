# IRC-logger

Not much to say - the bot doesn't have much dependancies if not none.

To run, make a config.py file containing a few information such as your username/IRC pass/list of channels. File example:

```python
botnick = "your_username"
passwd = "your_IRC_pass"

# you can add channels freely as long as they exist. #announce might have some issues with links
channels = [
    'french',
    'osu',
    'english'
]
```


Once you have that file in the same directory as `noname.py`, you can run the bot in any terminal:

```
python3 noname.py
```

Would you need to quit the bot, as KeyboardInterrupt won't work, type "QUIT" and enter. It'll close both threads and exit.
