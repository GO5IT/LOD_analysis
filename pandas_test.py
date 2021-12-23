import pandas as pd

coverage = {'source': [], 'count': [], 'percentage': []}
coverage_df = pd.DataFrame(coverage)
coverage_df.loc[-1] = [2, 3, 4]
#new = {'source': ['asde', 'afew', 'tttt']}
#coverage_df.append(new, ignore_index=True)
print(coverage_df)