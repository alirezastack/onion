from olive.store.cache_wrapper import CacheWrapper
from olive.exc import SaveError, InvalidObjectId, CacheNotFound, DocumentNotFound
from onion.core.models.leaf import LeafSchema
from bson import ObjectId
import traceback
import bson


class LeafStore:
    def __init__(self, db, app):
        self.app = app
        self.db = db
        self.leaf_schema = LeafSchema(exclude_none_id=True)
        self.cache_key = 'ONION:LEAF:{}'
        self.cache_wrapper = CacheWrapper(self.app, self.cache_key)

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

    def get(self, leaf_id):
        try:
            leaf_doc = self.cache_wrapper.get_cache(leaf_id)
        except CacheNotFound:
            self.app.log.debug('reading directly from database by id {}'.format(leaf_id))
            leaf_doc = self.db.find_one({'_id': leaf_id}, {'created_at': 0, 'updated_at': 0})
            if not leaf_doc:
                raise DocumentNotFound("Document with _id {} not found!".format(leaf_id))

            leaf_doc['_id'] = str(leaf_doc['_id'])
            self.cache_wrapper.write_cache(leaf_id, leaf_doc)

        clean_data = self.leaf_schema.load(leaf_doc)
        self.app.log.info('fetched leaf:\r\n{}'.format(clean_data))

        return clean_data
