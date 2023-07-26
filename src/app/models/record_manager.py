"""
Python file consisting all the logic
"""
# Standard Library
import json

# Third Party Library
from bson import json_util
from pymongo import MongoClient
from src.app.models.exceptions import InvalidPayloadException, RecordExistenceError, RecordInExistenceError


class MongoService:
    """
    Class to connect with MongoDB and perform operations
    """
    @staticmethod
    def create_connection():
        """
        Method to connect to the MongoDB instance
        """
        try:
            connection = MongoClient('mongo', 27017)
            # creating a database
            database = connection.database
            # creating a collection under the database
            return database.my_test_database
        except Exception as error:
            msg = f'Failed to establish a connection. Error:{error}'
            raise Exception(msg) from error

    def create_record(self, payload: dict or list) -> dict:
        """
            This method takes the payload as input and validates the payload and updates it to the database
            :param payload: input payload that is required to create a record
            :return: dictionary consisting of the status of the record creation
        """
        try:
            connection = self.create_connection()
            if isinstance(payload, list):
                for record in payload:
                    self.validate_payload(payload=record)
                    record = connection.find_one({"Name": f"{payload['Name']}"})
                    if record:
                        raise RecordExistenceError(f'Record {record} already exists')
                connection.insert_many(payload)
            else:
                self.validate_payload(payload)
                record = connection.find_one({"Name": f"{payload['Name']}"})
                if record:
                    msg = f'Record {payload["Name"]} already exists'
                    raise RecordExistenceError(msg)
                connection.insert_one(payload)
            msg = {"message": f"Successfully inserted data {payload} into the database"}
            return msg
        except KeyError as error:
            raise KeyError(error.args[0]) from error
        except RecordExistenceError as error:
            raise RecordExistenceError(error) from error
        except Exception as error:
            msg = f"Encountered exception while creating record. Error:{error}"
            raise Exception(msg) from error

    def fetch_record(self, id=None) -> list or dict:
        """
            this method fetches the records that are present in the database
            :param id: record that is to be fetched
            :return: list of all the records or an individual record that is passed
        """
        connection = self.create_connection()
        if id:
            record = connection.find_one({"Name": f"{id}"})
            if record:
                return json.loads(json_util.dumps(record))
            msg = f"No record with id {id}"
            raise RecordInExistenceError(msg)
        else:
            return json_util.dumps(connection.find())

    def update_record(self, payload: dict) -> dict:
        """
            this method updates the data for a record in the database
            :param payload: input payload which is to be required for updating the value in the database
            :return: dictionary showing the status of the record
        """
        if not payload["Name"]:
            raise KeyError("Name is required in the payload")
        if len(payload) < 2:
            msg = "Requires one or more attributes to update the payload"
            raise InvalidPayloadException(msg)
        connection = self.create_connection()
        record = connection.find_one({"Name": f"{payload['Name']}"})
        if not record:
            msg = f'Record {payload["Name"]} doesnt exists'
            raise RecordInExistenceError(msg)
        filters = {"Name": payload["Name"]}
        new_values = {"$set": payload}
        connection.update_one(filters, new_values)
        message = {"Message": f"Record {filters} updated in the database"}
        return message

    def delete_record(self, id: str) -> dict:
        """
            this method deletes the record that is present in the database
            :param id: id is the record name that is to be deleted
            :return: string consisting of the deleted status
        """
        connection = self.create_connection()
        record = connection.find_one({"Name": f"{id}"})
        if record:
            record = json.loads(json_util.dumps(record))
            del record["_id"]
            connection.delete_one(record)
            msg = {"Message": f"Deleted record {id}"}
            return msg
        msg = f"No record {id} in the database"
        raise RecordInExistenceError(msg)

    @staticmethod
    def validate_payload(payload: dict) -> str:
        """
        Method to check if all the keys in the payload exists
        """
        required_keys = ("Name", "Organisation", "Location")
        for key in required_keys:
            if key not in payload.keys():
                msg = f'{key} is required in payload'
                raise KeyError(msg)
        return "Valid Payload"
