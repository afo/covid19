### Description

[covid19nordics.se](covid19nordics.se) is an open source dashboard to visualize Covid-19 related data for the Nordic countries, including reported cases, deaths, mobility data, timeline of political decisions.

The data is presented in dynamic graphs and maps which are easy to overview and understand even for a layman. Time stamps for data points and events are available and can be adjusted. The information can be used to analyse the effect of political actions done by a country. Mobility data shows how travel habits have evolved during the crisis, per day and region.

Individuals can see mobility trends, confirmed cases and deaths in their region and how it evolves over time. Based on the assumption that less mobility leads to less virus spread and deaths, this data can have a positive impact if people reduce their mobility and social interactions.

Decision makers can get an easy overview of the status in their country as well as other countries. They can base their decisions on the most recent and reliable data.


The Nordic countries are not testing broadly, therefore the recorded number of deaths is a more reliable measure to use in order to assess the impact of the disease in each country.

It's interesting to track the developments because these countries are very similar, but they have implemented very different mitigation strategies -- see e.g.: [https://www.nytimes.com/2020/03/28/world/europe/sweden-coronavirus.html](https://www.nytimes.com/2020/03/28/world/europe/sweden-coronavirus.html)

The plots are updated every 30mins with the most recent data.

### Data Sources

* COVID19 death data: [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19)
* Population data (July 1st 2019): [https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)](https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations))
* Number of physicians and nurses Sweden Per region Socialstyrelsen [https://www.socialstyrelsen.se/statistik-och-data/statistik/statistikamnen/halso-och-sjukvardspersonal/](https://www.socialstyrelsen.se/statistik-och-data/statistik/statistikamnen/halso-och-sjukvardspersonal/) Excel 2018 Annual 2020-04-04 No
* New cases of Covid-19 Sweden Per region Folkhälsomyndigheten [https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/](https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/) Excel 2020-04-04 Daily 2020-04-05 2020-04-04 To be implemented
* Total cases, deaths & ICU Sweden Per region Folkhälsomyndigheten [https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/](https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/bekraftade-fall-i-sverige/) Excel 2020-04-04 Daily 2020-04-05 2020-04-04 To be implemented
* Mobility index Sweden Per region Google [https://www.google.com/covid19/mobility/](https://www.google.com/covid19/mobility/) PDF and plots 2020-03-29 Random(weekly?) 2020-04-04 To be implemented
* Covid-19 confirmed, recovered & deaths Global Per country Johns Hopkins University Center for Systems Science and Engineering [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19) csv 2020-04-04 Daily 2020-04-06 2020-04-05 Yes
* Population Global Per country Wikipedia [https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)](https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)) table 2019-07-01 Annual 2020-07-01 ? ?
* Covid-19 confirmed, recovered & deaths Global Per country Worldometers [https://www.worldometers.info/coronavirus/](https://www.worldometers.info/coronavirus/) table 2020-04-05 Daily 2020-04-06 2020-04-05 Yes

Source code available at [https://github.com/afo/covid19](https://github.com/afo/covid19) (feel free to contribute 😊)

This project was built for [https://www.hackthecrisis.se/](https://www.hackthecrisis.se/) by:
* Alexander Fred-Ojala
* Andreas Fred-Ojala
* Annika Rydgård
* Joakim Bülow
* Johan Sleman
* Kent Ngo
* Marcus Zethraeus
* Martin Ascard
* Martin Edung
