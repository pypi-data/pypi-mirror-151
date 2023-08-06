"""
This file contains classes needed for ELBO progress Tracker
"""
import os
import json
import shutil
import tempfile
import elbo.connector
from enum import Enum
from elbo.actions import cp
from collections import namedtuple
import logging

from elbo.utils.misc_utils import generate_short_rand_string

logging.basicConfig()


class ProgressTileType(str, Enum):
    heart_beat = "Heart Beat"
    key_metric_numeric = "Key Numeric Metric"
    message = "Message"
    image = "Image"


ProgressTile = namedtuple("ProgressTile", 'name type value')


class TaskTracker(object):
    ELBO_PROGRESS_TRACKER_LOGS_DIRECTORY = "logs"
    ELBO_MESSAGE_TILE_NAME = "Messages"

    def __init__(self, experiment_name, experiment_id=None):
        self._experiment_id = experiment_id
        if self._experiment_id is None:
            self._experiment_id = self.get_random_human_friendly_experiment_id()
        self._elbo_connector = elbo.connector.ElboConnector()
        self._target_prefix = os.path.join(self._experiment_id, self.ELBO_PROGRESS_TRACKER_LOGS_DIRECTORY)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)
        self._progress_tiles = []
        self._payload = {
            'name': experiment_name,
            'tiles': self._progress_tiles
        }
        self._images = []
        self._output_dir = tempfile.mkdtemp()
        self._logger.debug(f"Saving to {self._output_dir}")

    @staticmethod
    def get_random_human_friendly_experiment_id():
        # TODO Generate a human friendly name like - fanciful-society-1
        return generate_short_rand_string()

    def upload_logs(self):
        json_log = json.dumps(self._payload)
        temp_file = os.path.join(self._output_dir, "elbo.json")
        with open(temp_file, "w") as fd:
            fd.write(json_log)

        self._logger.debug(json_log)
        self._logger.debug(f"Uploading file {temp_file}")
        cp.cp_to_elbo(self._elbo_connector, temp_file, self._target_prefix)
        self._logger.debug(f"Upload completed {temp_file}")
        for image in self._images:
            shutil.copyfile(image, os.path.join(self._output_dir, os.path.basename(image)))
            cp.cp_to_elbo(self._elbo_connector, image, self._target_prefix)
            self._logger.debug(f"Upload completed {image}")

        self._logger.debug(f"Logs in {self._output_dir}")
        return self._output_dir

    def log_message(self, message):
        message_tile = ProgressTile(name=self.ELBO_MESSAGE_TILE_NAME,
                                    type=ProgressTileType.message,
                                    value=message)
        self._progress_tiles.append(message_tile)

    def log_key_metric(self, key_metric: str, key_metric_value):
        """
        Log a key metric with the given name and value. Note that this overwrites the last value

        :param key_metric: The key metric
        :param key_metric_value: The metric value
        :return:
        """
        numeric_tile = ProgressTile(name=key_metric,
                                    type=ProgressTileType.key_metric_numeric,
                                    value=key_metric_value)
        self._progress_tiles.append(numeric_tile)

    def log_image(self, image_title, image_file_path):
        image_tile = ProgressTile(name=image_title,
                                  type=ProgressTileType.image,
                                  value=os.path.basename(image_file_path))
        self._progress_tiles.append(image_tile)
        self._images.append(image_file_path)
