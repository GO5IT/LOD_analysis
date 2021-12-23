import pandas as pd
# Create dataframe for URLs and URIs of resources
def create_uri_df(url, uri):
    # Merge two series from two sheets
    merged = pd.concat([url, uri], axis=1)
    # Replace NaN with empty cell
    merged_null = merged.fillna('')
    # Dataframe cleanup by dropping unneeded rows, resetting index, naming columns
    entities = merged_null.drop(merged_null.index[0:2])
    entities.reset_index(inplace=True)
    entities.columns = ['source', 'url', 'uri']
    #print(entities)

    # If some URLs do not work, you can omit them below, by replacing problematic URLs and URLs with empty (e.g. Wikidata and Europeana)
    #entities.loc[3:5, ['url', 'uri']] = ''
    #entities.loc[4, ['url', 'uri']] = ''
    #entities.loc[9, ['url', 'uri']] = ''
    #print(entities)
    return(entities)