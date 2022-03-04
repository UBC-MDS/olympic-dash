# olympic-dash

An interactive dashboard illustrating historic olympic data and trends

## Description

This app contains a dashboard which visualizes Olympic data from 1896 up until 2016. 
Key metrics of interest will be displayed including: 
- Medals earned per country
- Medals earned depending on athlete age
- Athlete height based on Olympic events 
- Medals per country will be displayed 

Medals earned per country will be displayed via a bubble chart accompanied by a 
slider, allowing users to control the year of the Olympics displayed by the graph. 

A bar chart will show the medals earned for each athlete age bracket, while a histogram 
will show the distribution of athlete heights based on the event selected. These figures 
will contain a slider allowing users to adjust athlete age ranges and a dropdown list, 
allowing users to select the event visualized respectively. 

Lastly, a line graph will display the number of medals earned by countries over time. This 
figure will be accompanied by a dropdown list allowing users to select a subset of countries 
to display on the graph. 

Radio buttons on the side of the dashboard will allow for filtering of 
summer/winter Olympics data, in addition to allowing for users to filter data 
by the type of medals. Using these filters, users will be able to investigate trends 
in Olympic success between countries, medal types, athlete demographics, and more.

## Proposed Sketch

![Alt text](img/olympic-dash-proposal.png?raw=true "Dashboard Proposal")

## Usage and Installation
TODO

## Contributing to The Dashboard

You are welcome to contribute to olympic-dash if you have any idea regarding to this dashboard. Please go through the [contributing guidelines](CONTRIBUTING.md) for the recommended ways if you want to contribute or report/fix any existing bugs.

### How to install and run locally

To run the dashboard locally, we recommend to use a virtual environment like [venv](https://docs.python.org/3/library/venv.html) or [Anaconda](https://www.anaconda.com/). For simplicity, we could demonstrate the installiation process with venv.

#### Setup

Run the following command at the root directory of the project:

```
# Create a virtual environment
python -m venv olympicdash
```

```
# Activate the environment
source olympicdash/bin/activate
```

```
# Install the requirements
pip install -r requirements.txt
```

#### Run the dashboard

```
python src/app.py
```

The dashboard could then be accessed locally in <localhost:8050>. Now, you are good to go!

## Contributions

This app was developed by the following contributors:

|  Contributor  |  Github Username |
|--------------|------------------|
|  Allyson Stoll |  @datallurgy |
|  Helin Wang |  @helingogo  |
|  Rubén De la Garza Macías  |  @ruben1dlg |
|  Andy Yang  |  @AndyYang80  |

## Code of Conduct

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.
For more details, see our [code of conduct.](CONDUCT.md)

## License

`olympic-dash` was created by Allyson Stoll, Helin Wang, Rubén De la Garza Macías and Song Bo Andy Yang . It is licensed under the terms of the MIT license.