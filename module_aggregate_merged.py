#Option X: Check 2 dataframes manually and save as CSVs
def manual_dataframe_check(aggregate):
    # Select number in [] to specify 2 sources
    aggregate[0].dropna(subset = ['full_coverage'], inplace=True)
    aggregate[1].dropna(subset = ['full_coverage'], inplace=True)
    # Save as CSV
    agg1 = aggregate[0].to_csv('Manual_BeforeMerge_world.csv', index=True, index_label='@id')
    agg2 = aggregate[1].to_csv('Manual_BeforeMerge_loc.csv', index=True, index_label='@id')
    merged = aggregate[0].merge(aggregate[1].drop_duplicates(), on='full_coverage', how='outer', indicator=True, validate='many_to_many')
    #print(merged)
    merged_csv = merged.to_csv('Manual_AfterMerge.csv', index=True, index_label='@id')
    return(merged)

# Option Y: Create merged dataframe from all aggregated dataframes automatically
def create_dataframe_agg(aggregate):
    # Set an empty array to store dataframes
    allagg = []
    #print(aggregate)
    #print('+++++++++++++++++++')
    # If there are 0 or 1 dataframe (no merge)
    if len(aggregate) == 1 | 0:
        print('\n****** Only 1 dataframe: no merge is possible ******\n')
    # If there are only 2 dataframes to merge, simple merging
    elif len(aggregate) == 2:
        print('\n****** Only 2 dataframes ******\n')
        # Indicator causes duplicate column problem from 2nd merge, thus deactivated
        # merged = aggregate[0].merge(aggregate[1].drop_duplicates(), on='full_coverage', how='outer', indicator=True, validate='many_to_many')
        merged = aggregate[0].merge(aggregate[1].drop_duplicates(), on='full_coverage', how='outer', validate='many_to_many')
        allagg.append(merged)
        #print(allagg)
    # If there are more than 3 dataframes to merge, loop over dataframes in the aggregate array (created above) until it there is no more dataframes to merge
    # Put all dataframes in a new allagg array
    else:
        for ii in range(len(aggregate)):
            if ii == 0:
                print('\n****** Working on ' + str(ii) + 'st merge ' + '******')
                # Indicator causes duplicate column problem from 2nd merge, thus deactivated
                #merged = aggregate[0].merge(aggregate[1].drop_duplicates(), on='full_coverage', how='outer', indicator=True, validate='many_to_many')
                merged = aggregate[ii].merge(aggregate[ii+1].drop_duplicates(), on='full_coverage', how='outer', validate='many_to_many')
                #merged = aggregate[ii].merge(aggregate[ii+1].drop_duplicates(), on=aggregate[ii].index, how='outer', validate='many_to_many')
                allagg.append(merged)
                #print(allagg)
            elif ii <= len(aggregate)-2:
                print('\n****** Working on ' + str(ii) + 'th merge ' + '******')
                # print(len(allagg))
                merged = allagg[ii-1].merge(aggregate[ii+1].drop_duplicates(), on='full_coverage', how='outer', validate='many_to_many')
                allagg.append(merged)
                #print(allagg)
    return(allagg)