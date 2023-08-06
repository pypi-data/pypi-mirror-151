from flask import request
from flask_restx import Resource, fields, reqparse
from ...db.db_connection import database_access
from ...namespace import api
from ...response_helper import get_response
import logging
import json
from bson import json_util
from bson.objectid import ObjectId

delete_checklist_master = reqparse.RequestParser()
delete_checklist_master.add_argument("_id", type=str, required=True)

post_checklist_master = api.model("CheckListMasterAdd", {
	"stages": fields.Raw(
		[],
		required="true",
		example=[
			{
				"applicable_movement": [
					{
						"value": "inbound",
						"label": "Inbound",
					}
				],
				"enable": "enable",
				"applicable_stage": "yard1",
				"mandatory": "yes",
			},
			{
				"applicable_movement": [
					{
						"value": "outbound",
						"label": "Outbound",
					}
				],
				"enable": "enable",
				"applicable_stage": "gate1",
				"mandatory": "no",
			},
		]
	),
	"cheklist_details": fields.Raw(
		[],
		required="true",
		example=[
			{
				"applicable_movement": [
					{
						"value": "inbound",
						"label": "Inbound"
					}
				],
				"enable": "enable",
				"applicable_stage": "yard1",
				"mandatory": "yes"
			},
			{
				"applicable_movement": [
					{
						"value": "outbound",
						"label": "Outbound"
					}
				],
				"enable": "enable",
				"applicable_stage": "gate1",
				"mandatory": "no"
			},
		])
})

put_checklist_master = api.model("CheckListMasterUpdate", {
	"_id": fields.String,
	"stages": fields.Raw(
		[],
		required="true",
		example=[
			{
				"applicable_movement": [
					{
						"value": "inbound",
						"label": "Inbound",
					}
				],
				"enable": "enable",
				"applicable_stage": "yard1",
				"mandatory": "yes",
			},
			{
				"applicable_movement": [
					{
						"value": "outbound",
						"label": "Outbound",
					}
				],
				"enable": "enable",
				"applicable_stage": "gate1",
				"mandatory": "no",
			},
		]
	),
	"checklist_details": fields.Raw(
		[],
		required="true",
		example=[
			{
				"applicable_movement": [
					{
						"value": "inbound",
						"label": "Inbound"
					}
				],
				"enable": "enable",
				"applicable_stage": "yard1",
				"mandatory": "yes"
			},
			{
				"applicable_movement": [
					{
						"value": "outbound",
						"label": "Outbound"
					}
				],
				"enable": "enable",
				"applicable_stage": "gate1",
				"mandatory": "no"
			},
		])
})

get_checklist_master = reqparse.RequestParser()
get_checklist_master.add_argument("page_no", type=int, required=True, help="Page number")
get_checklist_master.add_argument("page_limit", type=int, required=True, help="limit ")


class CheckListMaster(Resource):
	@api.expect(get_checklist_master)
	def get(self):
		try:
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			data = checklist_master_collection.find()
			count = checklist_master_collection.count_documents({})
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			if len(list(data)):
				data = checklist_master_collection.find().skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				_response["count"] = count
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Checklist Data'
			logging.error(e)
			return _response

	@api.expect(post_checklist_master)
	def post(self):
		try:
			args = request.get_json()
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			checklist_master_collection.insert_one(args)
			logging.info(get_response(200))
			return get_response(200)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Checklist Data'
			logging.error(e)
			return _response

	@api.expect(put_checklist_master)
	def put(self):
		try:
			args = request.get_json()
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			data = checklist_master_collection.find_one({"_id": ObjectId(args["_id"])})
			if data:
				checklist_master_collection.update_one(
					{"_id": ObjectId(args["_id"])},
					{'$set': {"stages": args["stages"], "checklist_details": args["checklist_details"]}})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Update Checklist Data'
			logging.error(e)
			return _response

	@api.expect(delete_checklist_master)
	def delete(self):
		try:
			_id = request.args.get("_id")
			database_connection = database_access()
			checklist_master_collection = database_connection["dms_checklist_master"]
			data = checklist_master_collection.find_one({"_id": ObjectId(_id)})
			if data:
				checklist_master_collection.delete_one({"_id": ObjectId(_id)})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Delete checklist data'
			logging.error(e)
			return _response
