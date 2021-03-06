import sublime, sublime_plugin
import desktop
import os


class BaseCommand(sublime_plugin.WindowCommand):
    def root(self):
        return self.window.folders()[0]

    def settings(self):
        return sublime.load_settings('Tita.sublime-settings')

    def exec_command(self, cmd):
        command = {'cmd': cmd, 'shell': True, 'working_dir': self.root()}
        exec_args = self.settings().get('exec_args')
        exec_args.update(command)
        self.window.run_command("exec", exec_args)


class Titaclean(BaseCommand):

    def run(self, *args, **kwargs):
        sublime.status_message('Clean build directories')
        exec_command(u"titanium clean", self.root(), self.window)


class Titagenerate(BaseCommand):

    def on_done(self, text):
        sublime.status_message('Generate' + text)
        self.exec_command(u"alloy generate " + text)

    def run(self, *args, **kwargs):
        self.window.show_input_panel("alloy generate ", "", self.on_done, None, None)


class TitaCommand(BaseCommand):

    def log_level(self):
        return self.settings().get('alloy').get('logLevel')

    def android_sdk_path(self):
        return self.settings().get('android_sdk_path')

    def compile_alloy(self, device):
        self.exec_command(u"alloy compile -n --config platform=" + device)

    def build(self, device, target):
        loglevel = self.log_level()

        if ('iphone' == device or 'ipad' == device):
            cmd = u"titanium build -p ios -F %s -T %s --log-level %s" % (device, target, loglevel)
        if ('android' == device):
            androidsdkpath = self.android_sdk_path()
            cmd = u"titanium build -p %s -T %s -A %s --log-level %s" % (device, target, androidsdkpath, loglevel)
        else:
            cmd = u"titanium build -p %s --log-level %s" % (device, loglevel)

        self.exec_command(cmd)

    def run(self, device='iphone', target='', *args, **kwargs):
        self.compile_alloy(device)
        self.build(device, target)

        if ('mobileweb' == device):
            desktop.open('http://127.0.0.1:8020/index.html')
