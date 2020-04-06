Usage
=======

Example
----------------
After installation you can call the command ``osivalidator`` in your terminal which has the following usage:

.. code-block:: bash

    usage: osivalidator [-h] [--rules RULES]
                        [--type {SensorView,GroundTruth,SensorData}]
                        [--output OUTPUT] [--timesteps TIMESTEPS] [--debug]
                        [--verbose] [--parallel] [--format {separated,None}]
                        [--blast BLAST] [--buffer BUFFER]
                        data

    Validate data defined at the input

    positional arguments:
    data                  Path to the file with OSI-serialized data.

    optional arguments:
    -h, --help            show this help message and exit
    --rules RULES, -r RULES
                            Directory with text files containig rules.
    --type {SensorView,GroundTruth,SensorData}, -t {SensorView,GroundTruth,SensorData}
                            Name of the type used to serialize data.
    --output OUTPUT, -o OUTPUT
                            Output folder of the log files.
    --timesteps TIMESTEPS
                            Number of timesteps to analyze. If -1, all.
    --debug               Set the debug mode to ON.
    --verbose, -v         Set the verbose mode to ON.
    --parallel, -p        Set parallel mode to ON.
    --format {separated,None}, -f {separated,None}
                            Set the format type of the trace.
    --blast BLAST, -bl BLAST
                            Set the in-memory storage count of OSI messages during
                            validation.
    --buffer BUFFER, -bu BUFFER
                            Set the buffer size to retrieve OSI messages from
                            trace file. Set it to 0 if you do not want to use
                            buffering at all.

To run the validation first you need an OSI trace file which consists of multiple OSI messages. 
In the directory ``data`` of the repository we already provide an example trace file which is called ``small_test.txt.lzma`` (a `lzma <https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm>`_ compressed trace file with the ``$$__$$`` separator which can/should be converted into an ``*.osi`` file). For decompressing lzma compressed files on linux machines run ``lzma -d data/small_test.txt.lzma``. 
Use the `txt2osi.py <https://github.com/OpenSimulationInterface/open-simulation-interface/blob/master/format/txt2osi.py>`_ of the OSI repo in the format directory to convert from ``*.txt`` to ``*.osi`` files or from ``*.txt.lzma`` to ``*.osi.lzma``). See usage below:

.. code-block:: bash

    usage: txt2osi converter [-h] [--file FILE]
                            [--type {SensorView,GroundTruth,SensorData}]
                            [--output OUTPUT] [--compress]

    Convert txt trace file to osi trace files.

    optional arguments:
    -h, --help            show this help message and exit
    --file FILE, -f FILE  Path to the file with serialized data.
    --type {SensorView,GroundTruth,SensorData}, -t {SensorView,GroundTruth,SensorData}
                            Name of the type used to serialize data.
    --output OUTPUT, -o OUTPUT
                            Output name of the file.
    --compress, -c        Compress the output to a lzma file.

To validate the trace files you simply call ``osivalidator`` and provide the path to the trace:

.. code-block:: bash

    osivalidator --data data/small_test.osi.lzma
    osivalidator --data data/small_test.txt.lzma

You can also validate the traces in parallel to increase the speed of the validation by providing ``-p`` flag:

.. code-block:: bash

    osivalidator --data data/small_test.osi.lzma -p
    osivalidator --data data/small_test.txt.lzma -p

To validate trace files with rules defined in the comments of ``*.proto`` files in the open-simulation-interface repository first you need to generate them and then specify them:

.. code-block:: bash

    python rules2yml.py # Generates the rule directory
    osivalidator -r rules data/small_test.txt.lzma -p


After successfully running the validation the following output is generated:

.. note::

    For demonstration purposes a more complex trace file was used in this example.

.. code-block:: bash

    Instantiate logger ...
    Reading data ...
    Retrieving messages in osi trace file until 3606600 ...
    |################################| 3606600/3606600
    1500 messages has been discovered in 0.03429770469665527 s
    Collect validation rules ...

    Caching ...
    Importing messages from trace file ...
    |################################| 500/500
    Caching done!
    |##########                      | 500/1500 [0:00:02]
    Closed pool!

    Caching ...
    Importing messages from trace file ...
    |################################| 500/500
    Caching done!
    |#####################           | 1000/1500 [0:00:07]
    Closed pool!

    Caching ...
    Importing messages from trace file ...
    |################################| 500/500
    Caching done!
    |################################| 1500/1500 [0:00:13]
    Closed pool!


    Errors (57) 
    Ranges of timestamps                Message
    ----------------------------------  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    [0, 1499]                           SensorView.sensor_id.is_set(None) does not comply in SensorView
    [0, 498], [500, 998], [1000, 1498]  SensorView.host_vehicle_id.is_set(None) does not comply in SensorView
    [0, 1499]                           SensorView.version.is_set(None) does not comply in SensorView
    [0, 1499]                           SensorView.mounting_position.is_set(None) does not comply in SensorView
    [0, 1499]                           SensorView.mounting_position_rmse.is_set(None) does not comply in SensorView
    [0, 1499]                           SensorView.host_vehicle_data.is_set(None) does not comply in SensorView
    [0, 1499]                           GroundTruth.country_code.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           GroundTruth.version.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           GroundTruth.stationary_object.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           MovingObject.vehicle_attributes.check_if.is_set(None) does not comply in SensorView.global_ground_truth.moving_object
    [0, 1499]                           MovingObject.vehicle_attributes.check_if([{'is_equal_to': 2, 'target': 'this.type'}]) does not comply in SensorView.global_ground_truth.moving_object
    [0, 1499]                           MovingObject.vehicle_attributes.is_set(None) does not comply in SensorView.global_ground_truth.moving_object
    [0, 1499]                           MovingObject.VehicleClassification.trailer_id.is_set(None) does not comply in SensorView.global_ground_truth.moving_object.vehicle_classification
    [0, 1499]                           MovingObject.VehicleClassification.light_state.is_set(None) does not comply in SensorView.global_ground_truth.moving_object.vehicle_classification
    [0, 1499]                           MovingObject.VehicleClassification.has_trailer.is_set(None) does not comply in SensorView.global_ground_truth.moving_object.vehicle_classification
    [0, 1499]                           MovingObject.vehicle_classification.is_valid(None) does not comply in SensorView.global_ground_truth.moving_object.vehicle_classification
    [0, 1499]                           BaseMoving.orientation.is_set(None) does not comply in SensorView.global_ground_truth.moving_object.base
    [0, 1499]                           BaseMoving.acceleration.is_set(None) does not comply in SensorView.global_ground_truth.moving_object.base
    [0, 1499]                           BaseMoving.orientation_rate.is_set(None) does not comply in SensorView.global_ground_truth.moving_object.base
    [0, 1499]                           BaseMoving.orientation_acceleration.is_set(None) does not comply in SensorView.global_ground_truth.moving_object.base
    [0, 1499]                           BaseMoving.base_polygon.is_set(None) does not comply in SensorView.global_ground_truth.moving_object.base
    [0, 1499]                           MovingObject.base.is_valid(None) does not comply in SensorView.global_ground_truth.moving_object.base
    [0, 1499]                           MovingObject.assigned_lane_id.is_set(None) does not comply in SensorView.global_ground_truth.moving_object
    [0, 1499]                           MovingObject.model_reference.is_set(None) does not comply in SensorView.global_ground_truth.moving_object
    [0, 1499]                           GroundTruth.moving_object.is_valid(None) does not comply in SensorView.global_ground_truth.moving_object
    [0, 1499]                           GroundTruth.traffic_sign.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           GroundTruth.traffic_light.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           GroundTruth.road_marking.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           LaneBoundary.boundary_line.first_element({'height': [{'is_equal_to': 0, 'target': 'this.height'}]}) does not comply in SensorView.global_ground_truth.lane_boundary.boundary_line
    [0, 1499]                           LaneBoundary.boundary_line.last_element({'height': [{'is_equal_to': 0, 'target': 'this.height'}]}) does not comply in SensorView.global_ground_truth.lane_boundary.boundary_line
    [0, 1499]                           LaneBoundary.BoundaryPoint.width.is_set(None) does not comply in SensorView.global_ground_truth.lane_boundary.boundary_line
    [0, 1499]                           LaneBoundary.BoundaryPoint.height.is_set(None) does not comply in SensorView.global_ground_truth.lane_boundary.boundary_line
    [0, 1499]                           LaneBoundary.boundary_line.is_valid(None) does not comply in SensorView.global_ground_truth.lane_boundary.boundary_line
    [0, 1499]                           LaneBoundary.classification.is_set(None) does not comply in SensorView.global_ground_truth.lane_boundary
    [0, 1499]                           GroundTruth.lane_boundary.is_valid(None) does not comply in SensorView.global_ground_truth.lane_boundary
    [0, 1499]                           Lane.Classification.left_adjacent_lane_id.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.Classification.right_adjacent_lane_id.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.Classification.right_lane_boundary_id.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.Classification.left_lane_boundary_id.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.Classification.free_lane_boundary_id.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.Classification.type.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.Classification.is_host_vehicle_lane.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.Classification.centerline_is_driving_direction.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.Classification.lane_pairing.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.Classification.road_condition.is_set(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           Lane.classification.is_valid(None) does not comply in SensorView.global_ground_truth.lane.classification
    [0, 1499]                           GroundTruth.lane.is_valid(None) does not comply in SensorView.global_ground_truth.lane
    [0, 1499]                           GroundTruth.occupant.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           GroundTruth.environmental_conditions.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           GroundTruth.proj_string.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           GroundTruth.map_reference.is_set(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           SensorView.global_ground_truth.is_valid(None) does not comply in SensorView.global_ground_truth
    [0, 1499]                           SensorView.generic_sensor_view.is_set(None) does not comply in SensorView
    [0, 1499]                           SensorView.radar_sensor_view.is_set(None) does not comply in SensorView
    [0, 1499]                           SensorView.lidar_sensor_view.is_set(None) does not comply in SensorView
    [0, 1499]                           SensorView.camera_sensor_view.is_set(None) does not comply in SensorView
    [0, 1499]                           SensorView.ultrasonic_sensor_view.is_set(None) does not comply in SensorView

    Warnings (3) 
    Ranges of timestamps    Message
    ----------------------  ----------------------------------------------------------------------
    [0, 1499]               Several objects of type MovingObject, LaneBoundary, Lane have the ID 0
    [0, 1499]               Several objects of type MovingObject, LaneBoundary, Lane have the ID 1
    [0, 1499]               Several objects of type LaneBoundary, Lane have the ID 2


The Output is a report of how many errors (here 57) and warnings (here 3) were found in the osi-message according to the defined rules in your specified rules directory. The rules can be found under the tag ``\rules`` in the \*.proto files from the `osi github <https://github.com/OpenSimulationInterface/open-simulation-interface>`_ or in the `requirements folder <https://github.com/OpenSimulationInterface/osi-validation/tree/master/requirements-osi-3>`_ from osi-validation as \*.yml files (for more information see :ref:`commenting`).

Currently an error is thrown when a field is not valid. A warning is thrown when a field is valid and set but does not comply with the defined rules. For each error and warning there is a description on which timestamp it was found, the path to the rule and the path to the osi-message. The general format is:

.. code-block:: bash

    Errors (NUMBER_ERRORS) 
    Ranges of timestamps                Message
    --------------------------------    --------------------------------------------------------
    [START_TIMESTAMP, END_TIMESTAMP]    PATH_TO_RULE(VALUE) does not comply in PATH_TO_OSI_FIELD

    Warnings (NUMBER_WARNINGS) 
    Ranges of timestamps    Message
    --------------------------------    --------------------------------------------------------
    [START_TIMESTAMP, END_TIMESTAMP]    PATH_TO_RULE(VALUE) does not comply in PATH_TO_OSI_FIELD

The rules to the fileds are applied in a recursive fashion. 