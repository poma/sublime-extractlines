import sublime
import sublime_plugin

settings_path = 'Extract Lines.sublime-settings'

class ExtractUniqueLinesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self._run(edit, False)

    def _run(self, edit, duplicate):
        self.settings = sublime.load_settings(settings_path)
        new_tab = self.settings.get('create_new_tab', False)
        lines = self.filter(duplicate ^ (not new_tab))

        if (new_tab):
            text = '\n'.join([v for k, v in lines])
            self.create_new_tab(text)
        else:
            for k, v in reversed(lines):
                self.view.erase(edit, self.view.full_line(k))

    def create_new_tab(self, text):
        results_view = self.view.window().new_file()
        results_view.set_name('Extract Results')
        results_view.set_scratch(True)
        results_view.settings().set('word_wrap', self.view.settings().get('word_wrap'))
        results_view.run_command('append', {'characters': text, 'force': True, 'scroll_to_end': False})
        results_view.set_syntax_file(self.view.settings().get('syntax'))

    def filter(self, duplicate):
        seen = set()
        lines = [(l, self.view.substr(l)) for l in self.view.lines(sublime.Region(0, self.view.size()))]
        duplicates = {v for k, v in lines if v in seen or seen.add(v)}
        return [(k, v) for k, v in lines if (v not in duplicates) ^ duplicate]


class ExtractDuplicateLinesCommand(ExtractUniqueLinesCommand):

    def run(self, edit):
        self._run(edit, True)
