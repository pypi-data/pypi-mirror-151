#  Author:   Niels Nuyttens  <niels@nannyml.com>
#
#  License: Apache Software License 2.0

"""Unit tests for metadata module."""
import math

import numpy as np
import pandas as pd
import pytest

from nannyml import MulticlassClassificationMetadata
from nannyml.exceptions import InvalidArgumentsException, MissingMetadataException
from nannyml.metadata import BinaryClassificationMetadata, extract_metadata
from nannyml.metadata.base import (
    Feature,
    FeatureType,
    ModelMetadata,
    ModelType,
    _guess_features,
    _guess_partitions,
    _guess_targets,
    _guess_timestamps,
    _predict_feature_types,
)
from nannyml.metadata.extraction import ModelMetadataFactory


@pytest.fixture
def sample_feature() -> Feature:  # noqa: D103
    return Feature(label='label', column_name='col', description='desc', feature_type=FeatureType.CATEGORICAL)


@pytest.fixture
def sample_model_metadata(sample_feature) -> ModelMetadata:  # noqa: D103
    return BinaryClassificationMetadata(model_name='my_model', features=[sample_feature])


@pytest.fixture
def sample_data() -> pd.DataFrame:  # noqa: D103
    data = pd.DataFrame(pd.date_range(start='1/6/2020', freq='10min', periods=20 * 1008), columns=['timestamp'])
    data['week'] = data.timestamp.dt.isocalendar().week - 1
    data['partition'] = 'reference'
    data.loc[data.week >= 11, ['partition']] = 'analysis'
    # data[NML_METADATA_PARTITION_COLUMN_NAME] = data['partition']  # simulate preprocessing
    np.random.seed(167)
    data['f1'] = np.random.randn(data.shape[0])
    data['f2'] = np.random.rand(data.shape[0])
    data['f3'] = np.random.randint(4, size=data.shape[0])
    data['f4'] = np.random.randint(20, size=data.shape[0])
    data['output'] = np.random.randint(2, size=data.shape[0])
    data['actual'] = np.random.randint(2, size=data.shape[0])

    # Rule 1b is the shifted feature, 75% 0 instead of 50%
    rule1a = {2: 0, 3: 1}
    rule1b = {2: 0, 3: 0}
    data.loc[data.week < 16, ['f3']] = data.loc[data.week < 16, ['f3']].replace(rule1a)
    data.loc[data.week >= 16, ['f3']] = data.loc[data.week >= 16, ['f3']].replace(rule1b)

    # Rule 2b is the shifted feature
    c1 = 'white'
    c2 = 'red'
    c3 = 'green'
    c4 = 'blue'

    rule2a = {
        0: c1,
        1: c1,
        2: c1,
        3: c1,
        4: c1,
        5: c2,
        6: c2,
        7: c2,
        8: c2,
        9: c2,
        10: c3,
        11: c3,
        12: c3,
        13: c3,
        14: c3,
        15: c4,
        16: c4,
        17: c4,
        18: c4,
        19: c4,
    }

    rule2b = {
        0: c1,
        1: c1,
        2: c1,
        3: c1,
        4: c1,
        5: c2,
        6: c2,
        7: c2,
        8: c2,
        9: c2,
        10: c3,
        11: c3,
        12: c3,
        13: c1,
        14: c1,
        15: c4,
        16: c4,
        17: c4,
        18: c1,
        19: c2,
    }

    data.loc[data.week < 16, ['f4']] = data.loc[data.week < 16, ['f4']].replace(rule2a)
    data.loc[data.week >= 16, ['f4']] = data.loc[data.week >= 16, ['f4']].replace(rule2b)

    data.loc[data.week >= 16, ['f1']] = data.loc[data.week >= 16, ['f1']] + 0.6
    data.loc[data.week >= 16, ['f2']] = np.sqrt(data.loc[data.week >= 16, ['f2']])
    data['id'] = data.index
    data.drop(columns=['week'], inplace=True)

    return data


def test_feature_creation_sets_properties_correctly():  # noqa: D103
    sut = Feature(label='label', column_name='col', description='desc', feature_type=FeatureType.CATEGORICAL)
    assert sut.label == 'label'
    assert sut.column_name == 'col'
    assert sut.description == 'desc'
    assert sut.feature_type == FeatureType.CATEGORICAL


# TODO: rewrite this using regexes
def test_feature_string_representation_contains_all_properties(sample_feature):  # noqa: D103
    sut = sample_feature.print()
    assert "Feature: label" in sut
    assert 'Column name' in sut
    assert 'Description' in sut
    assert 'Type' in sut


def test_binary_classification_metadata_creation_with_custom_values_has_correct_properties(  # noqa: D103
    sample_feature,
):
    sut = BinaryClassificationMetadata(
        model_name='model',
        features=[sample_feature],
        prediction_column_name='pred',
        predicted_probability_column_name='pred_proba',
        target_column_name='gt',
        partition_column_name='part',
        timestamp_column_name='ts',
    )
    assert sut.name == 'model'
    assert sut.model_type == ModelType.CLASSIFICATION_BINARY
    assert len(sut.features) == 1
    assert sut.features[0].label == 'label'
    assert sut.features[0].column_name == 'col'
    assert sut.features[0].description == 'desc'
    assert sut.features[0].feature_type == FeatureType.CATEGORICAL
    assert sut.prediction_column_name == 'pred'
    assert sut.predicted_probability_column_name == 'pred_proba'
    assert sut.target_column_name == 'gt'
    assert sut.partition_column_name == 'part'
    assert sut.timestamp_column_name == 'ts'


def test_to_dict_contains_all_properties(sample_model_metadata):  # noqa: D103
    sut = sample_model_metadata.to_dict()
    assert sut['prediction_column_name'] is None
    assert sut['predicted_probability_column_name'] is None
    assert sut['partition_column_name'] == 'partition'
    assert sut['timestamp_column_name'] == 'date'
    assert sut['target_column_name'] == 'target'


def test_to_pd_contains_all_properties(sample_model_metadata):  # noqa: D103
    sut = sample_model_metadata.to_df()
    assert sut.loc[sut['label'] == 'prediction_column_name', 'column_name'].iloc[0] is None
    assert sut.loc[sut['label'] == 'predicted_probability_column_name', 'column_name'].iloc[0] is None
    assert sut.loc[sut['label'] == 'partition_column_name', 'column_name'].iloc[0] == 'partition'
    assert sut.loc[sut['label'] == 'timestamp_column_name', 'column_name'].iloc[0] == 'date'
    assert sut.loc[sut['label'] == 'target_column_name', 'column_name'].iloc[0] == 'target'


def test_feature_filtering_by_index_delivers_correct_result(sample_model_metadata):  # noqa: D103
    features = [
        Feature(label=str.upper(c), column_name=c, feature_type=FeatureType.CATEGORICAL, description='')
        for c in ['a', 'b', 'c']
    ]
    sample_model_metadata.features = features
    for i in range(len(features)):
        assert sample_model_metadata.feature(index=i) == features[i]


def test_feature_filtering_by_index_with_out_of_bounds_index_raises_exception(sample_model_metadata):  # noqa: D103
    features = [
        Feature(label=str.upper(c), column_name=c, feature_type=FeatureType.CATEGORICAL, description='')
        for c in ['a', 'b', 'c']
    ]
    sample_model_metadata.features = features
    with pytest.raises(IndexError):
        _ = sample_model_metadata.feature(index=99)


def test_feature_filtering_by_feature_name_delivers_correct_result(sample_model_metadata):  # noqa: D103
    features = [
        Feature(label=str.upper(c), column_name=c, feature_type=FeatureType.CATEGORICAL, description='')
        for c in ['a', 'b', 'c']
    ]
    sample_model_metadata.features = features
    for i, c in enumerate(['a', 'b', 'c']):
        assert sample_model_metadata.feature(feature=str.upper(c)) == features[i]


def test_feature_filtering_by_feature_name_without_matches_returns_none(sample_model_metadata):  # noqa: D103
    features = [
        Feature(label=str.upper(c), column_name=c, feature_type=FeatureType.CATEGORICAL, description='')
        for c in ['a', 'b', 'c']
    ]
    sample_model_metadata.features = features
    assert sample_model_metadata.feature(feature='I dont exist') is None


def test_feature_filtering_by_column_name_returns_correct_result(sample_model_metadata):  # noqa: D103
    features = [
        Feature(label=str.upper(c), column_name=c, feature_type=FeatureType.CATEGORICAL, description='')
        for c in ['a', 'b', 'c']
    ]
    sample_model_metadata.features = features
    for i, c in enumerate(['a', 'b', 'c']):
        assert sample_model_metadata.feature(column=c) == features[i]


def test_feature_filtering_by_column_name_without_matches_returns_none(sample_model_metadata):  # noqa: D103
    features = [
        Feature(label=str.upper(c), column_name=c, feature_type=FeatureType.CATEGORICAL, description='')
        for c in ['a', 'b', 'c']
    ]
    sample_model_metadata.features = features
    assert sample_model_metadata.feature(column='I dont exist') is None


def test_feature_filtering_without_criteria_returns_none(sample_model_metadata):  # noqa: D103
    features = [
        Feature(label=str.upper(c), column_name=c, feature_type=FeatureType.CATEGORICAL, description='')
        for c in ['a', 'b', 'c']
    ]
    sample_model_metadata.features = features
    assert sample_model_metadata.feature() is None


def test_extract_metadata_for_no_cols_dataframe_should_return_none():  # noqa: D103
    sut = extract_metadata(data=pd.DataFrame(), model_type='classification_binary')
    assert sut is None


def test_extract_metadata_without_any_feature_columns_should_return_metadata_without_features():  # noqa: D103
    data = pd.DataFrame(columns=['actual', 'partition', 'ts'])
    sut = extract_metadata(data, model_type='classification_binary')
    assert len(sut.features) == 0


def test_extract_metadata_should_not_consider_excluded_columns(sample_model_metadata, sample_data):  # noqa: D103
    metadata = extract_metadata(sample_data, exclude_columns=['id'], model_type='classification_binary')
    assert metadata.feature(feature='id') is None


def test_extract_metadata_for_empty_dataframe_should_return_correct_column_names(sample_model_metadata):  # noqa: D103
    data = pd.DataFrame(columns=['y_pred', 'y_pred_proba', 'actual', 'partition', 'ts', 'feat1', 'feat2'])
    sut = extract_metadata(data, model_type='classification_binary')
    assert sut is not None
    assert sut.target_column_name == 'actual'
    assert sut.partition_column_name == 'partition'
    assert sut.timestamp_column_name == 'ts'


# TODO verify behaviour
def test_extract_metadata_for_empty_dataframe_should_return_features_with_feature_type_unknown():  # noqa: D103
    data = pd.DataFrame(columns=['actual', 'partition', 'ts', 'feat1', 'feat2'])
    sut = extract_metadata(data, model_type='classification_binary')
    assert len(sut.features) == 2
    assert sut.features[0].feature_type is FeatureType.UNKNOWN
    assert sut.features[1].feature_type is FeatureType.UNKNOWN


def test_extract_metadata_without_matching_columns_should_set_them_to_none():  # noqa: D103
    data = pd.DataFrame(columns=['a', 'b', 'c'])
    sut = extract_metadata(data, model_type='classification_binary')
    assert sut.prediction_column_name is None
    assert sut.target_column_name is None
    assert sut.partition_column_name is None
    assert sut.timestamp_column_name is None


def test_extract_metadata_without_matching_columns_should_set_features():  # noqa: D103
    data = pd.DataFrame(columns=['a', 'b', 'c'])
    sut = extract_metadata(data, model_type='classification_binary')
    assert len(sut.features) == 3
    assert sut.feature(column='a')
    assert sut.feature(column='b')
    assert sut.feature(column='c')


def test_extract_metadata_with_multiple_matching_columns_should_return_first_matching_column():  # noqa: D103
    data = pd.DataFrame(columns=['target', 'ground_truth', 'actual'])
    sut = extract_metadata(data, model_type='classification_binary')
    assert sut.target_column_name == 'target'


def test_extract_metadata_does_not_fail_when_adding_metadata_parameter_fails():  # noqa: D103
    cols = ['actual', 'partition', 'timestamp_non_standard', 'feat1', 'feat2']
    df = pd.DataFrame(columns=cols)
    try:
        _ = extract_metadata(df, model_type='classification_binary')
    except Exception:
        pytest.fail("should not have failed because of inner exception")


@pytest.mark.parametrize('metadata_column', ['timestamp', 'actual', 'partition'])
def test_extract_metadata_raises_missing_metadata_exception_when_missing_metadata_values(metadata_column):  # noqa: D103
    df = pd.DataFrame({metadata_column: [np.NaN]})
    with pytest.raises(MissingMetadataException):
        _ = extract_metadata(df, model_type='classification_binary')


@pytest.mark.parametrize(
    'col,expected', [('date', True), ('timestamp', True), ('ts', True), ('date', True), ('time', True), ('nope', False)]
)
def test_guess_timestamps_yields_correct_results(col, expected):  # noqa: D103
    sut = _guess_timestamps(data=pd.DataFrame(columns=[col]))
    assert col == sut[0] if expected else len(sut) == 0


@pytest.mark.parametrize(
    'col,expected', [('target', True), ('ground_truth', True), ('actual', True), ('actuals', True), ('nope', False)]
)
def test_guess_ground_truths_yields_correct_results(col, expected):  # noqa: D103
    sut = _guess_targets(data=pd.DataFrame(columns=[col]))
    assert col == sut[0] if expected else len(sut) == 0


@pytest.mark.parametrize(
    'col,expected', [('part', False), ('partition', True), ('data_partition', True), ('nope', False)]
)
def test_guess_partitions_yields_correct_results(col, expected):  # noqa: D103
    sut = _guess_partitions(data=pd.DataFrame(columns=[col]))
    assert col == sut[0] if expected else len(sut) == 0


@pytest.mark.parametrize(
    'col,expected', [('part', True), ('A', True), ('partition', False), ('id', True), ('nope', True)]
)
def test_guess_features_yields_correct_results(col, expected):  # noqa: D103
    sut = _guess_features(data=pd.DataFrame(columns=[col]))
    assert col == sut[0] if expected else len(sut) == 0


def test_feature_type_detection_with_rows_under_num_rows_threshold_should_return_none():  # noqa: D103
    data = pd.DataFrame(columns=['a', 'b', 'c', 'd'])
    sut = _predict_feature_types(data)
    assert sut['predicted_feature_type'].map(lambda t: t == FeatureType.UNKNOWN).all()


def test_feature_type_detection_sets_float_cols_to_continuous():  # noqa: D103
    data = pd.DataFrame({'A': [math.pi for i in range(1000)]})
    sut = _predict_feature_types(data)
    assert sut.loc['A', 'predicted_feature_type'] == FeatureType.CONTINUOUS


def test_feature_type_detection_sets_int_cols_with_high_unique_value_count_to_continuous():  # noqa: D103
    data = pd.DataFrame({'A': np.random.randint(75, size=10000)})
    sut = _predict_feature_types(data)
    assert sut.loc['A', 'predicted_feature_type'] == FeatureType.CONTINUOUS


def test_feature_type_detection_sets_above_high_cardinality_threshold_to_nominal():  # noqa: D103
    data = pd.DataFrame({'A': np.random.randint(75, size=100)})
    sut = _predict_feature_types(data)
    assert sut.loc['A', 'predicted_feature_type'] == FeatureType.CONTINUOUS


def test_feature_type_detection_sets_between_mid_and_high_cardinality_threshold_to_none():  # noqa: D103
    data = pd.DataFrame({'A': np.random.randint(39, size=1000)})
    sut = _predict_feature_types(data)
    assert sut.loc['A', 'predicted_feature_type'] == FeatureType.UNKNOWN


def test_feature_type_detection_sets_between_low_and_mid_cardinality_threshold_to_nominal():  # noqa: D103
    data = pd.DataFrame({'A': np.random.randint(6, size=1000)})
    sut = _predict_feature_types(data)
    assert sut.loc['A', 'predicted_feature_type'] == FeatureType.CATEGORICAL


def test_categorical_features_returns_only_nominal_features(sample_model_metadata):  # noqa: D103
    sample_model_metadata.features = [
        Feature(label='f1', column_name='f1', feature_type=FeatureType.CATEGORICAL),
        Feature(label='f2', column_name='f2', feature_type=FeatureType.UNKNOWN),
        Feature(label='f3', column_name='f3', feature_type=FeatureType.CATEGORICAL),
        Feature(label='f4', column_name='f4', feature_type=FeatureType.CONTINUOUS),
        Feature(label='f5', column_name='f5', feature_type=FeatureType.CATEGORICAL),
    ]

    sut = sample_model_metadata.categorical_features
    assert len(sut) == 3
    assert [f.label for f in sut] == ['f1', 'f3', 'f5']


def test_continuous_features_returns_only_continuous_features(sample_model_metadata):  # noqa: D103
    sample_model_metadata.features = [
        Feature(label='f1', column_name='f1', feature_type=FeatureType.CATEGORICAL),
        Feature(label='f2', column_name='f2', feature_type=FeatureType.UNKNOWN),
        Feature(label='f3', column_name='f3', feature_type=FeatureType.CATEGORICAL),
        Feature(label='f4', column_name='f4', feature_type=FeatureType.CONTINUOUS),
        Feature(label='f5', column_name='f5', feature_type=FeatureType.CATEGORICAL),
    ]

    sut = sample_model_metadata.continuous_features
    assert len(sut) == 1
    assert sut[0].label == 'f4'


def test_metadata_columns_returns_common_metadata_columns(sample_model_metadata):  # noqa: D103
    sut = sample_model_metadata.metadata_columns
    assert 'nml_meta_partition' in sut
    assert 'nml_meta_target' in sut
    assert 'nml_meta_timestamp' in sut


def test_metadata_factory_raises_invalid_args_exception_when_given_unknown_model_type():  # noqa: D103
    with pytest.raises(InvalidArgumentsException, match="could not create metadata for model type 'foo'"):
        _ = ModelMetadataFactory.create(model_type='foo')


@pytest.mark.parametrize(
    'model_type,metadata_class',
    [
        (ModelType.CLASSIFICATION_BINARY, BinaryClassificationMetadata),
        (ModelType.CLASSIFICATION_MULTICLASS, MulticlassClassificationMetadata),
    ],
)
def test_metadata_factory_creates_correct_model_metadata_instance_given_model_type(  # noqa: D103
    model_type, metadata_class
):
    sut = ModelMetadataFactory.create(model_type=model_type)
    assert isinstance(sut, metadata_class)
