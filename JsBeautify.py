import os, re, sublime, sublime_plugin, sys

# this import code taken from the JsFormat plugin by Davis Clark (https://github.com/jdc0589/JsFormat)
# craziness to get jsbeautifier.unpackers to actually import
# with sublime's weird hackery of the path and module loading
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "jsbeaufifier"))
sys.path.append(os.path.join(directory, "jsbeautifier", "unpackers"))

# if you don't explicitly import jsbeautifier.unpackers here things will bomb out,
# even though we don't use it directly.....
import jsbeautifier, jsbeautifier.unpackers

s = sublime.load_settings("JsBeautify.sublime-settings")

class JsBeautifyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.save()
		self.beautify(edit)

	def get_options(self):
		settings = self.view.settings()

		opts = jsbeautifier.default_options()
		opts.brace_style = s.get("brace_style", "collapse")
		opts.indent_char = " " if settings.get("translate_tabs_to_spaces") else "\t"
		opts.indent_size = int(settings.get("tab_size")) if opts.indent_char == " " else 1
		opts.indent_with_tabs = s.get("indent_with_tabs", True)
		opts.jslint_happy = s.get("jslint_happy", False)
		opts.keep_array_indentation = s.get("keep_array_indentation", False)
		opts.keep_function_indentation = s.get("keep_function_indentation", False)
		opts.max_preserve_newlines = s.get("max_preserve_newlines", 2)
		opts.preserve_newlines = s.get("preserve_newlines", True)
		opts.space_before_line_starters = s.get("space_before_line_starters", False)
		opts.unescape_strings = False

		return opts

	def save(self):
		self.view.run_command("save")

	def beautify(self, edit):
		opts = self.get_options()

		selection = self.view.sel()[0]

		# do formatting and replacement
		replaceRegion = None

		# formatting a selection/highlighted area
		if(len(selection) > 0):
			replaceRegion = selection
		# formatting the entire file
		else:
			replaceRegion = sublime.Region(0, self.view.size())
		
		unformatted = self.view.substr(replaceRegion)
		formatted = jsbeautifier.beautify(unformatted, opts)

		if len(formatted) > 0:
			self.view.replace(edit, replaceRegion, formatted)
			sublime.set_timeout(self.save, 100)
