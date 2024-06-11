import unittest
from osivalidator.osi_general_validator import detect_message_type


class TestDetectMessageType(unittest.TestCase):
    def test_detect_message_type_sensor_data(self):
        path = "path/to/file_sd_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "SensorData")

    def test_detect_message_type_sensor_view(self):
        path = "path/to/file_sv_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "SensorView")

    def test_detect_message_type_sensor_view_config(self):
        path = "path/to/file_svc_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "SensorViewConfiguration")

    def test_detect_message_type_ground_truth(self):
        path = "path/to/file_gt_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "GroundTruth")

    def test_detect_message_type_traffic_update(self):
        path = "path/to/file_tu_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "TrafficUpdate")

    def test_detect_message_type_traffic_command_update(self):
        path = "path/to/file_tcu_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "TrafficCommandUpdate")

    def test_detect_message_type_traffic_command(self):
        path = "path/to/file_tc_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "TrafficCommand")

    def test_detect_message_type_host_vehicle_data(self):
        path = "path/to/file_hvd_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "HostVehicleData")

    def test_detect_message_type_motion_request(self):
        path = "path/to/file_mr_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "MotionRequest")

    def test_detect_message_type_streaming_update(self):
        path = "path/to/file_su_123.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "StreamingUpdate")

    def test_detect_message_type_unknown(self):
        path = "path/to/unknown_file.osi"
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "SensorView")

    def test_detect_message_type_empty_path(self):
        path = ""
        message_type = detect_message_type(path)
        self.assertEqual(message_type, "SensorView")


if __name__ == "__main__":
    unittest.main()
