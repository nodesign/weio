from IoTPy.pyuper.interrupt import Interrupt

class RotaryEncoder:

    FORWARD = 1
    BACKWARD = -1

    _backward_states = [
        [[0, 0], [1, 0], [1, 1]],  # missing 1st
        [[0, 1], [1, 0], [1, 1]],  # missing 2nd
        [[0, 1], [0, 0], [1, 1]],  # missing 3rd
        [[0, 1], [0, 0], [1, 0]],  # missing 4th
    ]

    _forward_states = [
        [[0, 0], [0, 1], [1, 1]],  # missing 1st or perfect
        [[1, 0], [0, 1], [1, 1]],  # missing 2nd
        [[1, 0], [0, 0], [1, 1]],  # missing 3rd
        [[1, 0], [0, 0], [0, 1]],  # missing 4th
    ]

    _null_state = [[-1, -1], [-1, -1], [-1, -1]]
    
    def __init__(self, chan0, chan1, callback=None):
        #obj = {'previous_states': list(self._null_state), 'position': 0}

        self._previous_states = list(self._null_state)
        self.position = 0

        self._chan0 = chan0
        self._chan1 = chan1

        self._user_callback = callback

        self._id0 = chan0.attach(Interrupt.EDGE_CHANGE, self.call_back, None, 3)
        self._id1 = chan1.attach(Interrupt.EDGE_CHANGE, self.call_back, None, 3)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def call_back(self, event, obj):
        pins = event['values']
        pin1 = (pins >> self._id0) & 0x01
        pin2 = (pins >> self._id1) & 0x01
        
        if [pin1, pin2] != self._previous_states[2]:
            self._previous_states[0:2] = self._previous_states[1:3]
            self._previous_states[2] = [pin1, pin2]

            if self._previous_states in self._forward_states:
                self.position += 1
                self._previous_states = list(self._null_state)
                if self._user_callback:
                    self._user_callback(RotaryEncoder.FORWARD, self.position)
            elif self._previous_states in self._backward_states:
                self.position -= 1
                self._previous_states = list(self._null_state)
                if self._user_callback:
                    self._user_callback(RotaryEncoder.BACKWARD, self.position)