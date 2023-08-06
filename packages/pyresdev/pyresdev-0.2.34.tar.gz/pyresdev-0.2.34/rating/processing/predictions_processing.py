import logging
# General
import os
import pickle

import pandas as pd

import pyresdev.utils as utils
import pyresdev.utils.data_engineering_functions as DEutils

# Data
# ML
# Used in : Data_Engineering

logger = logging.getLogger(__name__)


def preprocessing_predictions(df, imputer, mapping_dicts: dict, config: dict, training_sample, fill_value=0):

    df = (df.pipe(utils.reduce_mem_usage).
          pipe(DEutils.set_dataframe_columntypes)
          .pipe(DEutils.clean_companytype)
          .pipe(DEutils.fill_na_with_unknown,
                columns=config['fill_unknown'])
          .pipe(DEutils.create_company_years_column)
          .pipe(DEutils.fill_seniority_column)
          .pipe(DEutils.clean_companyfollowers_text)
          .pipe(DEutils.filter_countries)
          .pipe(DEutils.convert_kwkey_specialties_and_technologies_to_int)
          .pipe(DEutils.fill_variables)
          .pipe(DEutils.impute_growth)
          .pipe(DEutils.impute_nas,
                columns_to_impute=config['impute_columns'],
                imp=imputer)
          .pipe(DEutils.log_transformation,
                columns=config['cols_to_transform'])
          .pipe(DEutils.map_conv_prob_using_dictionary,
                mapping_dicts,
                'MXType')
          .pipe(DEutils.map_conv_prob_using_dictionary,
                mapping_dicts,
                'State')
          .pipe(DEutils.map_conv_prob_using_dictionary,
                mapping_dicts,
                'Industry')
          .pipe(DEutils.map_conv_prob_using_dictionary,
                mapping_dicts,
                'PreviousContacts',
                drop=True,
                )
          .pipe(DEutils.drop_columns,
                columns=config['cols_to_drop'])
          .pipe(utils.reduce_mem_usage_category)
          .pipe(DEutils.one_hot_encoding)
          .pipe(DEutils.align_dataframe_with_sample,
                training_sample,
                fill_value,
                predictions_flag=True)
          )
    return df
