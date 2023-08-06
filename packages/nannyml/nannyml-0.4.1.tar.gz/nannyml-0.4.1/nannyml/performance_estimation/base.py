#  Author:   Niels Nuyttens  <niels@nannyml.com>
#
#  License: Apache Software License 2.0

"""Module containing base classes for performance estimation."""
from __future__ import annotations

import abc
from typing import List

import pandas as pd
import plotly.graph_objects as go

from nannyml.chunk import Chunker, CountBasedChunker, DefaultChunker, PeriodBasedChunker, SizeBasedChunker
from nannyml.metadata import ModelMetadata


class PerformanceEstimatorResult(abc.ABC):
    """Contains performance estimation results and provides additional functionality on them."""

    def __init__(self, estimated_data: pd.DataFrame, model_metadata: ModelMetadata):
        """Creates a new DriftResult instance.

        Parameters
        ----------
        estimated_data: pd.DataFrame
            The results of the :meth:`~nannyml.performance_estimation.base.PerformanceEstimator.estimate` call.
        model_metadata: ModelMetadata
            The metadata describing the monitored model.
        """
        self.data = estimated_data.copy(deep=True)
        self.metadata = model_metadata

    def plot(self, *args, **kwargs) -> go.Figure:
        """Plot drift results."""
        raise NotImplementedError


class PerformanceEstimator(abc.ABC):
    """Abstract class for performance estimation."""

    def __init__(
        self,
        model_metadata: ModelMetadata,
        features: List[str] = None,
        chunk_size: int = None,
        chunk_number: int = None,
        chunk_period: str = None,
        chunker: Chunker = None,
    ):
        """Creates a new instance of a performance estimator.

        Parameters
        ----------
        model_metadata: ModelMetadata
            Metadata telling the DriftCalculator what columns are required for drift calculation.
        features: List[str]
            An optional list of feature column names. When set only these columns will be included in the
            drift calculation. If not set it will default to all feature column names.
        chunk_size: int
            Splits the data into chunks containing `chunks_size` observations.
            Only one of `chunk_size`, `chunk_number` or `chunk_period` should be given.
        chunk_number: int
            Splits the data into `chunk_number` pieces.
            Only one of `chunk_size`, `chunk_number` or `chunk_period` should be given.
        chunk_period: str
            Splits the data according to the given period.
            Only one of `chunk_size`, `chunk_number` or `chunk_period` should be given.
        chunker : Chunker
            The `Chunker` used to split the data sets into a lists of chunks.

        """
        self.model_metadata = model_metadata
        if not features:
            features = [f.column_name for f in self.model_metadata.features]
        self.selected_features = features

        if chunker is None:
            if chunk_size:
                self.chunker = SizeBasedChunker(chunk_size=chunk_size)  # type: ignore
            elif chunk_number:
                self.chunker = CountBasedChunker(chunk_count=chunk_number)  # type: ignore
            elif chunk_period:
                self.chunker = PeriodBasedChunker(offset=chunk_period)  # type: ignore
            else:
                self.chunker = DefaultChunker()  # type: ignore
        else:
            self.chunker = chunker  # type: ignore

    def fit(self, reference_data: pd.DataFrame) -> PerformanceEstimator:
        """Fits the data on a reference data set."""
        raise NotImplementedError

    def estimate(self, data: pd.DataFrame) -> PerformanceEstimatorResult:
        """Estimate performance given a data set lacking ground truth."""
        raise NotImplementedError
