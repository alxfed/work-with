# -*- coding: utf-8 -*-
"""...
"""
from socradata import meta
import pandas as pd
import numpy as np
from datetime import datetime


def main():
    '''
    output_file_path = '/home/alxfed/archive/all_chicago_datasets.csv'
    catalog = pd.DataFrame()
    sections = ['resource', 'classification', 'metadata', 'permalink', 'link', 'preview_image_url', 'owner']
    row = {}
    all_datasets = meta.all_chicago_datasets()
    for dataset in all_datasets:
        row = dataset['resource']
        catalog = catalog.append(row, sort=False, ignore_index=True)
    output = catalog.reindex(columns=['name', 'id', 'data_updated_at', 'description' ])
    output.to_csv(output_file_path, index=False)
    print('Downloaded all Chicago datasets')
    '''
    metadata = meta.dataset_meta('ydr8-5enu')
    datatypes_dict = {'text': object, 'calendar_date': np.datetime64, 'number': np.float64, 'point': object}
    # there are also np.float32, np.int32 and np.int64,
    # inp = pd.read_json(metadata, typ='series')

    '''
    "resource" :
                {"name" : "Building Permits",
            "id" : "ydr8-5enu",
            "parent_fxf" : null,
            "description" : ''
            "attribution" : "City of Chicago",
            "attribution_link" : "http://www.cityofchicago.org",
            "contact_email" : null,
            "type" : "dataset",
            "updatedAt" : "2019-11-11T13:06:02.000Z",
            "createdAt" : "2011-09-30T12:00:08.000Z",
            "metadata_updated_at" : "2019-07-15T18:02:08.000Z",
            "data_updated_at" : "2019-11-11T13:06:02.000Z",
            "page_views" : {}
            "columns_name" :[]
            "columns_field_name" : []
            "columns_datatype" :
              ["text",
              "calendar_date",
              "number",
              "point"]
            "columns_description" :[]
            "columns_format" : []
            "classification" : {}
            "metadata" : { 
                "domain" : "data.cityofchicago.org",
                "license" : "See Terms of Use"
                }
            "permalink" : "https://data.cityofchicago.org/d/ydr8-5enu",
            "link" : "https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu",
            "owner" : { "id" : "scy9-9wg4", "display_name" : "cocadmin" }
        }
                
    '''
    return


if __name__ == '__main__':
    main()
    print('main - done')