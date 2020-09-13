# DDG Signal Bot

A bot for [Signal Messenger](https://signal.org/) that talks to [DuckDuckGo](https://duckduckgo.com/)
API and [Bang](https://duckduckgo.com/bang) shortcuts.

## Install

The bot requires the [Signal-CLI](https://github.com/asamk/signal-cli/) to be
running in the daemon mode and a valid python version that supports f-strings
(v3.6+).

```
$ pipenv shell
$ pipenv sync
$ signal-cli -u <signal_phone_number> daemon --json
$ python bot.py
```

## Usage

To invoke the bot, you need to use a `PREFIX`. The default `PREFIX` is `!bot`.

For example,

```
!bot Signal Messenger

## Searches the DuckDuckGo API for Signal Messenger and responds

https://en.wikipedia.org/wiki/Signal_Messenger
Signal Messenger, LLC, is a software organization that was founded by Moxie Marlinspike and Brian Acton in 2018 to take over the role of the Open Whisper Systems project that Marlinspike founded in 2013. Its main focus is the development of the Signal app and the Signal Protocol. The organization is funded by the non-profit Signal Foundation, and all of its products are published as free and open-source software.
```

To use the DDG bang, use the `PREFIX` followed by the bang syntax.

```
!bot !w DuckDuckGo

## Searches Wikipedia for DuckDuckGo
https://en.wikipedia.org/wiki/DuckDuckGo
```

## Credits

* Signal Messenger.
* Signal-CLI for the easy to use library to interact with the Signal Messenger.
* DuckDuckGo for the free and permissible API and safeguarding user privacy.

## License

Please refer to the `LICENSE` file for more details.
