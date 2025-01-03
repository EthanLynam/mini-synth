def set_distortion_amount(value, synth):
    synth.distortion_amount = float(value)

def set_reverb_amount(value, synth):
    synth.reverb_amount = float(value)

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
    synth.num_samples = value
