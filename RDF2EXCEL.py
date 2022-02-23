import urllib.parse
import rdfpandas
from rdfpandas.graph import to_dataframe
import pandas as pd
import rdflib
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import module_uri_list as uri_list
import module_df_entity as df_entity
import module_aggregate_merged as aggregate_merged
import module_create_counts as create_counts
import module_save_excel as save_excel

############# User Parameters #############
# Specify the start and end number of entities to be process in this module
# To shorten testing time, use only a few entities (e.g. start 0, end 2). To set all entities in a category, see the range below. Best to batch per category, so errors can be found too
# Person 0:19, 0:22, Places 23-42, 23:52, Dates 53:72, Events 73:92, 73:95, Objects 96:115, 96:121
start_batch = 73
end_batch = 95
# Specify the prefix of each file to be produced (Dates_, Events, Places_, Objects_)
fileprefix = 'prop_events_'


print(r'********* Script Started *********')
# Reference to sources in this code
# 0   Worldcat
# 1        LoC
# 2       VIAF
# 3      Getty
# 4   Wikidata
# 5    DBpedia
# 6   BabelNet
# 7   GeoNames
# 8       YAGO
# 9  Europeana

# Include all access URLs and URLs automatically from EXCEL file
#xl_file = pd.ExcelFile('URLsandURIs.xlsx')
xl_file = pd.ExcelFile('ListOfAllURLs_nohttps_for_URIs_and_URLs_GettyWebURIs_BabelNameSpaces_GettyNameSpaces_wikidataNameSpaces_euroURLsURIs_GeoHttpURIs_YagoURIs_2.xlsx')
# Put 2 sheets in DataFrame with the sheetnames
data = {sheet_name: xl_file.parse(sheet_name)
           for sheet_name in xl_file.sheet_names}
#print(entities['ListOfURLs']['YAGO'])
#print(entities['ListOfURIs'].T.loc['Entity'][0])

# # Iterate over all entities and generate CSV separately (ca 3000), and for each category (ca 60,000) all is too long (300,000)
# # Transpose to make a right shape of Dataframe and locate the series (e.g. series for Shakespeare)
# #print(data['ListOfURLs'].T.loc[:,5])
# #print(len(data['ListOfURLs'].index))
for n in range(len(data['ListOfURLs'].index)):
    # To shorten testing time, use only a few entities, set 20 for all entities in a category (e.g. all persons)
    # if n < 2:
    if n < start_batch:
        continue
    elif n >= start_batch and n <= end_batch:
        url = data['ListOfURLs'].T.loc[:,n]
        uri = data['ListOfURIs'].T.loc[:,n]
        # Create dataframe for URLs and URIs of resources
        entities = uri_list.create_uri_df(url, uri)

        # Remove some sources and focus on 2 sources to shorten testing time
        #entities.loc[2:9, ['url', 'uri']] = ''
        #entities.loc[2, ['url', 'uri']] = ''
        #entities.loc[4, ['url', 'uri']] = ''
        #entities.loc[5, ['url', 'uri']] = ''
        #entities.loc[8, ['url', 'uri']] = ''
        print("\n\n*******************************\n List of URIs to be processed \n*******************************\n\n")
        print(entities)
        #print(len(entities))

        # print('Each Entity+++++++++++++++++++')
        # Access URLs and create dataframe for the graph of each entity
        aggregate = df_entity.create_dataframe_entity(entities)
        #print(aggregate)
        # print('Aggregate all entity+++++++++++++++++++')
        # Aggregate each entity
        allagg = aggregate_merged.create_dataframe_agg(aggregate)
    else:
        break

    #print(allagg[-1])
    print('\n\n***********************\n Generating percentage of coverage for each entity \n***********************\n\n')
    # Generate percentage of coverage for each entity
    count = create_counts.count(allagg)
    print('\n\n***********************\n Creating Covertage Stats \n***********************\n\n')
    # Create DataFrame for coverage stats
    coverage_df = create_counts.create_coverage_stats(count, entities)

    # Obtain the entity name for each iteration
    entityname = data['ListOfURIs'].T.loc[:, n].loc['Entity']
    # Save Workbook (2 sheets) as XLSX
    print('\n***********************\n Saving in EXCEL files \n***********************\n')
    save_excel.save_excel(allagg, coverage_df, fileprefix, entityname)
    print('\n***********************\n EXCEL files saved \n***********************\n')
    print('\n***********************\n ALL DONE SUCCESSFULLY \n***********************\n')