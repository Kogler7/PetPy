from petpy.utils.parser import CommandParser, ActParser, ObjParser, CommandExecutor
from petpy.utils.text import EditableText


class CommandHandler:
    def __init__(
            self,
            console,
            update_command: callable,
            update_tooltip: callable,
            on_refresh: callable,
    ):
        from petpy.console import PetPyConsole
        self.console: PetPyConsole = console
        self.parser = None
        self.update_command = update_command
        self.update_tooltip = update_tooltip
        self.on_refresh = on_refresh
        self.setupParser()

    def command_exit(self):
        pass

    def command_page_task(self, objs, args):
        pass

    def command_page_log(self, objs, args):
        pass

    def command_task_pause(self, objs, args):
        pass

    def command_task_resume(self, objs, args):
        pass

    def command_task_kill(self, objs, args):
        pass

    def command_log_save(self, objs, args):
        pass

    def command_log_clear(self, objs, args):
        pass

    def command_log_max(self, objs, args):
        pass

    def setupParser(self):
        self.parser = CommandParser({
            'exit': CommandExecutor(self.command_exit, 'none'),
            'page': ActParser({
                'task': CommandExecutor(self.command_page_task, 'none'),
                'log': CommandExecutor(self.command_page_log, 'none'),
            }),
            'task': ActParser({
                'pause': ObjParser(
                    CommandExecutor(self.command_task_pause, 'none')
                ),
                'resume': ObjParser(
                    CommandExecutor(self.command_task_resume, 'none')
                ),
                'kill': ObjParser(
                    CommandExecutor(self.command_task_kill, 'none')
                ),
            }),
            'log': ActParser({
                'save': ObjParser(
                    CommandExecutor(self.command_log_save, 'required')
                ),
                'clear': ObjParser(
                    CommandExecutor(self.command_log_clear, 'none')
                ),
                'max': CommandExecutor(self.command_log_max, 'required'),
            }),
        })

    def handle(self, cmd_text: EditableText):
        cmd_str = cmd_text.get_text()
        try:
            self.parser.parse(cmd_str.split(' '))
        except Exception as e:
            self.update_tooltip(str(e), cmd_str.split(' '))
        self.update_command(cmd_str, cmd_text.cursor)
        self.on_refresh()

    def help(self, cmd_text: EditableText):
        cmd_str = cmd_text.get_text()
        self.update_command(cmd_str, cmd_text.cursor)
        strs = cmd_str.split(' ')
        tip = self.parser.help(strs)
        self.update_tooltip(tip, strs)
        self.on_refresh()
