class ToolManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.tools = {}
        self.active_tool = None

    def register_tool(self, name, tool):
        self.tools[name] = tool

    def set_tool(self, name):
        if self.active_tool:
            self.active_tool.deactivate()
        tool = self.tools.get(name)
        if tool:
            self.active_tool = tool
            self.active_tool.activate()

    def cancel(self):
        if self.active_tool:
            self.active_tool.cancel(None)

    def redraw(self):
        if self.active_tool and hasattr(self.active_tool, "redraw"):
            self.active_tool.redraw()
