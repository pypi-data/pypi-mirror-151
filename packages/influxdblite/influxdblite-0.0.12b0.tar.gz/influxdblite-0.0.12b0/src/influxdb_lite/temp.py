from influxdb_lite.measurement import Measurement
from influxdb_lite.attributes import Tag, Field


class SomeMeasure(Measurement):
    first_tag = Tag()
    second_tag = Tag()
    first_fld = Field()
    second_fld = Field()
