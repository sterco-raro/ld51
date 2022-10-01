from pygame.time import get_ticks


# -------------------------------------------------------------------------------------------------


class Timer():
    """Custom pygame timer. Slightly modified version of ClearCode Sproutland tutorial code (yt)"""

    def __init__(self, duration, callback=None):
        self.duration = duration
        self.callback = callback
        self.start_time = 0
        self._active = False

    @property
    def active(self):
        return self._active

    @property
    def value(self):
        """Return current timer value in seconds"""
        if not self.active:
            return 0
        return ( get_ticks() - self.start_time ) // 1000

    def activate(self):
        self._active = True
        self.start_time = get_ticks()

    def deactivate(self):
        self._active = False
        self.start_time = 0

    def update(self):
        if not self._active: return
        current_time = get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.callback and self.start_time != 0:
                self.callback()
            self.deactivate()
