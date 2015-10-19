from IoTPy.pyuper.utils import errmsg, IoTPy_APIError

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
                errmsg("UPER API: IoPinout must consist of integer keys and IoParams values.")

    def __delitem__(self, key):
        errmsg("UPER API: IoPinout can not be modified.")

    def __setitem__(self, key, value):
        errmsg("UPER API: IoPinout can not be modified.")

# Actual WeIO pinout
WEIO_PINOUT = IoPinout({
    0 : IoParams(CAP_GPIO,              20, "PIO0_18"),
    1 : IoParams(CAP_GPIO,              19, "PIO0_19"),
    2 : IoParams(CAP_GPIO | CAP_SPI,    13, "PIO0_9"),  #SPI0 MOSI
    3 : IoParams(CAP_GPIO | CAP_SPI,    12, "PIO0_8"),  #SPI0 MISO
    4 : IoParams(CAP_GPIO | CAP_SPI,    14, "PIO0_10"), #SPI0 SCK
    5 : IoParams(CAP_GPIO,              1,  "PIO0_2"),
    6 : IoParams(CAP_GPIO,              8,  "PIO0_7"),
    7 : IoParams(CAP_GPIO,              21, "PIO0_17"),
    8 : IoParams(CAP_GPIO,              0,  "PIO0_20"),
    9 : IoParams(CAP_GPIO,              18, "PIO1_16"),
    10: IoParams(CAP_GPIO | CAP_SPI,    5,  "PIO0_21"), #SPI1 MOSI
    11: IoParams(CAP_GPIO | CAP_SPI,    11, "PIO1_21"), #SPI1 MISO
    12: IoParams(CAP_GPIO | CAP_SPI,    4,  "PIO1_20"), #SPI1 SCK
    13: IoParams(CAP_GPIO,              16, "PIO1_19"),
    14: IoParams(CAP_GPIO,              27, "PIO1_22"),
    15: IoParams(CAP_GPIO,              6,  "PIO1_23"),
    16: IoParams(CAP_GPIO,              3,  "PIO1_27"),
    17: IoParams(CAP_GPIO,              9,  "PIO1_28"),
    18: IoParams(CAP_GPIO | CAP_PWM,    29, "PIO1_13",  [0,0]),
    19: IoParams(CAP_GPIO | CAP_PWM,    28, "PIO1_14",  [0,1]),
    20: IoParams(CAP_GPIO | CAP_PWM,    22, "PIO1_15",  [0,2]),
    21: IoParams(CAP_GPIO | CAP_PWM,    7,  "PIO1_24",  [1,0]),
    22: IoParams(CAP_GPIO | CAP_PWM,    17, "PIO1_25",  [1,1]),
    23: IoParams(CAP_GPIO | CAP_PWM,    2,  "PIO1_26",  [1,2]),
    24: IoParams(CAP_GPIO | CAP_ADC,    33, "PIO0_11",  [0]),
    25: IoParams(CAP_GPIO | CAP_ADC,    32, "PIO0_12",  [1]),
    26: IoParams(CAP_GPIO | CAP_ADC,    31, "PIO0_13",  [2]),
    27: IoParams(CAP_GPIO | CAP_ADC,    30, "PIO0_14",  [3]),
    28: IoParams(CAP_GPIO | CAP_ADC,    26, "PIO0_15",  [4]),
    29: IoParams(CAP_GPIO | CAP_ADC,    25, "PIO0_16",  [5]),
    30: IoParams(CAP_GPIO | CAP_ADC,    24, "PIO0_22",  [6]),
    31: IoParams(CAP_GPIO | CAP_ADC,    23, "PIO0_23",  [7])
})

# Pre-production boards have a different pinout (pin 8 to 12)
# This mapping handle these old boards. By default, the 
# production pinout is selected. To switch to the 'old' pinout,
# change line 8 of weio.py this way :
# --- IoBoard.__init__(self, WEIO_PINOUT, serial_port)
# +++ IoBoard.__init__(self, WEIO_PINOUT_OLD, serial_port)
# and restart the server with the command 
# /etc/init.d/weio_run restart
WEIO_PINOUT_OLD = IoPinout({
    0 : IoParams(CAP_GPIO,              20, "PIO0_18"),
    1 : IoParams(CAP_GPIO,              19, "PIO0_19"),
    2 : IoParams(CAP_GPIO | CAP_SPI,    13, "PIO0_9"),  #SPI0 MOSI
    3 : IoParams(CAP_GPIO | CAP_SPI,    12, "PIO0_8"),  #SPI0 MISO
    4 : IoParams(CAP_GPIO | CAP_SPI,    14, "PIO0_10"), #SPI0 SCK
    5 : IoParams(CAP_GPIO,              1,  "PIO0_2"),
    6 : IoParams(CAP_GPIO,              8,  "PIO0_7"),
    7 : IoParams(CAP_GPIO,              21, "PIO0_17"),
    8 : IoParams(CAP_GPIO | CAP_SPI,    5,  "PIO0_21"), #SPI1 MOSI
    9 : IoParams(CAP_GPIO | CAP_SPI,    11, "PIO1_21"), #SPI1 MISO
    10: IoParams(CAP_GPIO | CAP_SPI,    4,  "PIO1_20"), #SPI1 SCK
    11: IoParams(CAP_GPIO,              0,  "PIO0_20"),
    12: IoParams(CAP_GPIO,              18, "PIO1_16"),
    13: IoParams(CAP_GPIO,              16, "PIO1_19"),
    14: IoParams(CAP_GPIO,              27, "PIO1_22"),
    15: IoParams(CAP_GPIO,              6,  "PIO1_23"),
    16: IoParams(CAP_GPIO,              3,  "PIO1_27"),
    17: IoParams(CAP_GPIO,              9,  "PIO1_28"),
    18: IoParams(CAP_GPIO | CAP_PWM,    29, "PIO1_13",  [0,0]),
    19: IoParams(CAP_GPIO | CAP_PWM,    28, "PIO1_14",  [0,1]),
    20: IoParams(CAP_GPIO | CAP_PWM,    22, "PIO1_15",  [0,2]),
    21: IoParams(CAP_GPIO | CAP_PWM,    7,  "PIO1_24",  [1,0]),
    22: IoParams(CAP_GPIO | CAP_PWM,    17, "PIO1_25",  [1,1]),
    23: IoParams(CAP_GPIO | CAP_PWM,    2,  "PIO1_26",  [1,2]),
    24: IoParams(CAP_GPIO | CAP_ADC,    33, "PIO0_11",  [0]),
    25: IoParams(CAP_GPIO | CAP_ADC,    32, "PIO0_12",  [1]),
    26: IoParams(CAP_GPIO | CAP_ADC,    31, "PIO0_13",  [2]),
    27: IoParams(CAP_GPIO | CAP_ADC,    30, "PIO0_14",  [3]),
    28: IoParams(CAP_GPIO | CAP_ADC,    26, "PIO0_15",  [4]),
    29: IoParams(CAP_GPIO | CAP_ADC,    25, "PIO0_16",  [5]),
    30: IoParams(CAP_GPIO | CAP_ADC,    24, "PIO0_22",  [6]),
    31: IoParams(CAP_GPIO | CAP_ADC,    23, "PIO0_23",  [7])
})
