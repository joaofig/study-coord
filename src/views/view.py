from viewmodels.view_model import ViewModel


class View:
    def __init__(self, vm: ViewModel):
        self.vm = vm
        self.vm.register(self._handle_notification)

    def _handle_notification(self, action: str, **kwargs):
        """Handle notifications from the ViewModel"""
        # This method can be overridden in subclasses to handle notifications
        pass

    async def command(self, cmd: str, **kwargs):
        """Send a command to the ViewModel"""
        result = await self.vm.message(cmd, **kwargs)
        return result
