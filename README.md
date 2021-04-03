# run-scaled

***This one is deprecated. To use IME in other versions of `run_scaled`, add `input-method=keep` and other necessary arguments (for me, it is `start=fcitx5`) to `~/.config/xpra/xpra.conf`***

Run an X application scaled via xpra. Originally [run_scaled](https://github.com/kaueraal/run_scaled), rewritten in Python, with experimental input method support added (use `--ime` flag to specify your IME daemon).

## Dependencies
* xvfb
* [xpra](https://xpra.org/) >= 2
* xrandr