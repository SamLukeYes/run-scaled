# run-scaled

***NOTICE: Xpra 4.1 already has a `run_scaled` script rewritten in Python. If Xpra developers add IME support to their `run_scaled` script, this one will be deprecated.***

Run an X application scaled via xpra. Originally [run_scaled](https://github.com/kaueraal/run_scaled), rewritten in Python, with experimental input method support added (use `--ime` flag to specify your IME daemon).

## Dependencies
* xvfb
* [xpra](https://xpra.org/) >= 2
* xrandr