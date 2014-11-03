from IoTPy.pyuper.utils import IoTPy_APIError

CAP_RESERVED = 0x0
CAP_GPIO     = 0x1
CAP_ADC      = 0x2
CAP_PWM      = 0x4
CAP_SPI      = 0x8

class IoParams:
    """
    Class describing IO pin.

    :param int capabilities: Integer describing pin capabilities. Can be a combination of CAP_CAP_RESERVED, CAP_GPIO, CAP_ADC, CAP_PWM and CAP_SPI.
    :param int pinID: Pin ID.
    :param str name: Pin alias name.
    :param list extra: Extra data for pin capabilities.
    """

    def __init__(self, capabilities, pinID, name, extra=None):
        self.capabilities = capabilities
        self.pinID = pinID
        self.pinName = name
        self.extra = extra

class IoPinout(dict):
    """
    A dictionary consisting of integer keys and :class:`IoParams` values which describe board pin mapping and capabilities.
    """

    def __init__(self, *args, **kw):
        super(IoPinout,self).__init__(*args, **kw)
        for key in self:
            if not isinstance(key, int) or not isinstance(self[key], IoParams):
                raise IoTPy_APIError("IoPinout must consist of integer keys and IoParams values.")

    def __delitem__(self, key):
        raise IoTPy_APIError("IoPinout can not be modified.")

    def __setitem__(self, key, value):
        raise IoTPy_APIError("IoPinout can not be modified.")


UPER1_PINOUT = IoPinout({
    1 : IoParams(CAP_GPIO,              0,  "PIO0_20"),
    2 : IoParams(CAP_GPIO,              1,  "PIO0_2"),
    3:  IoParams(CAP_GPIO | CAP_PWM,    2,  "PIO1_26",  [1,2]),
    4:  IoParams(CAP_GPIO,              3,  "PIO1_27"),
    5:  IoParams(CAP_GPIO | CAP_SPI,    4,  "PIO1_20",  [1,2]),  #SPI1 SCK
    6:  IoParams(CAP_RESERVED,          -1, "PIO0_4"),
    7:  IoParams(CAP_RESERVED,          -1, "PIO0_5"),
    8 : IoParams(CAP_GPIO | CAP_SPI,    5,  "PIO0_21",  [1,1]),  #SPI1 MOSI
    9 : IoParams(CAP_GPIO,              6,  "PIO1_23"),
    10 : IoParams(CAP_GPIO | CAP_PWM,   7,  "PIO1_24",  [1,0]),
    11 : IoParams(CAP_GPIO,             8,  "PIO0_7"),
    12 : IoParams(CAP_GPIO,             9,  "PIO1_28"),
    13 : IoParams(CAP_GPIO,             10, "PIO1_31"),
    14 : IoParams(CAP_GPIO | CAP_SPI,   11, "PIO1_21",  [1,0]),  #SPI1 MISO
    15 : IoParams(CAP_GPIO,             12, "PIO0_8"),
    16 : IoParams(CAP_GPIO,             13, "PIO0_9"),
    17 : IoParams(CAP_GPIO,             14, "PIO0_10"),
    18 : IoParams(CAP_GPIO,             15, "PIO1_29"),
    19 : IoParams(CAP_RESERVED,         -1, "5V"),
    20 : IoParams(CAP_RESERVED,         -1, "GND"),
    21 : IoParams(CAP_RESERVED,         -1, "GND"),
    22 : IoParams(CAP_RESERVED,         -1, "3.3V"),
    23 : IoParams(CAP_GPIO | CAP_ADC,   33, "PIO0_11",  [0]),
    24 : IoParams(CAP_GPIO | CAP_ADC,   32, "PIO0_12",  [1]),
    25 : IoParams(CAP_GPIO | CAP_ADC,   31, "PIO0_13",  [2]),
    26 : IoParams(CAP_GPIO | CAP_ADC,   30, "PIO0_14",  [3]),
    27 : IoParams(CAP_GPIO | CAP_PWM,   29, "PIO1_13",  [0,0]),
    28 : IoParams(CAP_GPIO | CAP_PWM,   28, "PIO1_14",  [0,1]),
    29 : IoParams(CAP_GPIO,             27, "PIO1_22"),
    30 : IoParams(CAP_GPIO | CAP_ADC,   26, "PIO0_15",  [4]),
    31 : IoParams(CAP_GPIO | CAP_ADC,   25, "PIO0_16",  [5]),
    32 : IoParams(CAP_GPIO | CAP_ADC,   24, "PIO0_22",  [6]),
    33 : IoParams(CAP_GPIO | CAP_ADC,   23, "PIO0_23",  [7]),
    34 : IoParams(CAP_GPIO | CAP_PWM,   22, "PIO1_15",  [0,2]),
    35 : IoParams(CAP_GPIO,             21, "PIO0_17"),
    36 : IoParams(CAP_GPIO,             20, "PIO0_18"),
    37 : IoParams(CAP_GPIO,             19, "PIO0_19"),
    38 : IoParams(CAP_GPIO,             18, "PIO0_16"),
    39 : IoParams(CAP_GPIO | CAP_PWM,   17, "PIO1_25",  [1,1]),
    40 : IoParams(CAP_GPIO,             16, "PIO1_19")
})

WEIO_PINOUT = IoPinout({
    0 : IoParams(CAP_GPIO,              20, "PIO1_13"),
    1 : IoParams(CAP_GPIO,              19, "PIO0_14"),
    2 : IoParams(CAP_GPIO,              13, "PIO0_9"),
    3 : IoParams(CAP_GPIO,              12, "PIO0_8"),
    4 : IoParams(CAP_GPIO,              14, "PIO0_10"),
    5 : IoParams(CAP_GPIO,              1,  "PIO0_2"),
    6 : IoParams(CAP_GPIO,              8,  "PIO0_7"),
    7 : IoParams(CAP_GPIO,              21, "PIO1_14"),
    8 : IoParams(CAP_GPIO,              5,  "PIO0_21"),
    9 : IoParams(CAP_GPIO,              11, "PIO1_21"),
    10: IoParams(CAP_GPIO,              4,  "PIO1_20"),
    11: IoParams(CAP_GPIO,              0,  "PIO0_20"),
    12: IoParams(CAP_GPIO,              18, "PIO0_13"),
    13: IoParams(CAP_GPIO,              16, "PIO0_11"),
    14: IoParams(CAP_GPIO,              27, "PIO1_15"),
    15: IoParams(CAP_GPIO,              6,  "PIO1_23"),
    16: IoParams(CAP_GPIO,              3,  "PIO1_27"),
    17: IoParams(CAP_GPIO,              9,  "PIO1_28"),
    18: IoParams(CAP_GPIO | CAP_PWM,    29, "PIO0_18",  [0,0]),
    19: IoParams(CAP_GPIO | CAP_PWM,    28, "PIO0_17",  [0,1]),
    20: IoParams(CAP_GPIO | CAP_PWM,    22, "PIO1_22",  [0,2]),
    21: IoParams(CAP_GPIO | CAP_PWM,    7,  "PIO1_24",  [1,0]),
    22: IoParams(CAP_GPIO | CAP_PWM,    17, "PIO0_12",  [1,1]),
    23: IoParams(CAP_GPIO | CAP_PWM,    2,  "PIO1_26",  [1,2]),
    24: IoParams(CAP_GPIO | CAP_ADC,    33, "PIO1_19",  [0]),
    25: IoParams(CAP_GPIO | CAP_ADC,    32, "PIO1_25",  [1]),
    26: IoParams(CAP_GPIO | CAP_ADC,    31, "PIO1_16",  [2]),
    27: IoParams(CAP_GPIO | CAP_ADC,    30, "PIO0_19",  [3]),
    28: IoParams(CAP_GPIO | CAP_ADC,    26, "PIO0_23",  [4]),
    29: IoParams(CAP_GPIO | CAP_ADC,    25, "PIO0_22",  [5]),
    30: IoParams(CAP_GPIO | CAP_ADC,    24, "PIO0_16",  [6]),
    31: IoParams(CAP_GPIO | CAP_ADC,    23, "PIO0_15",  [7])
})