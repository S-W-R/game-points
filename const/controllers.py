from enum import Enum
import controllers.controllers as c


class ControllerType(Enum):
    player = c.PlayerController()
    randomAI = c.RandomAI()
    simpleAI = c.SimpleAI()


CONTROLLER_FROM_NAME = {i.value.name: i.value for i in ControllerType}
