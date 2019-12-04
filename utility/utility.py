import json
import math
import os
import sys
from game.serializable import Serializable

# Helper class for utility functions
class Utility:
    @staticmethod
    def debug(src, msg):
        print("[%s] %s" % (src, msg))

    @staticmethod
    def round(num):
        sign = -1 if num < 0 else 1
        num = abs(num)
        if num % 1 >= 0.5:
            return sign*math.ceil(num)
        else:
            return sign*math.floor(num)

    # Store a world into a savefile
    @staticmethod
    def save(world):
        name = world.name
        if not os.path.exists("saves"):
            os.makedirs("saves")

        file = open(f"saves/{name}.world", "w")
        file.write(Serializable.serialize(world))
        file.close()

    @staticmethod
    def loadWorlds():
        ls = []
        if os.path.exists("saves"):
            for i in range(1, 4):
                try:
                    world = Utility.loadWorld(f"saves/World {i}.world")
                except:
                    world = None
                ls.append(world)
        return ls

    @staticmethod
    def loadWorld(fileName):
        from game.world.world import World
        if os.path.exists(fileName):
            with open(fileName, "r") as file:
                content = file.read()
                content = json.loads(content)
                world = World.fromJson(content)
                return world
        return None

    @staticmethod
    def deleteWorld(index):
        fn = f"saves/World {index}.world"
        if os.path.exists(fn):
            os.remove(fn)
        else:
            print("File does not exist:", fn)
