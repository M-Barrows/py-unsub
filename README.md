# Py-Unsubscribe

This project was born out of my neglect for my own Gmail inbox. Rather than simply cleaning out my inbox using tools that already existed, I decided to spend days creating a python app that is slower, and less feature-rich. 

![](https://imgs.xkcd.com/comics/is_it_worth_the_time.png)

# Quickstart

For now you will need to create your own Google cloud project in order to use this project. Use [this walkthrough](https://developers.google.com/gmail/api/quickstart/python) to get started. 

Once the project is created and you have the `credentials.json` and `token.json` files, you can run the following commands to start the application.  

```bash
pip install virtualenv
python -m virtualenv .venv
pip install -r requirements.txt
python ui.py
```

# Contributing

You are welcome to create PRs for this project. I don't have a grand vision other than creating a quick way for me to tame my email newsletters. 

# To-Do List

- [x] ~~Open all unsubscribe links at once~~

- [x] ~~Give option to Select All~~

- [ ] Package code into executable (Windows only for now)

- [ ] Enable Auth for more users than just the owner

- [ ] Mark all emails from unsubscribed newsletters read

- [ ] Move all emails from unsubscribed newsletters to special folder as fail-safe

- [ ] Auto-unsubscribe (no user input) from as many emails as possible
