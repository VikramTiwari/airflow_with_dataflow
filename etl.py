import argparse
import csv
import datetime
import json
import logging
import os
import sys
import tempfile
from datetime import date, timedelta
from time import gmtime, strftime

import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import (GoogleCloudOptions,
                                                  PipelineOptions,
                                                  SetupOptions,
                                                  StandardOptions,
                                                  WorkerOptions)

import Common
import numpy as np
import pandas as pd

job_id = ''.join(e for e in str(datetime.datetime.now()) if e.isalnum())
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BUCKET_URL = 'gs://us-central1-devbeta-c264d68e-bucket'  # replace with your bucket name
PROJECT_ID = 'ivikramtiwari'  # replace with your project id
JOB_NAME = 'etl-test-' + job_id  # replace with your job name


class ETL(beam.DoFn):
    def __init__(self, request):
        super(ETL, self).__init__()
        self._request = request

    def process(self, element):
        logging.info('Starting job: ETL')
        logging.info(self._request)
        etl(self._request)
        logging.info('Job finished')


def etl(request):
    logging.info('etl init')
    logging.info(request)
    request['floating_start_date'] = Common.Utils.string_to_float(
        request['start_date'])
    request['floating_end_date'] = Common.Utils.string_to_float(
        request['end_date'])
    request['config'] = Common.Utils.get_config()
    logging.info(request)
    logging.info('etl end')


def run(argv=None):
    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--runner',
        dest='runner',
        default='DirectRunner',
        help='DirectRunner or DataflowRunner')

    parser.add_argument(
        '--start_date',
        dest='start_date',
        default='2018-01-01',
        help='Start date')

    parser.add_argument(
        '--end_date', dest='end_date', default='2018-01-02', help='End date')

    known_args, extra_pipeline_options = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions()
    pipeline_options.view_as(SetupOptions).save_main_session = True

    logging.info('Basic pipeline options ready')

    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    google_cloud_options.project = PROJECT_ID
    google_cloud_options.job_name = JOB_NAME
    google_cloud_options.staging_location = BUCKET_URL + '/dataflow_runner/staging'
    google_cloud_options.temp_location = BUCKET_URL + '/dataflow_runner/temp'

    logging.info('Google cloud pipeline options are ready')

    pipeline_options.view_as(StandardOptions).runner = known_args.runner

    logging.info('Runner is set')

    p = beam.Pipeline(options=pipeline_options)

    request = {
        'start_date': known_args.start_date,
        'end_date': known_args.end_date
    }

    init = p | 'Begin pipeline' >> beam.Create([0]) | 'Run ETL' >> beam.ParDo(
        ETL(request))

    logging.info('Pipeline structured')

    result = p.run()
    logging.info('Pipeline running')

    result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
