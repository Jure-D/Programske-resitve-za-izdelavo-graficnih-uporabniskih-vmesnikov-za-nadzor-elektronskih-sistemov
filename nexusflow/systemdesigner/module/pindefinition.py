from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class Miscellaneous:
    dac_range: float
    adc_range: float
    disable_powerdrop: bool


@dataclass(kw_only=True)
class Alarm:
    enable: bool
    above: int  # 0 = below, 1 = above
    warning_value: float
    interlock_value: float

    def __post_init__(self):
        if self.warning_value is None:
            self.warning_value = 0.0
        if self.interlock_value is None:
            self.interlock_value = 0.0


@dataclass(kw_only=True)
class Exponential:
    enable: bool
    B: float
    R0: float
    T0: float

    def __post_init__(self):
        if self.B is None:
            self.B = 0.0
        if self.R0 is None:
            self.R0 = 0.0
        if self.T0 is None:
            self.T0 = 0.0


@dataclass(kw_only=True)
class Value:
    min: float
    max: float
    initial: float
    enable_initial: bool


@dataclass(kw_only=True)
class Gui:
    display: bool
    column: int = 0
    row: int = 0
    display_type: str = ""  # int, float, str, bool, list, path,...
    display_direction: str = ""  # input / output

    def __post_init__(self):
        if self.column is None:
            self.column = 0
        if self.row is None:
            self.row = 0


@dataclass(kw_only=True)
class ConversionCoefficients:
    k: float
    C: float


@dataclass(kw_only=True)
class PinDefinition:
    id: str
    function: str
    name: str
    unit: str
    main_gui: Gui
    value: Value
    important_gui: Gui
    active_low: bool
    miscellaneous: Miscellaneous
    conversion_coefficients: Optional[ConversionCoefficients] = None
    exponential: Optional[Exponential] = None
    alarm: Optional[Alarm] = None
