"""Unit Test Cases for record_manager.py file"""
# Standard Library
import unittest
from unittest import mock

# Third Party Library
from nose.tools import assert_raises

# Custom Library
from app.models.exceptions import RecordInExistenceError
from app.models.record_manager import MongoService


class TestRecordManager(unittest.TestCase):
    def setUp(self):
        self.mongo_service = MongoService()
        self.payload = {
            "Location": "Mumbai",
            "Name": "Test_Gowrav",
            "Organisation": "ABC"
        }

    @mock.patch('pymongo.collection.Collection.insert_one')
    @mock.patch('app.models.record_manager.MongoService.validate_payload')
    def test_01_create_new_single_record_success(self, mock_validate_payload, mock_find):
        """test_01_create_new_single_record_success"""
        mock_validate_payload.return_value = "Valid Payload"
        mock_find.return_value = {'_id': '1234', 'Location': 'Mumbai', 'Name': 'Test_Gowrav',
                                  'Organisation': 'ABC'}
        response = self.mongo_service.create_record(payload=self.payload)
        expected_result = {
            'message': "Successfully inserted data {'Location': 'Mumbai', 'Name': 'Test_Gowrav', 'Organisation': "
                       "'ABC'} into the database"}
        self.assertEqual(expected_result, response)

    @mock.patch('pymongo.collection.Collection.insert_one')
    @mock.patch('requests.get')
    @mock.patch('app.models.record_manager.MongoService.validate_payload')
    def test_02_create_new_multiple_record_success(self, mock_validate_payload, mock_get, mock_find):
        """test_02_create_new_multiple_record_success"""
        mock_get.return_value.status_code = 404
        mock_validate_payload.return_value = "Valid Payload"
        mock_find.return_value = {'_id': '1234', 'Location': 'Mumbai', 'Name': 'Test_Gowrav_2',
                                  'Organisation': 'ABC'}
        response = self.mongo_service.create_record(payload=[self.payload])
        self.assertTrue(response)

    def test_03_invalid_payload(self):
        """test_03_invalid_payload"""
        del self.payload['Name']
        with assert_raises(KeyError):
            self.mongo_service.create_record(payload=self.payload)

    @mock.patch('app.models.record_manager.MongoService.create_connection')
    def test_04_connection_exception(self, mock_create_connection):
        """test_04_connection_exception"""
        mock_create_connection.side_effect = Exception("Connection Exception")
        with assert_raises(Exception):
            self.mongo_service.create_record(payload=self.payload)

    def test_05_record_inexistence_error(self):
        """test_05_record_inexistence_error"""
        self.payload.update({'Name': 123})
        with self.assertRaises(RecordInExistenceError):
            self.mongo_service.delete_record(id=self.payload['Name'])

    @mock.patch('pymongo.collection.Collection.update_one')
    @mock.patch('requests.get')
    def test_06_update_record_success(self, mock_get, mock_update_one):
        """test_06_update_record_success"""
        mock_get.return_value.status_code = 200
        mock_update_one.return_value = {'Message': "Record {'Name': 'Test_Gowrav'} updated in the database"}
        del self.payload["Location"]
        self.payload.update({"Organisation": "LT"})
        response = self.mongo_service.update_record(payload=self.payload)
        expected_response = {'Message': "Record {'Name': 'Test_Gowrav'} updated in the database"}
        self.assertEqual(expected_response, response)

    @mock.patch("requests.get")
    def test_07_update_record_fails_due_to_no_record_exists_error(self, mock_get):
        """test_07_update_record_fails_due_to_no_record_exists_error"""
        mock_get.return_value.status_code = 404
        payload = {"Name": 123, "Location": "Hyderadad"}
        with self.assertRaises(RecordInExistenceError):
            self.mongo_service.update_record(payload=payload)

    @mock.patch("requests.get")
    def test_08_delete_record_success(self, mock_get):
        """test_08_delete_record_success"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = b'{"_id": 123, "Name": "Test_Gowrav"}'
        response = self.mongo_service.delete_record(id=self.payload["Name"])
        expected_result = {'Message': 'Deleted record Test_Gowrav'}
        self.assertEqual(expected_result, response)
