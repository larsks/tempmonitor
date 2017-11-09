import gc
import machine


def reset():
    machine.reset()


gc.collect()
