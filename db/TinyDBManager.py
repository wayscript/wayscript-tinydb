from tinydb import TinyDB, Query, table


def format_record(r):
    return {"id": r.doc_id, "data": r}


def format_records(records):
    return [format_record(r) for r in records]


class TinyDBManager:
    def __init__(self, db_path="db.json") -> None:
        self.db = TinyDB(db_path)

    def insert(self, document) -> None:
        return self.db.insert(document)

    def deleteFromIds(self, ids) -> None:
        try:
            return self.db.remove(doc_ids=ids)
        except KeyError:
            raise TinyDBDocumentNotFoundException

    def getOne(self, id) -> table.Document:
        record = self.db.get(doc_id=id)
        if record:
            return format_record(record)
        else:
            raise TinyDBDocumentNotFoundException

    def getAll(self) -> list:
        return format_records(self.db.all())

    def update(self, id, document) -> int:
        try:
            return self.db.update(document, doc_ids=[id])
        except KeyError:
            raise TinyDBDocumentNotFoundException

    def search(self, field, value) -> list:
        records = self.db.search(Query()[field] == value)
        return format_records(records)


class TindyDBManagerException(Exception):
    def __init__(self, error_id="") -> None:
        self.message = f"{error_id}"
        self.error_id = error_id
        super().__init__(self.message)


class TinyDBDocumentNotFoundException(TindyDBManagerException):
    def __init__(self) -> None:
        super().__init__("doc_not_found")
