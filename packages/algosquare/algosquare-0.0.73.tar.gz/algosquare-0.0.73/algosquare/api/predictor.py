"""AlgoSquare Predictor API."""
import os
import io
import json
import uuid
import pandas as pd

from ..base.tabular import TabularClassifier, TabularRegressor
from ..metrics import get_metric

from .common import upload_file
from .api import ApiObject, api_post, api_get, api_delete
from .model import Model

def add_model(predictor, output_dir, tag = None, metric_name = None, pos_label = None, metric_mean = None, metric_std = None, metric_num_samples = None, predictor_id = None):
    """
    Add model to latest or specific Predictor.
    
    Args:
        predictor: TabularClassifier or TabularRegressor.
        output_dir: path for temp files.   
        tag: model tag.
        metric_name: name used for get_metric.
        pos_label: positive label for binary metrics.
        metric_mean: expected value of metric.
        metric_std: standard deviation of metric.
        metric_num_samples: number of samples over which the metric_mean and metric_std has been computed.
        predictor_id: string.

    Returns:
        Model.

    Raises:
        TypeError, ValueError
    """
    if not _is_valid_predictor(predictor):
        raise TypeError('invalid predictor')  

    if predictor_id is not None and not isinstance(predictor_id, str):
        raise TypeError('invalid predictor_id')

    settings = dict()
    if tag is not None:
        if len(str(tag)) > 64:
            raise ValueError('tag must not be longer than 64')
        settings['tag'] = str(tag)

    metric = dict()
    if metric_name is None:
        metric['name'] = 'accuracy' if _is_classifier(predictor) else 'mean_squared_error'
    else:
        if get_metric(metric_name)['metatypes'] == ['binary'] and pos_label is None:
            raise ValueError('pos_label is missing')

        metric['name'] = metric_name
        if pos_label is not None:
            metric['kwargs'] = dict(pos_label = pos_label)

    metric_stats = dict()
    if metric_mean is not None:
        metric_stats['mean'] = float(metric_mean)

    if metric_std is not None:
        metric_stats['std'] = float(metric_std)

    if metric_num_samples is not None:
        metric_stats['num_samples'] = int(metric_num_samples)

    if metric_stats:
        if {'mean', 'std', 'num_samples'}.difference(metric_stats.keys()):
            raise ValueError('metric_stats not complete')
        metric['stats'] = metric_stats

    settings['metric'] = metric

    filename = uuid.uuid4().hex + '.mdl'
    model_path = os.path.join(output_dir, filename)
    predictor.save(model_path)

    payload = dict(settings = settings, class_name = type(predictor).__name__)
    payload['file'] = dict(filename = filename, key = upload_file(model_path))
    if predictor_id is not None:
        payload['predictor_id'] = predictor_id

    os.remove(model_path)
    return Model.load(api_post('api/predictors', json=payload))

class Predictor(ApiObject):
    def add_model(predictor, output_dir, tag = None, metric_name = None, pos_label = None, metric_mean = None, metric_std = None, metric_num_samples = None):
        """
        Add model to specific Predictor.
        
        Args:
            predictor: TabularClassifier or TabularRegressor.
            output_dir: path for temp files.   
            tag: model tag.
            metric_name: name used for get_metric.
            pos_label: positive label for binary metrics.
            metric_mean: expected value of metric.
            metric_std: standard deviation of metric.
            metric_num_samples: number of samples over which the metric_mean and metric_std has been computed.

        Returns:
            Model.

        Raises:
            TypeError, ValueError
        """
        if self.status == 'disabled':
            raise RuntimeError('predictor is disabled')

        return add_model(predictor, output_dir, tag, metric_name, pos_label, metric_mean, metric_std, metric_num_samples, self.predictor_id)

    @classmethod
    def get(cls, predictor_id):
        """
        Gets specific predictor.
        
        Args:
            predictor_id: string.

        Returns:
            Predictor.
        """
        return cls(api_get(f'api/predictors/{predictor_id}'))

    def get_models(self):
        """
        Gets models for predictor.
        
        Returns:
            List of Models.
        """
        return [Model.load(x) for x in api_get(f'api/predictors/{self.predictor_id}/models')]

def _is_classifier(predictor):
    for base_class in [TabularClassifier]:
        if isinstance(predictor, base_class):
            return True
    return False

def _is_valid_predictor(predictor):
    for base_class in [TabularClassifier, TabularRegressor]:
        if isinstance(predictor, base_class):
            return True
    return False