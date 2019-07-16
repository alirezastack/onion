from olive.toolbox import MarshmallowDateTimeField
from marshmallow import Schema, fields, EXCLUDE
from olive.consts import UTC_DATE_FORMAT
import datetime


class LeafSchema(Schema):
    class Meta:
        # Tuple or list of fields to include in the serialized result
        fields = ("_id", "title", "created_at")
        # exclude unknown fields from database on .load() call
        unknown = EXCLUDE
        datetimeformat = UTC_DATE_FORMAT

    title = fields.Str(required=True,
                       error_messages={'required': {'message': 'status required', 'code': 400}})

    # dump_only: Fields to skip during deserialization(i.e.: .load())
    created_at = MarshmallowDateTimeField(dump_only=True,
                                          default=lambda: datetime.datetime.utcnow(),
                                          allow_none=False
                                          )
