class Car(object):

    def __init__(self):
        self.color = 'red'
        self.speed = 0

    def _accelerate(self):
        if self.speed < 100:
            self.speed += 1
        else:
            self.crash()

    def _decelerate(self):
        if self.speed > 0:
            self.speed -= 1

    def stop(self):
        self.speed = 0

    def crash(self):
        self.stop()
        self.destroyed = True
