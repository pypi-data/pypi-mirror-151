from flask import request
from flask_restx import Resource, fields, reqparse
from ...db.db_connection import database_access
from ...namespace import api
from ...response_helper import get_response
import logging
import json
from bson import json_util
import re


check_list_add = api.model("CheckListAdd", {
    "trip_id": fields.String,
    "vehicle_id": fields.String,
    "transporter_name": fields.String,
    "stage": fields.String,
    "check_status": fields.String,
    "user": fields.String,
    "date_of_submission": fields.String,
})


delete_checklist = reqparse.RequestParser()
delete_checklist.add_argument("trip_id", type=str, required=True, help="Trip ID")

get_checklist = reqparse.RequestParser()
get_checklist.add_argument("page_no", type=int, required=True, help="Page number")
get_checklist.add_argument("page_limit", type=int, required=True, help="limit ")


class CheckListApproval(Resource):
    @api.expect(get_checklist)
    def get(self):
        try:
            database_connection = database_access()
            checklist_collection = database_connection["dms_check_list"]
            data = checklist_collection.find()
            page_no = request.args.get("page_no")
            page_limit = request.args.get("page_limit")
            if len(list(data)):
                data = checklist_collection.find().skip(int(page_limit) * (int(page_no) - 1)). limit(int(page_limit))
                _response = get_response(200)
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Find Checklist History'
            logging.error(e)
            return _response

    @api.expect(check_list_add)
    def post(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            checklist_collection = database_connection["dms_check_list"]
            if not checklist_collection.find_one({"trip_id": args["trip_id"]}):
                checklist_collection.insert_one(args)
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.info(get_response(409))
                return get_response(409)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Store checklist'
            logging.error(e)
            return _response

    @api.expect(check_list_add, validate=True)
    def put(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            violation_collection = database_connection["dms_check_list"]
            if violation_collection.find_one({"trip_id": args["trip_id"]}):
                violation_collection.update_one({"trip_id": args["trip_id"]}, {
                    '$set': args})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update CheckList'
            logging.error(e)
            return _response
#

    @api.expect(delete_checklist, validate=True)
    def delete(self):
        try:
            database_connection = database_access()
            checklist_collection = database_connection["dms_check_list"]
            trip_id = request.args.get("trip_id")
            if checklist_collection.find_one({"trip_id": trip_id}):
                checklist_collection.delete_one({"trip_id": trip_id})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Delete Checklist'
            logging.error(e)
            return _response


status_update = api.model("StatusUpdate", {
    "trip_id": fields.String,
    "check_status": fields.String,
})


class CheckListCheck(Resource):
    def get(self):
        try:
            database_connection = database_access()
            checklist_collection = database_connection["dms_check_list"]
            check_status = re.compile("failed", re.IGNORECASE)
            data = checklist_collection.find({"check_status": check_status})
            if len(list(data)):
                data = checklist_collection.find({"check_status": check_status})
                _response = get_response(200)
                _response["data"] = json.loads(json_util.dumps(data))
                return _response
            else:
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Find Checklist History'
            logging.error(e)
            return _response

    @api.expect(status_update)
    def put(self):
        args = request.get_json()
        try:
            database_connection = database_access()
            violation_collection = database_connection["dms_check_list"]
            if violation_collection.find_one({"trip_id": args["trip_id"]}):
                violation_collection.update_one({"trip_id": args["trip_id"]}, {
                    '$set': {"check_status": args["check_status"]}})
                logging.info(get_response(200))
                return get_response(200)
            else:
                logging.error(get_response(404))
                return get_response(404)
        except Exception as e:
            _response = get_response(404)
            _response['message'] = 'Failed to Update CheckList'
            logging.error(e)
            return _response