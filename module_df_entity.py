import pandas as pd
import rdflib
import rdfpandas
from rdfpandas.graph import to_dataframe

# Option A: Check each entity manually
# Set which row to analyse by providing row number in [] as entities to compare (to find the most important data in an entity)
def manual_entity_check(rownumber, entities):
    target = entities.loc[rownumber, 'url']
    target2 = entities.loc[rownumber, 'uri']
    name = entities.loc[rownumber, 'source']
    # If dataframe is not empty ('')
    if target != '':
        print('\n\n***********************\nWorking on ' + name + '\n***********************\n\n')
        g = rdflib.Graph()
        g.parse(target, format = 'xml')
        df = to_dataframe(g)
        df['entity'] = df.index
        print(df)
        # Exact match
        x = df[df['entity'] == target2]
        #Test: Get rows that contain specified text (in this case a string from dataframe)(not used)
        #x = df.loc[df['entity'].str.contains(target2, regex=False)]
        x_transposed = x.T
        print(x_transposed)
        # #Saving as CSV file
        #df_csv = x_transposed.to_csv('Manual_Entity_Check.csv', index=True, index_label='@id')
        return(x_transposed)
    else:
        print('\n\n   ***\n   ' + name + ' does not have entity. Try another entity!!\n   ***\n\n')

# Option B: Create dataframe for each entity automatically
def create_dataframe_entity(entities):
    aggregate = []
    for i in range(len(entities)):
        print('\n\n***********************\nWorking on ' + entities.loc[i, 'source'] + '\n***********************\n\n')
        if entities.loc[i, 'url'] != '':
            g = rdflib.Graph()
            # Wikidata works only with ttl
            if entities.loc[i, 'source'] == 'Wikidata':
                g.parse(entities.loc[i, 'url'], format = 'ttl')
            else:
                g.parse(entities.loc[i, 'url'], format = 'xml')
            df = to_dataframe(g)
            df['entity'] = df.index
            print(df.head)
            # Just testing purpose to check YAGO data (delete after all XSLX created)
            if entities.loc[i, 'source'] == 'GeoNames':
                csvnumber = entities.loc[i, 'source'] + str(i) + '.csv'
                df_csv = df.to_csv(csvnumber, index=True, index_label='@id')
            # Check matching rows in the dafafame which includes the entity URI
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            print(df['entity'])
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            print(entities.loc[i, 'uri'])
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            # If Mary,_Mother (not Mary,_mother) exist, do the following (in case of YAGO's problem with URI with 'M' or 'm')
            mary = 'http://dbpedia.org/resource/Mary,_Mother_of_Jesus'
            if df['entity'].str.contains(mary).any() and entities.loc[i, 'source'] == 'YAGO':
                x = df[df['entity'] == mary]
                x_transposed = x.T
                x_transposed['full_coverage'] = x_transposed[mary]
                print(x)
                print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            # Dates category has wierd URIs for YAGO, so adjust
            category_uri = entities.loc[i, 'uri'].replace('http://dbpedia.org/resource/', 'http://dbpedia.org/resource/Category:')
            if df['entity'].str.contains(category_uri).any() and entities.loc[i, 'source'] == 'YAGO':
                x = df[df['entity'] == category_uri]
                x_transposed = x.T
                x_transposed['full_coverage'] = x_transposed[category_uri]
                print(x)
                print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            else:
                x = df[df['entity'] == entities.loc[i, 'uri']]
                print(x)
                print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
                x_transposed = x.T
                x_transposed['full_coverage'] = x_transposed[entities.loc[i, 'uri']]
            x_transposed.dropna(subset=['full_coverage'], inplace=True)
            print(x_transposed)
            aggregate.append(x_transposed)
            #print(aggregate)
            # Save dataframe of each entity as CSV (file name is index number (i) in the dataframe)
            #csvnumber = entities.loc[i, 'source'] + str(i) + '.csv'
            #df_csv = x_transposed.to_csv(csvnumber, index=True, index_label='@id')
        else:
            print('\n\n   ***\n   ' + entities.loc[i, 'source'] + ' does not have entity. Try another entity!!\n   ***\n\n')
            print('----------------')
            #data2 = {'NAME': '', 'full_coverage': ''}
            data2 = {entities.loc[i, 'source'] : '', 'full_coverage': ''}
            y2 = pd.DataFrame(data2, index = ['dc:identifier'])
            print(y2)
            aggregate.append(y2)
            # print('----------------')
            # # Create an empty dataframe
            # data = {'dc:identifier{Literal}': [''], 'entity': [entities.loc[i, 'source']]}
            # #data = {str(entities.loc[i, 'uri']): [''], 'full_coverage': ['']}
            # y = pd.DataFrame(data)
            # print('----------------')
            # print(y)
            # print('----------------')
            # print(entities.loc[i, 'source'])
            # y['entity'] = y.index
            # print('----------------')
            # print(y)
            # y_transposed = y.T
            # #y_transposed['full_coverage'] = y_transposed[entities.loc[i, 'source']]
            # #y_transposed['full_coverage'] = y_transposed['dc:identifier{Literal}']
            # #y_transposed.dropna(subset=['full_coverage'], inplace=True)
            # print(y_transposed)
            # aggregate.append(y)
    return(aggregate)