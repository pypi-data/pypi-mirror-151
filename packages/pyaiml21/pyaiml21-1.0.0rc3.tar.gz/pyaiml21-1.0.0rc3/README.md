# pyaiml21

AIML[^1] 2.1 Chatbot Design Language Interpreter in Python 3.

The AIML language is a (simple) XML-derived language for description of chatbots
and the communication with the user based on the pattern-matching the user's
query and evaluating (human-coded) response.

**pyaiml21** is an AIML interpreter, supporting the latest AIML specification.
It was created as a bachelor thesis and should be fully compatible with
its predecessor, **PyAiml**[^2].



## Installation

Install the project from *PYPI*:

```console
$ python -m pip install pyaiml21
```


## Quick Example

This example demonstrates how to quickly set-up and run a basic chatbot with
publicly available source files from ALICE[^5].


### Running via console script

`pyaiml21` comes with a simple script to run your chatbots, if you unpacked
the contents of your bot into `alice/` folder (so that the structure
is `alice/aiml/..`, `alice/aimlif/..`, `alice/sets/..` ..), then running
the following will start your bot:

    $ aiml --bot alice


### Running from Python

It is still possible to start your bot directly from python[^3], e.g.

    >>> from pyaiml21 import Bot
    >>> my_bot = Bot()
    >>> my_bot.learn_aiml("path to .aiml file")
    >>> # more loading stuff, see `pyaiml21.utils` for helpers
    >>> my_bot.respond("Hello", "USER_1")
    Hi! How are you doing?


For examples of simple bots, checkout `/examples` folder.


## Motivation

This project was created to support the AIML 2.1 in Python while preserving
the simplicity of user interface from **pyaiml**. Note that for Python,
there exists an AIML interpreter, **program-y** [^4], but it does
come with the full chatbot platform, the simple interface is missing.


## Documentation

Please visit the
[official documentation](https://pyaiml21.readthedocs.io/en/latest/).


## License

MIT.

---

[^5]: [alice source code](https://code.google.com/archive/p/aiml-en-us-foundation-alice/)

[^1]: Artificial Intelligence Markup Language (Dr. Wallace, 2001); see
the official [specification of version 2.1](http://www.aiml.foundation/doc.html).

[^3]: The actual response depends on your AIML file, to load .aimlif,
    substitutions.., see methods of `pyaiml21.Bot`

[^2]: [original interpreter in python for AIML 1.0](https://github.com/cdwfs/pyaiml)

[^4]: [AIML Interpreter in Python3]((https://github.com/keiffster/program-y))