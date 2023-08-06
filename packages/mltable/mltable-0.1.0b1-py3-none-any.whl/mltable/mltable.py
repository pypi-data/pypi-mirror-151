# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Contains functionality to create and interact with MLTable objects
"""
import os
import yaml

from azureml.dataprep.api._loggerfactory import track, _LoggerFactory
from azureml.dataprep.api._dataframereader import get_dataframe_reader
from azureml.dataprep.api.mltable._mltable_helper import _read_yaml, _validate, _download_mltable_yaml, \
    _parse_path_format, _PathType, _make_all_paths_absolute

_PUBLIC_API = 'PublicApi'
_INTERNAL_API = 'InternalCall'
_logger = None
_PATHS_SECTION_KEY = 'paths'

_REQUIRED_PROPS = ['paths', 'transformations']


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _LoggerFactory.get_logger(__name__)
    return _logger


def _remove_properties_not_required(mltable_yaml_dict):
    filtered_mltable_yaml_dict = {k: v for k, v in mltable_yaml_dict.items() if k in _REQUIRED_PROPS}
    return filtered_mltable_yaml_dict


@track(_get_logger, custom_dimensions={'app_name': 'MLTable'})
def load(uri) -> 'MLTable':
    """
    Loads the MLTable file present at the given uri.

    .. remarks::

        There must be a valid MLTable file with the name 'MLTable' present at the given uri.

        .. code-block:: python
            from mltable import load
            tbl = load('.\\samples\\mltable_sample')

    :return: MLTable object representing the MLTable YAML file at uri.
    """
    if not os.path.isabs(uri):
        uri = os.path.join(os.getcwd(), uri)
    path_type, local_path, _ = _parse_path_format(uri)
    local_path = os.path.normpath(local_path)
    if path_type == _PathType.local:
        pass
    elif path_type == _PathType.cloud:
        local_path = _download_mltable_yaml(uri)
    else:
        raise ValueError('The uri should be a valid path to a local or cloud directory which contains an '
                         'MLTable file.')
    mltable_dict = _read_yaml(local_path)
    _validate(mltable_dict)
    normalized_dict = _remove_properties_not_required(mltable_dict)
    normalized_dict = _make_all_paths_absolute(normalized_dict, local_path)
    return MLTable(mltable_dict=normalized_dict, original_mltable_dict=mltable_dict)


class MLTable:
    """
    Class to create a new MLTable file or load/modify an existing file and obtain data from the paths it refers too.
    """

    def __init__(self, mltable_dict=None, original_mltable_dict=None):
        """
        Initialize a new MLTable object
        """
        self.__original_mltable_dict = original_mltable_dict
        self.__mltable_dict = mltable_dict
        if mltable_dict is not None:
            self.__mltable_yaml_string = yaml.dump(mltable_dict)

    @track(_get_logger, custom_dimensions={'app_name': 'MLTable'})
    def to_pandas_dataframe(self) -> 'pandas.DataFrame':
        """
        Load all records from the paths specified in the MLTable into a pandas DataFrame.

        .. remarks::

            The following code snippet shows how to use the to_pandas_dataframe api to obtain a pandas dataframe
            corresponding to the provided MLTable.

            .. code-block:: python
                from mltable import load
                tbl = load('.\\samples\\mltable_sample')
                pdf = tbl.to_pandas_dataframe()
                print(pdf.shape)

        :return: pandas.DataFrame object representing the records from the paths in the MLTable.
        """
        dataframe_reader = get_dataframe_reader()
        return dataframe_reader._to_pandas_arrow_rslex(self.__mltable_yaml_string)

    @property
    @track(_get_logger, custom_dimensions={'app_name': 'MLTable'})
    def paths(self):
        """
        Returns list of dicts containing paths specified in the MLTable.

        :return: A list of dicts containing paths specified in the MLTable
        :rtype: list[dict]
        """
        return self.__original_mltable_dict[_PATHS_SECTION_KEY]
