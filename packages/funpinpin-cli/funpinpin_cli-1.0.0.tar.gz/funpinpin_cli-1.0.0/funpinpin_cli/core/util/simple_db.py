"""Simple key-value db."""
import os
import tempfile
import pickledb


class SimpleDB(object):
    """DB definition."""

    def __init__(self, db_path, auto_dump=True):
        self.db_path = db_path
        try:
            self.db = pickledb.load(db_path, auto_dump)
        except Exception as e:
            print(e)

    def get(self, key):
        return self.db.get(key)

    def set(self, key, value):
        self.db.set(key, value)

    def delete(self, key):
        self.db.rem(key)


db_path = os.path.join(
    os.path.realpath(tempfile.gettempdir()), "funpinpin_db"
)
db = SimpleDB(db_path)
