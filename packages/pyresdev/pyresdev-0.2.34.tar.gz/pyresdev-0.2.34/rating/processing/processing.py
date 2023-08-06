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

__all__ = ['preprocessing_training']


def preprocessing_training_common(df, config, model_type, mapping_dicts=None, imp=None):
    """Common functions used for every campaign in the processing

    Args:
        mapping_dicts: dictionaries for mapping strings to floats
        df ([DataFrame]): [Dataframe to split]
        config ([Dict]): [Config for the campaign]
        model_type(dict): model used ( bv, probabiltiy or multiclass)
    Returns:
        [DataFrames]: [Training and testing divided into dependent and independent variables ]
        [imp]: iterative imputer
    """
    # Data engineering part

    df = (df.pipe(utils.reduce_mem_usage)
          .pipe(DEutils.set_dataframe_columntypes)
          .pipe(DEutils.clean_previous_status, status_to_clean=config['status_to_delete'])
          .pipe(DEutils.clean_companytype)
          .pipe(DEutils.fill_na_with_unknown, columns=config['fill_unknown'])
          .pipe(DEutils.create_company_years_column)
          .pipe(DEutils.fill_seniority_column)
          .pipe(DEutils.filter_countries)
          .pipe(DEutils.clean_companyfollowers_text)
          .pipe(DEutils.convert_kwkey_specialties_and_technologies_to_int)
          .pipe(DEutils.fill_variables)
          .pipe(DEutils.impute_growth)
          .pipe(DEutils.log_transformation, columns=config['cols_to_transform'])
          .pipe(DEutils.correct_C80_success_code)
          )

    if imp:
        df = DEutils.impute_nas(df=df, columns_to_impute=config['impute_columns'], imp=imp)
    else:
        df, imp = DEutils.impute_nas_and_save_imputer(df=df, columns_to_impute=config['impute_columns'])
        imputer_name = 'imputer_' + config['campaign'] + '.pkl'
        imputer_output_path = os.path.join('/opt/ml/processing/imputer', imputer_name)
        logging.info('Saving iterative imputer to {}'.format(imputer_output_path))
        pickle.dump(imp, open(imputer_output_path, 'wb'))

    df = DEutils.drop_columns(df, columns=config['cols_to_drop'])

    # creation and application of the dictionaries
    if mapping_dicts is None:
        logger.info("No mapping dicts present, creating them")
        mapping_dicts = {}

        mapping_dicts = DEutils.create_class_dictionaries(df,
                                                          mapping_dicts,
                                                          "MXType")
        df = DEutils.map_conv_prob_using_dictionary(df,
                                                    mapping_dicts,
                                                    'MXType')
        mapping_dicts = DEutils.create_class_dictionaries(df,
                                                          mapping_dicts,
                                                          "State")
        df = DEutils.map_conv_prob_using_dictionary(df,
                                                    mapping_dicts,
                                                    'State')
        mapping_dicts = DEutils.create_class_dictionaries(df,
                                                          mapping_dicts,
                                                          "Industry")
        df = DEutils.map_conv_prob_using_dictionary(df,
                                                    mapping_dicts,
                                                    'Industry')
        mapping_dicts = DEutils.create_class_dictionaries(df,
                                                          mapping_dicts,
                                                          "PreviousContacts")
        df = DEutils.map_conv_prob_using_dictionary(df,
                                                    mapping_dicts,
                                                    'PreviousContacts',
                                                    drop=False)

        mapping_dicts_name = 'mapping_dicts' + config['campaign'] + '.pkl'
        mapping_dicts_output_path = os.path.join('/opt/ml/processing/mapping_dicts', mapping_dicts_name)
        logging.info('Saving dicts to {}'.format(mapping_dicts_output_path))
        pickle.dump(mapping_dicts, open(mapping_dicts_output_path, 'wb'))
    else:
        logging.info("Mapping dicts found! Using them")
        df = DEutils.map_conv_prob_using_dictionary(df,
                                                    mapping_dicts,
                                                    'MXType')

        df = DEutils.map_conv_prob_using_dictionary(df,
                                                    mapping_dicts,
                                                    'State')

        df = DEutils.map_conv_prob_using_dictionary(df,
                                                    mapping_dicts,
                                                    'Industry')
        df = DEutils.map_conv_prob_using_dictionary(df,
                                                    mapping_dicts,
                                                    'PreviousContacts',
                                                    drop=False)

    return df, imp, mapping_dicts


def preprocessing_training(df, config, model_type, mapping_dicts=None, imp=None):
    """[Pre-processing function to prepare the data for training the model and to make predictions]
s
    Args:
        model_type:
        config:
        df:
        df ([Pandas Dataframe]): [Pandas Dataframe with the raw data ]
        industry_dictionary ([Dict]): [Dictionary to reduce the cardinality of the "Industry attribute"]
        config(dict) : Dictionary with the configuration ( read from json)
        model_type(string) : type of the model to be used
        mx_bv_dictionary(string): Dictionary of MX converting to bv performance
        mx_prob_dictionary(string): Dictionary of MX converting to prob performance
        model_type(string) : can be probability, bv or multiclass
    Returns:
        df_clean[Pandas Dataframe]: Pre-processed DataFrame ready for training purposes
        :param mx_prob_dictionary:
        :param use_one_hot_encoding:
        :param mapping_dicts:
    """

    # Make a copy of the dataset
    df_leads_clean = df.copy()

    nna = df_leads_clean.isna().sum()
    logging.info("NA in original dataframe:")
    logging.info(f"{nna}")

    # Convert to categories and 
    df_leads_clean, imp, mapping_dicts = preprocessing_training_common(df=df_leads_clean,
                                                                       config=config,
                                                                       mapping_dicts=mapping_dicts,
                                                                       model_type=model_type,
                                                                       imp=imp)

    df_leads_clean = utils.reduce_mem_usage_category(df=df_leads_clean)

    df_leads_clean = DEutils.one_hot_encoding(df=df_leads_clean)

    df_leads_clean = DEutils.convert_date(df=df_leads_clean)

    df_leads_clean = DEutils.set_target_column(df=df_leads_clean, model_type=model_type)

    nna = df_leads_clean.isna().sum()
    logging.info("NA in final dataframe:")
    logging.info(f"{nna}")

    return df_leads_clean, imp, mapping_dicts
