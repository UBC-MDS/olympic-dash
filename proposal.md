## Motivation and Purpose

Our role: Data scientist consultancy firm  

Target audience: International Olympic Committee members (and the curious public)  

“The goal of the Olympic Movement is to contribute to building a peaceful and better world by educating youth through sport practiced without discrimination of any kind and in the Olympic spirit, which requires mutual understanding with a spirit of friendship, solidarity and fair play.”[^1]

We propose building a visualization app to allow IOC members (and members of the general public) to explore historical Olympic results to review the success trends of various countries to determine abnormal performance trends and which countries could be future high medal achievers. All in the interest of making the olympic games more competitive and reward the countries that are developing their athletes and improving their performance in the games.

## Description of the Data

We will be visualizing a historical dataset on the modern Olympic Games, including the Game from Athens 1896 to Rio 2016. The dataset is from [tidytuesday](https://github.com/rfordatascience/tidytuesday). There are 271116 observations(rows) in the dataset, which shows the data for 135571 athletes. Each row corresponds to an individual athlete competing in an individual Olympic event (athlete-events). There are 15 associated variables(columns). The key columns that we use for visualization are name, age, height(in cm), team(Country/Team competing for), games(Olympic games name), year(Year of Olympics), season(either Winter or Summer), city(City of Olympic host), sport, event, and medal(Gold, Silver, Bronze or NA).

Note that the Winter and Summer Games were held in the same year up until 1992. After that, they staggered them such that Winter Games occur on a four-year cycle starting with 1994, then Summer in 1996, then Winter in 1998, and so on. A common mistake people make when analyzing this data is to assume that the Summer and Winter Games have always been staggered.
## Reseach Question and Usage Scenario

Some of the research questions that our app will answer are the following:

- Which countries have been improving their performance in the olympics historically?
- Have countries performed better in the summer or winter olympics?
- What are some common characteristics among the athletes that compete in the same event?
- Which athletes have won the most medals across the years?

Here's also a description of the user persona:

Harry is a member of the IOC (International Olympic Committee). He and his team have been working recently on investigating if there are any abnormal performance trends for certain countries. They want to know if there is something that they can do to help countries that have been perfoming worse every olympic cycle with the techniques that high performing countries are using to generate more competitive events in the olympics. They also want to know which are countries are on the rise, to become future contenders in most events, so that they can reward them by hosting the olympics on their countries if feasible and encourage athlete development around the world in this way.

[^1]: [International Olympic Committee: Beyond the Games](https://olympics.com/ioc/beyond-the-games)