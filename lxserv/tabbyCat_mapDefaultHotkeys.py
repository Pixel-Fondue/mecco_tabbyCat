# python

import lx, lxu, modo
from tabbyCat import CommanderClass

HOTKEYS = [
    {
        "contexts":[
            [".global", "(stateless)", ".anywhere", "(contextless)", "poly.convert face subpatch true"]
        ],
        "key":"tab",
        "command":"tabbyCat.tab",
        "name":"TabbyCat Tab"
    }
]

class CommandClass(CommanderClass):
    def commander_arguments(self):
        args = []
        for n, hotkey in enumerate(HOTKEYS):
            args.append({
                'name':str(n),
                'label':"%s \x03(c:25132927)(%s)" % (hotkey['name'], hotkey['key']),
                'datatype':'boolean',
                'default':True
            })
        return args

    def commander_execute(self, msg, flags):
        counter = 0
        for n, hotkey in enumerate(HOTKEYS):
            if not self.commander_arg_value(n):
                continue
            command = hotkey["command"]
            key = hotkey["key"]

            for context_list in hotkey["contexts"]:
                mapping = context_list[0]
                state = context_list[1]
                region = context_list[2]
                context = context_list[3]

                try:
                    lx.eval('!cmds.mapKey {%s} {%s} {%s} {%s} {%s} {%s}' % (key, command, mapping, state, region, context))
                except:
                    lx.out("Could not set '%s' to '%s'." % (command, key))

            counter += 1

        modo.dialogs.alert("Mapped TabbyCat Hotkeys", "Mapped %s TabbyCat hotkeys." % counter)

lx.bless(CommandClass, "tabbyCat.mapDefaultHotkeys")


class RemoveCommandClass(CommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in HOTKEYS:
            key = hotkey["key"]

            for context_list in hotkey["contexts"]:
                mapping = context_list[0]
                state = context_list[1]
                region = context_list[2]
                context = context_list[3]
                default = context_list[4]

                if default is None:
                    try:
                        lx.eval('!cmds.clearKey {%s} {%s} {%s} {%s} {%s}' % (key, mapping, state, region, context))
                    except:
                        lx.out("Could not clear mapping for '%s'." % key)
                else:
                    try:
                        lx.eval('!cmds.mapKey {%s} {%s} {%s} {%s} {%s} {%s}' % (key, default, mapping, state, region, context))
                    except:
                        lx.out("Could not set '%s' to '%s'." % (default, key))

        modo.dialogs.alert("Reverted TabbyCat Hotkeys", "Reverted %s TabbyCat hotkeys to defaults." % len(HOTKEYS))

lx.bless(RemoveCommandClass, "tabbyCat.unmapDefaultHotkeys")
