import os
import sys
from os import environ
import subprocess


class LucidLoadingBar:
    reset = "\033[38;2;200;200;200m" if not sys.stdout.isatty() else ''

    def __init__(
            self, iterable=None, prefix='Loading...', prefix_color=None, suffix='',
            suffix_color=None, bar_color=None, percent_color=None, decimals=1,
            length=100, fill=None, print_end='\r', is_loading=None, total=0, bar_format=None
    ):
        self.iterable = iterable
        self.prefix = prefix
        self.prefix_color = prefix_color
        self.suffix = suffix
        self.suffix_color = suffix_color
        self.bar_color = "\033[38;2;0;255;255m" if not sys.stdout.isatty() else ''
        self.percent_color = percent_color
        self.decimals = decimals
        self.length = length
        self.fill = '\xdb' if environ.get('SHELL') else '\u2588'
        self.print_end = print_end
        self.is_loading = is_loading
        self.progress = 0
        self.total = total
        self.bar_format = "$RESET$PREFIX_COLOR$PREFIX$RESET |$BAR_COLOR$BAR$RESET| $PERCENT_COLOR$PERCENT$RESET"

    def get_bar(self):
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.progress / float(self.total)))
        filled_length = int(self.length * self.progress // self.total)
        bar = self.fill * filled_length + "-" * (self.length - filled_length)

        return self.format_bar(bar=bar, percent=percent)

    def get_clear_bar(self):
        return ''.join(' ' for i in range(len(self.prefix) + self.length + 9))

    def format_bar(self, bar, percent):
        formatted_bar = self.bar_format.replace(
            '$PREFIX_COLOR', self.prefix_color if self.prefix_color else ''
        ).replace(
            '$RESET', self.reset
        ).replace(
            '$PREFIX', self.prefix
        ).replace(
            '$BAR_COLOR', self.bar_color if self.bar_color else ''
        ).replace(
            '$BAR', bar
        ).replace(
            '$PERCENT_COLOR', self.percent_color if self.percent_color else ''
        ).replace(
            '$PERCENT', percent
        )

        return formatted_bar

    def init_bar(self, iterable=None, prefix="Loading...", total=None):
        try:
            tput = subprocess.Popen(['tput', 'cols'], stdout=subprocess.PIPE)
            terminal_length = int(tput.communicate()[0].strip())
        except FileNotFoundError:
            terminal_length = 100

        self.is_loading = True
        self.total = len(iterable) if iterable else total
        self.length = (terminal_length - len(self.prefix) - 10)
        self.prefix = prefix
        return self

    def finish_loading(self):
        self.is_loading = False
        self.total = 0
        self.prefix = ''
        self.progress = 0

    def progress_bar(self):
        self.progress += 1
