from typing import Union

from pydantic import Field

from model.base import RoleBaseDocument, BaseDocument


class RoleTest(RoleBaseDocument):
    id: int = Field(..., primary_field=True, alias='id')

    class Settings:
        name = "roles"
        database = "test_data"


class RoleWbsite(RoleBaseDocument):
    id: int = Field(..., primary_field=True, alias='id')

    class Settings:
        name = "roles"
        database = "wbsite"


class Spur(BaseDocument):
    id: int = Field(..., primary_field=True, alias='id')

    class Settings:
        name = "spur"
        database = "test_data"


class AntCalibCrossFreq(BaseDocument):
    id: int = Field(..., primary_field=True, alias='id')

    class Settings:
        name = "ant_calib_cross_freq"
        database = "test_data"


class Calibration(BaseDocument):
    id: int = Field(..., primary_field=True, alias='id')

    class Settings:
        name = "calibration"
        database = "test_data"


class Eirp(BaseDocument):
    id: int = Field(..., primary_field=True, alias='id')

    class Settings:
        name = "eirp"
        database = "test_data"


class Pattern(BaseDocument):
    id: int = Field(..., primary_field=True, alias='id')

    class Settings:
        name = "pattern"
        database = "test_data"
