# Various constants used in the project
# TODO(@Andreasfo@gmail.com)
# Fix this so it is not this ugly :)
dfs = ['df_deaths', 'df_deaths_per_mn', 'df_deaths_1', 'df_deaths_per_mn_1']
plots = {'death': 'df_deaths',
         'confirmed': 'Cases',
         'ICU': 'ICU',
         'mobility_index': 'mobility',
         'per_million': 'million',
         'political': 'politics'}
countries = ['Sweden', 'Finland', 'Denmark', 'Norway', 'Iceland']
active_map = ["map_death", 'map_total_cases',
              'map_iva_patients', 'mobility_map']
titles = {'df_deaths': 'COVID19 Total Nordic Deaths, starting March 10 2020',
          'df_deaths_per_mn': 'COVID19 Total Nordic Deaths per Mn inhabitants, starting March 10 2020',
          'df_deaths_1': 'COVID19 Total Nordic Deaths, daily data since first death',
          'df_deaths_per_mn_1': 'COVID19 Total Nordic Deaths per Mn inhabitants, daily data since first death'}
x_axis_labels = {'df_deaths': 'Date',
                 'df_deaths_per_mn': 'Date',
                 'df_deaths_1': 'Days since first Death',
                 'df_deaths_per_mn_1': 'Days since first Death'}
y_axis_labels = {'df_deaths': 'Deaths',
                 'df_deaths_per_mn': 'Deaths per Mn inhabitants',
                 'df_deaths_1': 'Deaths',
                 'df_deaths_per_mn_1': 'Deaths per Mn inhabitants'}

legends = {'df_deaths': 'Deaths',
           'Cases': 'Confirmed Cases',
           'ICU': 'Intensive Care',
           'mobility': 'Mobility ', }
colors = {'Sweden': 'blue',
          'Denmark': 'red',
          'Norway': 'orange',
          'Finland': 'black',
          'Iceland': 'magenta'}
lines = {'df_deaths': 'solid',
         'Cases': 'dash',
         'ICU': 'dashdot'}

yaxis = {}

pops = {'Sweden': 10.036379,
        'Denmark': 5.771876,
        'Norway': 5.378857,
        'Finland': 5.532156,
        'Iceland': 0.339031}

fillcolors = {'Denmark': 'rgba(255, 0, 0, 0.05)',
              'Sweden': 'rgba(0,0,255,0.05)', }
