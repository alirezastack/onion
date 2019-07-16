from onion.core.models.leaf import LeafSchema
from olive.exc import SaveError, InvalidObjectId
from bson import ObjectId
import traceback
import bson


class LeafStore:
    def __init__(self, db, app):
        self.app = app
        self.db = db
        self.leaf_schema = LeafSchema()

    def save(self, data):
        # raise validation error on invalid data
        self.leaf_schema.load(data)
        clean_data = self.leaf_schema.dump(data)
        if not clean_data:
            self.app.log.error('empty leaf payload cannot be saved.')
            raise SaveError

        self.app.log.debug('saving clean onion leaf:\n{}'.format(clean_data))
        leaf_id = self.db.save(clean_data)
        return str(leaf_id)

    def get_question_by_id(self, leaf_id):
        try:
            leaf_id = ObjectId(leaf_id)
        except bson.errors.InvalidId:
            self.app.log.error(traceback.format_exc())
            raise InvalidObjectId

        self.app.log.debug('getting leaf by ID: {}'.format(leaf_id))
        leaf_doc = self.db.find_one({'_id': leaf_id}, {'created_at': 0})
        clean_data = self.leaf_schema.load(leaf_doc)
        self.app.log.info('fetched leaf:\r\n{}'.format(clean_data))
        return clean_data
