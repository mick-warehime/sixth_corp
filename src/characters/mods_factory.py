from characters.mods_base import GenericMod, ModData


def build_mod(mod: ModData) -> GenericMod:
    return GenericMod(mod.states_granted, mod.attribute_modifiers,
                      mod.abilities_granted)
