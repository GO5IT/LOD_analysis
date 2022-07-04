import pandas as pd
# Generate percentage of coverage for each entity
def count(allagg):
    # Count the number of data
    count = allagg[-1].count(0)
    print("\n****** count ******\n")
    print(count)
    #Change series into dataframe
    count2 = allagg[-1].count().to_frame()
    # Replace 1 (i.e. resource with no entity was temporarily assigned 1) with 0
    for iii in range(len(count2)):
        #print(count2.iloc[iii, 0])
        if count2.iloc[iii, 0] == 1:
            count2.iloc[iii, 0] = 0
        else:
            continue
    # full_coverage contains an empty data that overlaps across all entities, so 1 should be deducted
    count2.loc['full_coverage', 0] = count2.loc['full_coverage', 0] - 1
    print("\n****** count2 ******\n")
    print(count2)
    return(count2)

# Create DataFrame for coverage stats
def create_coverage_stats(count,entities):
    coverage = {'uri': [], 'count': [], 'gap': [], 'percentage': []}
    coverage_df = pd.DataFrame(coverage)
    # print(coverage_df)
    # print(count)
    # print(count.loc['full_coverage', 0])
    # Iterate over count
    for n in range(len(count)):
        gap = count.loc['full_coverage',0] - count.iloc[n,0]
        #print(gap)
        rate = str(count.iloc[n,0] / count.loc['full_coverage',0] * 100) + '%'
        #print(rate)
        #print(count.index[n])
        #coverage_df.loc[n,:] = [count.index[n], count[n], gap, rate]
        coverage_df.loc[n,['uri','count','gap','percentage']] = [count.index[n],count.iloc[n,0], gap, rate]
    # Insert 'full_coverage' in coverage_df dataframe
    # if entities.loc[entities['uri'] == '']:
    #     coverage_df.loc[0.5] = str(entities.loc['source']), '','',''
    #     coverage_df = coverage_df.sort_index().reset_index(drop=True)
    #print(coverage_df)

    # Insert count column at the end of entities dataframe, and if uri is empty, put 0
    entities.insert(3, 'count', '')
    entities.insert(4, 'gap', '')
    entities.insert(5, 'percentage', '')
    #entities.loc[entities['uri'] == '', 'count'] = 0
    entities.loc[entities['uri'] == '', 'gap'] = 0
    entities.loc[entities['uri'] == '', 'percentage'] = 0
    #print(entities)

    # Insert 'full_coverage' in entities dataframe
    entities.loc[0.5] = 'full_coverage', '','','','',''
    entities = entities.sort_index().reset_index(drop=True)
    #print(entities)
    # Combine 2 dataframes and reorder columns
    merge_coverage = coverage_df.combine_first(entities)
    merge_coverage = merge_coverage[['source', 'uri', 'url','count','gap','percentage']]
    #merge_coverage = entities.combine_first(coverage_df)
    # Merge with default shape of dataframe 'entities'
    #merge_coverage = pd.merge(entities, coverage_df, on=['uri', 'count'], how='outer')
    # Drop empty columns, but somehow only works to remove one by one
    #del merge_coverage['source']
    #del merge_coverage['url']
    #merge_coverage.drop(['source'], axis=1)
    #merge_coverage.drop(columns=['source', 'url'])
    #merge_coverage.drop(merge_coverage.columns[0:1], axis=1)

    #print(coverage_df)
    print("\n****** merge_coverage ******\n")
    print(merge_coverage)
    #return(coverage_df)
    return(merge_coverage)