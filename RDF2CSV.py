import pickle
import rdfpandas
from rdfpandas.graph import to_dataframe
import pandas as pd
import rdflib

# Wikidata generates an error with "rdf:nodeID value is not a valid NCName"
# Create an array for entity URIs
data = {
'source' : ['Worldcat', 'LoC', 'VIAF', 'Getty',	'Wikidata', 'DBpedia', 'BabelNet', 'GeoNames', 'YAGO', 'Europeana'],
# Below is the list of entities to be accessed (with file extention)
'url' : ['http://id.worldcat.org/fast/1037825.rdf.xml',
'https://id.loc.gov/authorities/subjects/sh97003090.rdf',
'',
'',
#'https://www.wikidata.org/wiki/Special:EntityData/Q2648.rdf',
'',
#'http://dbpedia.org/resource/1967',
'',
'http://babelnet.org/rdf/data/s02830721n?output=xml',
'',
'',
''],
# Below is the list of URIs to be searched (without file extention except BabelNet. Watchout also https)
'uri' : ['http://id.worldcat.org/fast/1037825',
'http://id.loc.gov/authorities/subjects/sh97003090',
'',
'',
#'http://www.wikidata.org/entity/Q2648',
'',
#'http://dbpedia.org/resource/1967',
'',
'http://babelnet.org/rdf/data/s02830721n?output=xml',
'',
'',
'']
}
entities = pd.DataFrame(data)
print(entities)

# Option A: Check each entity manually
# Set which row to analyse by providing row number in [] as entities to compare (to find the most important data in an entity)
# rownumber = 6
# target = entities.loc[rownumber, "url"]
# target2 = entities.loc[rownumber, "uri"]
# name = entities.loc[rownumber, "source"]
# # If dataframe is not empty ("")
# if target != "":
#     print('\n\n***********************\nWorking on ' + name + '\n***********************\n\n')
#     g = rdflib.Graph()
#     g.parse(target, format = 'xml')
#     df = to_dataframe(g)
#     df['entity'] = df.index
#     print(df)
#     # Exact match
#     x = df[df['entity'] == target2]
#     #Test: Get rows that contain specified text (in this case a string from dataframe)(not used)
#     #x = df.loc[df["entity"].str.contains(target2, regex=False)]
#     x_transposed = x.T
#     print(x_transposed)
#     # #Saving as CSV file
#     df_csv = x_transposed.to_csv('testrdf3.csv', index=True, index_label="@id")
# else:
#     print('\n\n***********************\n' + name + ' does not have entity. Try another entity!!\n***********************\n\n')

# Option B: Create dataframe for each entity automatically
aggregate = []
# create dataframe for each entity
for i in range(len(entities)):
    print('\n\n***********************\nWorking on ' + entities.loc[i, "source"] + '\n***********************\n\n')
    if entities.loc[i, "url"] != "":
        g = rdflib.Graph()
        g.parse(entities.loc[i, "url"], format = 'xml')
        df = to_dataframe(g)
        df['entity'] = df.index
        #print(df.head)
        # Check matching rows in the dafafame which includes the entity URI
        x = df[df['entity'] == entities.loc[i, "uri"]]
        x_transposed = x.T
        x_transposed['full_coverage'] = x_transposed[entities.loc[i, "uri"]]
        #print(x_transposed)
        aggregate.append(x_transposed)
        #print(aggregate)
        if i != 0:
            print("+++++++++++++++++++")
            # print(aggregate[1])
            #next = x_transposed
            #print(aggregate)
            #merged = aggregate[i-1].merge(aggregate[i], on='full_coverage', how='outer')
            #print(merged)
            #df_csv = merged.to_csv('merged.csv', index=True, index_label="@id")
            #x = df[df['entity'] == "http://dbpedia.org/resource/1967"]
            #print(x)
            #Saving as CSV file
            #csvnumber = str(i) + '.csv'
            #df_csv = x_transposed.to_csv(csvnumber, index=True, index_label="@id")
    else:
        print('\n\n***********************\n' + entities.loc[i, "source"] + ' does not have entity. Try another entity!!\n***********************\n\n')
# Option X: Check 2 dataframes manually
# #print(aggregate[1])
# aggregate[0].dropna(subset = ['full_coverage'], inplace=True)
# aggregate[1].dropna(subset = ['full_coverage'], inplace=True)
# # Save as CSV
# agg1 = aggregate[0].to_csv('merge_world.csv', index=True, index_label="@id")
# agg2 = aggregate[1].to_csv('merge_loc.csv', index=True, index_label="@id")
# merged = aggregate[0].merge(aggregate[1].drop_duplicates(), on='full_coverage', how='outer', indicator=True, validate='many_to_many')
# #print(merged)
# merged_csv = merged.to_csv('merged.csv', index=True, index_label="@id")

# Option Y: Create all aggregated automatically
allagg = []
#print(aggregate)
for ii in range(len(aggregate)):
    aggregate[ii].dropna(subset=['full_coverage'], inplace=True)
    if ii == 0:
        #merged = aggregate[0].merge(aggregate[1].drop_duplicates(), on='full_coverage', how='outer', indicator=True, validate='many_to_many')
        merged = aggregate[0].merge(aggregate[1].drop_duplicates(), on='full_coverage', how='outer', validate='many_to_many')
        #print(merged)
        allagg.append(merged)
        print(allagg)
    elif ii < len(aggregate)-2:
        #print(aggregate[ii])
        #df_csv = aggregate[ii].to_csv('allagg_test.csv', index=True, index_label="@id")
        #ii = ii - 2
        #print(allagg[1])
        print(str(ii) + "th iteration/n+++++++++++++++++++")
        print(len(allagg))
        #merged = allagg[ii-1].merge(aggregate[ii+1].drop_duplicates(), on='full_coverage', how='outer', validate='many_to_many')
        merged = allagg[ii - 1].merge(aggregate[2].drop_duplicates(), on='full_coverage', how='outer',
                                      validate='many_to_many')
        allagg.append(merged)
        print(allagg[-1])

#print("+++++++++++++++++++")
#print(allagg)
#print(allagg[-1])
#allagg_csv = allagg.to_csv('allagg.csv', index=True, index_label="@id")

# #Saving as CSV file
#df_csv = x.to_csv('testrdf3.csv', index = True, index_label = "@id")
# #Saving as Pickle file
# with open('testrdf.pkl', 'wb') as f:
#     pickle.dump(df, f)
# #Reading Pickle file
# with open('testrdf.pkl', 'rb') as f:
#     df = pickle.load(f)
# df['entity'] = df.index
# print(df.head)
#
# x = df[df['entity'] == "http://dbpedia.org/resource/1967"]
# print(x)
# # #Saving as CSV file
# df_csv = x.to_csv('testrdf2.csv', index = True, index_label = "@id")