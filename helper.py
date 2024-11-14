import numpy as np
from fontTools.subset import subset


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally= medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold']+ medal_tally['Silver']+medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')




    return medal_tally
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)

    return nations_over_time

def most_successful(df, sport):
    # Remove rows with missing Medal values
    temp_df = df.dropna(subset=['Medal'])

    # Filter by specific sport if given
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    #return temp_df['Name'].value_counts().reset_index()

    # Count medals by athlete name and get the top 15
    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'Total Medal']  # Rename columns

    # Merge to get additional athlete info
    return top_athletes.merge(df, on='Name', how='left')[['Name','Total Medal','Sport','region']].drop_duplicates('Name')

def most_successful_for_country(df, region):
    # Remove rows with missing Medal values
    temp_df = df.dropna(subset=['Medal'])

    # Filter by specific sport if given
    if region != 'Overall':
        temp_df = temp_df[temp_df['region'] == region]

    #return temp_df['Name'].value_counts().reset_index()

    # Count medals by athlete name and get the top 15
    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'Total Medal']  # Rename columns

    # Merge to get additional athlete info
    return top_athletes.merge(df, on='Name', how='left')[['Name','Total Medal','Sport','region']].drop_duplicates('region')

def yearwise_medal_tally(df,country):
       temp_df = df.dropna(subset=['Medal'])
       temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

       new_df = temp_df[temp_df['region'] == country]
       final_df = new_df.groupby('Year').count()['Medal'].reset_index()

       return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_bc(df, country):
    # Remove rows with missing Medal values
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'Total Medal']  # Rename columns

    # Merge to get additional athlete info
    return x.merge(df, on='Name', how='left')[['Name','Total Medal','Sport']].drop_duplicates('Name')

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()


    men.rename(columns={'Name': 'Men_Count'}, inplace=True)
    women.rename(columns={'Name': 'Women_Count'}, inplace=True)

    # Merge male and female data on 'Year'
    final = men.merge(women, on='Year', how='left')

    # Fill any missing values with 0 (for years without any female athletes, for example)
    final.fillna(0, inplace=True)
    return final
