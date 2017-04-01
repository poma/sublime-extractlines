import functools
import itertools
import re
import sublime
import sublime_plugin

class ExtractDuplicateLinesCommand(ExtractUniqueLinesCommand):

    def run(self, edit):
        self._run(edit, True)
        

class ExtractUniqueLinesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self._run(edit, False)

    def _run(self, edit, duplicate):
        results_view = self.view.window().new_file()
        results_view.set_name('Extract Results')
        results_view.set_scratch(True)
        results_view.settings().set('word_wrap', self.view.settings().get('word_wrap'))

        # This is the only way I found to extract a list of all lines, probably there is a more optimal one
        # Also is could be better to take newline symbol form current view settings
        ranges = self.view.lines(sublime.Region(0, self.view.size()))
        lines = ['%s\n' % (self.view.substr(r)) for r in ranges]
        lines = self.filter(lines, duplicate)
        text = ''.join(lines)
        results_view.run_command('append', {'characters': text, 'force': True, 'scroll_to_end': False})
        results_view.set_syntax_file(self.view.settings().get('syntax'))

    def filter(self, lines, duplicate):
        duplicates = set(self.find_duplicates(lines));
        return [l for l in lines if (l not in duplicates) ^ duplicate]

    def find_duplicates(self, lines):
        seen = set()
        return [l for l in lines if l in seen or seen.add(l)]
