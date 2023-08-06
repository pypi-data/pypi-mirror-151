from flask import request
from flask_restx import Resource, fields, reqparse
from ...db.db_connection import database_access
from ...namespace import api
import logging
from ...response_helper import get_response
import json
from bson import json_util
import re

post_vehicle_details = api.model("VehicleDetails", {
	"vehicle_no": fields.String,
	"plant_code": fields.String,
	"transporter_name": fields.String,
	"transporter_code": fields.String,
	"capacity": fields.String,
	"empty_weight": fields.String,
	"vehicle_type": fields.String,
	"engine_number": fields.String,
	"chasis_number": fields.String,
	"puc_number": fields.String,
	"puc_issue_date": fields.String,
	"puc_expiry_date": fields.String,
	"fitness_issue": fields.String,
	"fitness_expiry": fields.String,
	"insurance_number": fields.String,
	"insurance_issue_date": fields.String,
	"insurance_expiry_date": fields.String,
	"vehicle_owner_name": fields.String,
})

get_all_vehicle_detail = reqparse.RequestParser()
get_all_vehicle_detail.add_argument("page_no", type=int, required=True, help="Page number")
get_all_vehicle_detail.add_argument("page_limit", type=int, required=True, help="limit ")


class TruckMaster(Resource):
	@api.expect(get_all_vehicle_detail)
	def get(self):
		try:
			database_connection = database_access()
			truck_details_col = database_connection["truck_master"]
			data = truck_details_col.find()
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			if len(list(data)):
				data = truck_details_col.find().skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Truck Detail'
			logging.error(e)
			return _response

	@api.expect(post_vehicle_details)
	def post(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			truck_details_col = database_connection["truck_master"]
			if not truck_details_col.find_one({"vehicle_no": args["vehicle_no"]}):
				truck_details_col.insert_one(args)
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(409))
				return get_response(409)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Truck Details'
			logging.error(e)
			return _response

	@api.expect(post_vehicle_details)
	def put(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			truck_details_col = database_connection["truck_master"]
			if truck_details_col.find_one({"vehicle_no": args["vehicle_no"]}):
				truck_details_col.update_one({"vehicle_no": args["vehicle_no"]}, {
					'$set': args})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.error(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Update Truck Details'
			logging.error(e)
			return _response


post_outbound_integration = api.model("outbound_details", {
	"trip_id": fields.String,
	"vehicle_number": fields.String,
	"movement_type": fields.String,
	"stage": fields.String,
	"check_status": fields.String,
	"check_time": fields.String,
})

get_outbound_integration = reqparse.RequestParser()
get_outbound_integration.add_argument("page_no", type=int, required=True, help="Page number")
get_outbound_integration.add_argument("page_limit", type=int, required=True, help="limit ")

delete_outbound_integration = reqparse.RequestParser()
delete_outbound_integration.add_argument("trip_id", type=str, required=True, help="Trip Id")


class OutboundIntegration(Resource):
	@api.expect(get_outbound_integration)
	def get(self):
		try:
			database_connection = database_access()
			outbound_integration_col = database_connection["outbound_integration"]
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			data = outbound_integration_col.find()
			if len(list(data)):
				data = outbound_integration_col.find().skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Outbound Integration Details'
			logging.error(e)
			return _response

	@api.expect(post_outbound_integration)
	def post(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			outbound_integration_col = database_connection["outbound_integration"]
			if not outbound_integration_col.find_one({"trip_id": args["trip_id"]}):
				outbound_integration_col.insert_one(args)
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(409))
				return get_response(409)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Outbound Integration'
			logging.error(e)
			return _response

	@api.expect(post_outbound_integration)
	def put(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			outbound_integration_col = database_connection["outbound_integration"]
			if outbound_integration_col.find_one({"trip_id": args["trip_id"]}):
				outbound_integration_col.update_one({"trip_id": args["trip_id"]}, {
					'$set': args})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.error(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Update Outbound Integration'
			logging.error(e)
			return _response

	@api.expect(delete_outbound_integration, validate=True)
	def delete(self):
		try:
			database_connection = database_access()
			outbound_integration_col = database_connection["outbound_integration"]
			trip_id = request.args.get("trip_id")
			if outbound_integration_col.find_one({"trip_id": trip_id}):
				outbound_integration_col.delete_one({"trip_id": trip_id})
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.error(get_response(404))
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Delete Outbound Integration'
			logging.error(e)
			return _response


search_outbound_integration = reqparse.RequestParser()
search_outbound_integration.add_argument("trip_id", type=str, required=True, help="Trip Id")


class SearchOutboundIntegration(Resource):
	@api.expect(search_outbound_integration)
	def get(self):
		try:
			database_connection = database_access()
			checklist_collection = database_connection["outbound_integration"]
			trip_id = request.args.get("trip_id")
			regx_trip_id = re.compile(trip_id, re.IGNORECASE)
			data = checklist_collection.find(
				{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]})
			if len(list(data)):
				data = checklist_collection.find(
					{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]})
				data = list(data)
				logging.info(get_response(200))
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				logging.info(get_response(404))
				_response = get_response(404)
				return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Outbound Integration Not Found'
			logging.error(e)
			return _response


post_integration_trigger = api.model("integration_trigger", {
	"trip_id": fields.String,
	"vehicle_number": fields.String,
	"movement_type": fields.String,
})

get_integration_trigger_detail = reqparse.RequestParser()
get_integration_trigger_detail.add_argument("page_no", type=int, required=True, help="Page number")
get_integration_trigger_detail.add_argument("page_limit", type=int, required=True, help="limit ")


class IntegrationTrigger(Resource):
	@api.expect(get_integration_trigger_detail)
	def get(self):
		try:
			database_connection = database_access()
			integration_trigger_col = database_connection["integration_trigger"]
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			data = integration_trigger_col.find()
			if len(list(data)):
				data = integration_trigger_col.find().skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Integration Trigger Detail'
			logging.error(e)
			return _response

	@api.expect(post_integration_trigger)
	def post(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			integration_trigger_col = database_connection["integration_trigger"]
			if not integration_trigger_col.find_one({"vehicle_number": args["vehicle_number"]}):
				integration_trigger_col.insert_one(args)
				logging.info(get_response(200))
				return get_response(200)
			else:
				logging.info(get_response(409))
				return get_response(409)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Integration Trigger Details'
			logging.error(e)
			return _response


filter_integration = reqparse.RequestParser()
filter_integration.add_argument("movement_type", type=str, required=True, help="Movement Type")
filter_integration.add_argument("page_no", type=int, required=True, help="Page number")
filter_integration.add_argument("page_limit", type=int, required=True, help="limit ")


class IntegrationTriggerFilter(Resource):
	@api.expect(filter_integration)
	def get(self):
		try:
			database_connection = database_access()
			integration_trigger_col = database_connection["integration_trigger"]
			movement_type = request.args.get("movement_type")
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			regx = re.compile(movement_type, re.IGNORECASE)
			data = integration_trigger_col.find({"movement_type": {'$regex': regx}})
			count = integration_trigger_col.count_documents({})
			if len(list(data)):
				data = integration_trigger_col.find({"movement_type": {'$regex': regx}}).skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				_response["count"] = count
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Integration Trigger Detail'
			logging.error(e)
			return _response


search_integration = reqparse.RequestParser()
search_integration.add_argument("trip_id", type=str, required=True, help="Trip Id")


class IntegrationTriggerSearch(Resource):
	@api.expect(search_integration)
	def get(self):
		try:
			database_connection = database_access()
			integration_trigger_col = database_connection["integration_trigger"]
			trip_id = request.args.get("trip_id")
			regx_trip_id = re.compile(trip_id, re.IGNORECASE)
			data = integration_trigger_col.find(
				{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]})
			if len(list(data)):
				data = integration_trigger_col.find(
					{"$or": [{"trip_id": {'$regex': regx_trip_id}}, {"vehicle_number": {'$regex': regx_trip_id}}]})
				data = list(data)
				logging.info(get_response(200))
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				logging.info(get_response(404))
				_response = get_response(404)
				return _response
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Integration Trigger Not Found'
			logging.error(e)
			return _response


post_stage_master = api.model("StageMaster", {
	"stages": fields.Raw(
		[],
		required=True,
		example=[

		]
	)
})

get_stage_master = reqparse.RequestParser()
get_stage_master.add_argument("page_no", type=int, required=True, help="Page number")
get_stage_master.add_argument("page_limit", type=int, required=True, help="limit ")


class StageMaster(Resource):
	@api.expect(get_stage_master)
	def get(self):
		try:
			database_connection = database_access()
			stage_master_col = database_connection["stage_master"]
			page_no = request.args.get("page_no")
			page_limit = request.args.get("page_limit")
			data = stage_master_col.find()
			if len(list(data)):
				data = stage_master_col.find().skip(int(page_limit) * (int(page_no) - 1)). \
					limit(int(page_limit))
				_response = get_response(200)
				_response["data"] = json.loads(json_util.dumps(data))
				return _response
			else:
				return get_response(404)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Get Stage Master Detail'
			logging.error(e)
			return _response

	@api.expect(post_stage_master)
	def post(self):
		args = request.get_json()
		try:
			database_connection = database_access()
			stage_master_col = database_connection["stage_master"]
			stage_master_col.insert_one(args)
			logging.info(get_response(200))
			return get_response(200)
		except Exception as e:
			_response = get_response(404)
			_response['message'] = 'Failed to Store Stages Details'
			logging.error(e)
			return _response
