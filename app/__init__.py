from flask import Flask, request
from flask_restx import Resource, Api, fields, marshal
import werkzeug.exceptions
from db.TinyDBManager import TinyDBManager, TinyDBDocumentNotFoundException


def create_app(db=TinyDBManager()):
    app = Flask(__name__)
    api = Api(
        app,
        version="1.0",
        title="TinyDB API",
        description="A simple TinyDB API",
    )
    ns = api.namespace("document", description="Document operations")

    documentModel = api.model(
        "Document",
        {
            "id": fields.Integer(
                readonly=True, description="The task unique identifier"
            ),
            "data": fields.Wildcard(
                fields.String, example={"type": "peach", "count": 7}
            ),
        },
    )

    @app.errorhandler(TinyDBDocumentNotFoundException)
    def handle_no_doc_found_exception(error):
        """Return a custom not found error message and 404 status code"""
        return {"message": "document not found"}, 404

    @ns.errorhandler(werkzeug.exceptions.BadRequest)
    def handle_bad_request(error):
        return {"message": error.description}, 400

    @app.errorhandler(werkzeug.exceptions.NotFound)
    def handle_not_found_exception(e):
        return {"message": "Resource not found"}, 404

    @ns.route("s/")
    class DocumentList(Resource):
        @ns.doc("list_documents")
        @ns.response(200, "Success", [documentModel])
        def get(self):
            """List all documents"""
            return db.getAll()

        @ns.doc("create_document")
        @ns.expect(documentModel)
        @ns.response(201, "Success")
        @ns.marshal_with(documentModel, mask="id")
        def post(self):
            """Create new document"""

            try:
                wildcard_fields = {"*": fields.Wildcard(fields.String)}
                id = db.insert(marshal(request.json["data"], wildcard_fields))
                return {"id": id}
            except KeyError:
                raise werkzeug.exceptions.BadRequest(
                    "Request body should be of required format"
                )

    @ns.route("/<int:id>")
    @ns.response(404, "Document not found")
    @ns.param("id", "The document id")
    class Document(Resource):
        """Show a single todo item and lets you delete them"""

        @ns.doc("get_doc")
        @ns.response(200, "Success", documentModel)
        def get(self, id):
            """
            Get doc

            :raises TinyDBDocumentNotFoundException: When document not found
            """
            return db.getOne(id)

        @ns.doc("delete_document")
        @ns.response(204, "Document deleted")
        def delete(self, id):
            """Delete doc"""
            db.deleteFromIds([id])
            return "", 204

        @ns.doc("update_document")
        @ns.expect(documentModel)
        @ns.response(201, "Success")
        def put(self, id):
            """
            Update doc

            :raises TinyDBDocumentNotFoundException: When document not found
            """
            db.update(id, request.json["data"])
            return "", 201

    @ns.route("s/query")
    class DocumentQuery(Resource):
        @ns.param("value", "The value to be searched for", "query")
        @ns.param("field", "The document field to be searched against", "query")
        @ns.response(200, "Success", [documentModel])
        def get(self):
            """Get records whose 'field' matches 'value'"""
            field = request.args.get("field")
            value = request.args.get("value")
            if field and value:
                return db.search(field, value)
            else:
                raise werkzeug.exceptions.BadRequest(
                    "Field and Value must be part of request params"
                )

    return app
