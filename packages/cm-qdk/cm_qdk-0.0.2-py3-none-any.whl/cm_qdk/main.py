from qdk.main import QDK


class CMQDK(QDK):
    def zoom_app(self):
        self.execute_method('zoom_app')

    def reboot(self):
        self.execute_method('reboot')

    def close_app(self):
        self.execute_method('close_app')
