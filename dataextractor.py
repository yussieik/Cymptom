"""
Created on Thu Feb  3 12:08:56 2022.

@author: Yossi Eikelman
"""
from dataclasses import dataclass, field
from utils import get_logger
import boto3
import botocore
from tqdm import tqdm

logger = get_logger('DATA_EXTRACTOR')


@dataclass
class ExtractInstances:
    """Extractor for pulling instances from AWS EC2."""

    access_key: str
    secret_key: str
    available_regions: dict = field(default_factory=dict)
    regions: tuple = ('us-west-2', 'us-east-2', 'us-east-1', 'us-west-1', 'af-south-1', 'ap-east-1', 'ap-southeast-3', 'ap-south-1', 'ap-northeast-3', 'ap-northeast-2', 'ap-southeast-1',
                      'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-south-1', 'eu-west-3', 'eu-north-1', 'me-south-1', 'sa-east-1', 'us-gov-east-1', 'us-gov-west-1')

    @property
    def get_regions_data(self) -> dict:
        """Getter of all available/non empty regions w/relevant information."""
        if not self.available_regions:
            success = 0
            for region in tqdm(self.regions, desc='Processing regions'):
                try:
                    client = boto3.client(
                        'ec2',
                        aws_access_key_id=self.access_key,
                        aws_secret_access_key=self.secret_key,
                        region_name=region
                    )
                    response = client.describe_instances()
                    self.available_regions[region] = response
                    success += 1
                    logger.info(f"Successful connection to region: {region}")
                except botocore.exceptions.ClientError:
                    pass
                except botocore.exceptions.ParamValidationError:
                    logger.exception(
                        "Failed to connect: invalid access_key/secret key")
                    raise Exception("Failed connection: invalid keys")
            if success == 0:
                logger.exception(
                    "Failed to connect: No available regions")
                raise Exception("Failed connection: no available regions")

            logger.info(
                f"Successfully connected to {success}/{len(self.regions)} regions")

        return self.available_regions

    @property
    def extract_instances(self) -> dict:
        """Getter all instances per available region."""
        info = {}

        if not self.available_regions:
            self.available_regions = self.get_regions_data

        for _k, _v in self.available_regions.items():
            for instance in _v['Reservations'][0]['Instances']:
                info[_k] = {_v['Reservations'][0]
                            ['Instances'].index(instance): instance}
            logger.info(f"extracted {len(info[_k])} for instance {_k}")
        return info


@dataclass
class Preprocess:
    """Preprocessor for preparing extracted data/instaces for humans."""

    def find_values(self, dictionary: dict, output: dict, my_keys: str = ''):
        """Flatten all values in nested dictionaries/lists."""
        for key, value in dictionary.items():
            current_key = my_keys + str(key) + '_'
            if isinstance(value, dict):
                self.find_values(value, output, current_key)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.find_values(item, output, current_key)
            else:
                output[current_key[:-1]] = value

    def preprocess_instance(self, instance_dict: dict) -> tuple:
        """Extract non list/dict column names."""
        columns = [k for k in instance_dict.keys() if type(
            instance_dict[k]) not in [list, dict]]

        other_columns = [k for k in instance_dict.keys() if k not in columns]
        other_dict = {k: instance_dict[k] for k in other_columns}

        res = {}

        self.find_values(other_dict, res)

        if len(res) == 0:
            logger.warning("Couldn't surface values from instance")
        return res, other_columns

    def preprocess_data(self, data: dict) -> dict:
        """Preprocess all data, return flat dictionary w/all values/keys."""
        result = {}
        for region, instance in data.items():
            for i_id, inst in instance.items():
                result[f"{i_id}_{region}"], other_columns = self.preprocess_instance(
                    inst)
                logger.info(
                    f"surfaced {len(other_columns)} fields for instance {i_id}_{region}")
                for other in other_columns:
                    inst.pop(other)
                result[f"{i_id}_{region}"].update(inst)
        return result


@dataclass
class ConnectDB:
    """Connector to AWS EC2/Producer of readable Database of instances."""

    access_key: str
    secret_key: str
    data: dict = field(default_factory=dict)
    _df: dict = field(default_factory=dict)

    def upload_db(self):
        """Connect to AWS EC2 and extract instances."""
        extractor = ExtractInstances(self.access_key, self.secret_key)

        data_extracted = extractor.extract_instances
        if not data_extracted:
            logger.exception("Upload failed, check access_key/secret key")
            raise Exception('Failed Upload')
        self.data = data_extracted

    @property
    def get_db(self) -> dict:
        """Get uploaded instances from EC2."""
        if not self.data:
            logger.exception("No uploaded data")
            raise Exception('No data in Database')
        return self.data

    @property
    def get_df(self) -> dict:
        """Get readable DB out of the provided address to EC2."""
        if not self._df:

            if not self.data:
                logger.exception("No processed uploaded data")
                raise Exception('No data in Processed data in DB')
            preprocess = Preprocess()
            self._df = preprocess.preprocess_data(self.data)
        return self._df
