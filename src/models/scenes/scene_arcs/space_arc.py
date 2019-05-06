import random
import string

from models.characters.character_base import Character
from models.characters.character_impl import build_character
from models.characters.chassis import Chassis
from models.characters.chassis_examples import ChassisTypes
from models.characters.mods_base import build_mod
from models.characters.states import Attributes
from models.characters.subroutine_examples import repair, user_is_target, \
    direct_damage, damage_over_time
from models.characters.subroutines_base import build_subroutine
from models.combat.ai_impl import AIType
from models.scenes.decision_scene import DecisionScene, DecisionOption
from models.scenes import scene_examples


class SpaceArc(object):
    """Provides randomly generated arc scenes based on game history.

    This acts as a state machine to decide which choices are provided to the
    player at a given time.
    """

    def __init__(self, seed: int = 11):
        # We should figure out where to put the random seed
        random.seed(seed)
        self._time_until_landing = 3

    def intro(self) -> DecisionScene:
        chars = string.ascii_uppercase + string.digits
        serial_number = ''.join(random.choices(chars, k=10))
        serial_number = serial_number[:4] + '-' + serial_number[4:]
        serial_number = serial_number[:8] + '-' + serial_number[8:]
        prompt = (
            'The overhead speaker emits: "Utility Robot Mk II, serial number '
            '{}, exit hibernation mode and report to the staging area at '
            'maximum speed." You slide out of your charging pod. Your '
            'gryoscopes indicate that the "Mars or Bust" colony ship is still'
            ' in low gravity mode, so it has not yet initiated its landing '
            'sequence. You look up the content of your current mission in '
            'your long-term memory bank - help your current employer, the XXX'
            ' faction, dominate the new colony at all costs!').format(
            serial_number)
        return DecisionScene(prompt,
                             {'1': DecisionOption('Continue to staging area.',
                                                  self.staging_area)})

    def staging_area(self) -> DecisionScene:
        """The main scene where player chooses different random scenes.

        Game history and randomness is used to provide choices.
        """

        prompt = ('You enter the staging area. The wall monitor indicates that '
                  'there are {} hours until the ship lands on Mars.')

        cryo = DecisionOption('The cryo-chambers look promising.',
                              self.cryo_chambers)
        scene_2 = DecisionOption('Filler for scene 2',
                                 self.scene_2)

        return DecisionScene(prompt.format(self._time_until_landing), {
            '1': cryo, '2': scene_2})

    def _decrement_time_left(self) -> None:
        self._time_until_landing -= 1

    def cryo_chambers(self) -> DecisionScene:
        prompt = ('You enter the cryo-chambers, where all human personnel are'
                  'stored. As there are only {} hours left until landing, they'
                  'are in the process of being reanimated. Status monitors'
                  'indicate that some malfunction may be in progress, and that'
                  'the humans may expire due to lack of oxygen. A medical robot'
                  'administrator looks to be frantically administering some'
                  'fixes.').format(self._time_until_landing)

        # choices
        hack = DecisionOption('Hack the systems so that only the rival factions'
                              ' expire, and make it look like the medical robot'
                              'was at fault.', self.staging_area,
                              self._decrement_time_left)

        help = DecisionOption('Provide technical support to the medical robot.'
                              ' All human life is precious.', self.staging_area,
                              self._decrement_time_left)
        disable = DecisionOption('Attempt to disable the medical robot to '
                                 'access its encryption key.',
                                 self.staging_area, self._decrement_time_left)

        return DecisionScene(prompt, {'1': hack, '2': help, '3': disable})

    def scene_2(self) -> DecisionScene:
        return DecisionScene('Something with space unicorns',
                             {'1': DecisionOption('Back to staging area',
                                                  self.staging_area,
                                                  self._decrement_time_left)})


def medical_bot_combat():
    pass


def _heal_over_time():
    def use_fun(user: Character, target: Character) -> None:
        target.status.increment_attribute(Attributes.HEALTH, 2)

    rounds = 3
    desc = 'repair +2 for {} rounds'.format(rounds)

    return build_subroutine(use_fun, user_is_target, 1, 1, desc, rounds - 1,
                            True)


def _bone_drill():
    return damage_over_time(1, 3, 1, 1, 'bone drill')


def medical_bot(number: int) -> Character:
    """Construct a medical robot character"""

    base_mod = build_mod(subroutines_granted=[_heal_over_time(), _bone_drill()],
                         attribute_modifiers={Attributes.MAX_HEALTH: 4,
                                              Attributes.MAX_CPU: 2})
    chassis = Chassis(base_mod=base_mod)
    name = 'med_bot {}'.format(number)
    build_character(chassis, AIType.Random, name=name,
                    image_path='src/data/images/')
