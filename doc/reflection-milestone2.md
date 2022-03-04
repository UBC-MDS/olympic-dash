## Reflection

As of the current milestone, our dashboard has incorporated all of the graphs in our proposal with a high degree of functionality. The four graphs implemented underwent slight changes in display and functionality compared to the proposed graphs. The first graph consists of a bubble chart displaying medals earned by country. As there are a significant number of countries, the color scheme in the proposal was not implemented for now. 

The second graph situated below is a histogram showing the distribution of athlete heights. This graph is accompanied by a dropdown list allowing the user to specify which event they want to see data displayed for. 

Both these graphs are affected by a year slider located in the bottom left. The slider currently iterates by 2 years to capture years where Olympics take place. Currently, due to irregularities in Olympic years, certain years on the slider will result in no data being displayed for the height histogram and the medals by country bubble plot. There's a plan to pythonically input the available Olympic years into the slider as a list to correct this.

The third graph located to the right of the bubble chart is a histogram showing the distribution of Olympic medals earned by athlete age. This graph is accompanied by an age slider which allows for the selection of age range to be displayed. We may look into implementing additional filters on this graph in the future to reduce the number of rows of data shown and thus lowering the loading time. This graph is also affected by the year slider previously mentioned. In the future, the arrangement of the graph may be altered to better reflect how this slider affects 3 of the 4 total graphs.

The last graph in the bottom right is a time series graph showing the number of Olympic medals earned by specific countries over time. This graph has a dropdown list which allows the user to select which country data is displayed for.

Finally on the left hand side of the dashboard we have included radio buttons to filter data for the season of Olympics (winter or summer) and the type of medal displayed. Note that the season filter interferes with the year slider so no data will be displayed if for example, the year is selected to be a summer olympics year while the winter radio button is selected. We hope to fix this interaction in the future. These filters apply to all graphs on the dashboard. 

In terms of implementation, we believe most of the functionality we intended to provide users has been incorporated into our initial dashboard. Future plans are to make the dashboard more aesthetically pleasing, which involves adding css themes and borders around graphs to clearly differentiate them. Additionally, we would like to rearrange the position of the year slider to better reflect its functionality as well as implement headers for sliders so that their functions are clear to the user.
