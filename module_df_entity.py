import pandas as pd
import urllib.parse
import rdflib
import rdfpandas
from rdfpandas.graph import to_dataframe

# Option A: Check each entity manually
# Set which row to analyse by providing row number in [] as entities to compare (to find the most important data in an entity)
def manual_entity_check(rownumber, entities):
    # URL percent coding
    target = urllib.parse.quote(entities.loc[rownumber, 'url'])
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
            print("\n****** original df ******\n")
            print(df)
            df['entity'] = df.index
            print("\n****** HEAD of df.index ******\n")
            print(df.head)
            # Just testing purpose to check YAGO data (delete after all XSLX created)
            #if entities.loc[i, 'source'] == 'YAGO':
                #csvnumber = entities.loc[i, 'source'] + str(i) + '.csv'
                #df_csv = df.to_csv(csvnumber, index=True, index_label='@id')
            # Check matching rows in the dafafame which includes the entity URI
            print("\n****** df['entity'] ******\n")
            print(df['entity'])
            print("\n****** entities.loc[i, 'uri'] ******\n")
            print(entities.loc[i, 'uri'])
            print("\n****** Selecting ******\n")
            # If Mary,_Mother (not Mary,_mother) exist, do the following (in case of YAGO's problem with URI with 'M' or 'm')
            mary = 'http://dbpedia.org/resource/Mary,_Mother_of_Jesus'
            if df['entity'].str.contains(mary).any() and entities.loc[i, 'source'] == 'YAGO':
                x = df[df['entity'] == mary]
                x_transposed = x.T
                x_transposed['full_coverage'] = x_transposed[mary]
                print(r"****** Checking the case of Mary ******")
                print(x)
            # Dates category has wierd URIs for YAGO, so adjust
            category_uri = entities.loc[i, 'uri'].replace('http://dbpedia.org/resource/', 'http://dbpedia.org/resource/Category:')
            if df['entity'].str.contains(category_uri).any() and entities.loc[i, 'source'] == 'YAGO':
                x = df[df['entity'] == category_uri]
                x_transposed = x.T
                x_transposed['full_coverage'] = x_transposed[category_uri]
                print(r"****** Checking the case of YAGO ******")
                print(x)

            uncle_uri = r" http://yago-knowledge.org/resource/Uncle_Tom's_Cabin"
            uncle_uri2 = r"http://dbpedia.org/resource/Uncle_Tom's_Cabin"
            uncle_uri3 = r"http://dbpedia.org/resource/Uncle_Tom"
            if df['entity'].str.contains(uncle_uri2).any() and entities.loc[i, 'source'] == 'YAGO':
                entities.loc[i, 'uri'].replace(uncle_uri2, uncle_uri3)
                df['entity'].replace(uncle_uri2, uncle_uri3)
                x = df[df['entity'] == entities.loc[i, 'uri']]
                print(r"****** Checking the case of Uncle Toms ******")
                print(x)
                x_transposed = x.T
                x_transposed['full_coverage'] = x_transposed[entities.loc[i, 'uri']]

            else:
                x = df[df['entity'] == entities.loc[i, 'uri']]
                print("\n****** x = df[df['entity'] == entities.loc[i, 'uri']] ******\n")
                print(x)
                print("\n****** x.columns.T ******\n")
                print(x.columns.T)
                x_transposed = x.T
                print("\n****** x_transposed BEFORE dropna ******\n")
                print(x_transposed)

                # Newly added 2 line below will compare property names by string matching. The corresponding literals are still preserved in EXCEL, but as references only
                # Next 1 line added for "Extract all property names 2022-02-14"
                x_transposed = x_transposed.dropna()
                print("\n****** x_transposed AFTER dropna ******\n")
                print(x_transposed)
                # Next 1 line used before "Extract all property names 2022-02-14"
                #x_transposed['full_coverage'] = x_transposed[entities.loc[i, 'uri']]
                # Next 1 line added for "Extract all property names 2022-02-14"
                x_transposed['full_coverage'] = x_transposed.index
            x_transposed.dropna(subset=['full_coverage'], inplace=True)
            print("\n****** x_transposed ******\n")
            print(x_transposed)
            aggregate.append(x_transposed)
            print("\n****** aggregate ******\n")
            print(aggregate)
            # Save dataframe of each entity as CSV (file name is index number (i) in the dataframe)
            #csvnumber = '00000_' + entities.loc[i, 'source'] + str(i) + '.csv'
            #df_csv = x_transposed.to_csv(csvnumber, index=True, index_label='@id')
        else:
            print('\n****** ' + entities.loc[i, 'source'] + ' does not have entity. Try another entity. ******\n')
            #data2 = {'NAME': '', 'full_coverage': ''}
            data2 = {entities.loc[i, 'source'] : '', 'full_coverage': ''}
            y2 = pd.DataFrame(data2, index = ['dc:identifier'])
            print("****** Check if y2 dataframe is empty ******")
            print(y2)
            aggregate.append(y2)
    return(aggregate)