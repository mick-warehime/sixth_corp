import random
import string

from models.scenes.decision_scene import DecisionScene, DecisionOption
from models.scenes import scene_examples

seed = 11


def intro():
    random.seed(seed)

    chars = string.ascii_uppercase + string.digits
    serial_number = ''.join(random.choices(chars, k=10))
    serial_number = serial_number[:4] + '-' + serial_number[4:]
    serial_number = serial_number[:8] + '-' + serial_number[8:]
    prompt = ('The overhead speaker emits: "Utility Robot Mk II, serial number '
              '{}, exit hibernation mode and report to the staging area at '
              'maximum speed." You slide out of your charging pod. Your '
              'gryoscopes indicate that the "Mars or Bust" colony ship is still'
              ' in low gravity mode, so it has not yet initiated the landing '
              'sequence. Your long-term memory reminds you of your current '
              'mission - help your current employer, the XXX faction, dominate '
              'the new colony at all costs!').format(serial_number)
    return DecisionScene(prompt,
                         {'1': DecisionOption('Continue to staging area.',
                                              scene_examples.pre_start_scene)})
