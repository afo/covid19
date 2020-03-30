import requests
import datetime

def death_update():

    url = 'https://www.worldometers.info/coronavirus/'

    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(url, headers=header)

    dfs = pd.read_html(r.text)
    df = dfs[0]

    df = df[['Country,Other','TotalDeaths']]
    
    df.columns = ['Date','Deaths']

    df = df.transpose()

    df.columns = df.loc['Date']

    df = df.drop('Date')
    
    df.index = [datetime.datetime.now().date()]
    
    df.set_index
    
    return(df)
