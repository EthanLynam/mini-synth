# helper functions to change the adsr envelope
def set_attack(value, synth):
    synth.attack_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_decay(value, synth):
    synth.decay_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_sustain(value, synth):
    synth.sustain_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount

def set_release(value, synth):
    synth.release_amount = float(value)
    synth.total_duration = synth.attack_amount + synth.decay_amount + synth.sustain_amount + synth.release_amount
