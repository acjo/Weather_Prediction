# particle_filter.py
from pfilter import ParticleFilter, gaussian_noise, squared_error, independent_sample
from scipy.stats import norm, gamma, uniform
import pandas as pd
january = pd.read_csv("data/dataByMonth/jan_co2_weather.csv")
february = pd.read_csv("data/dataByMonth/feb_co2_weather.csv")

prior_fn = independent_sample([uniform(loc=0, scale=32).rvs, 
                    uniform(loc=0, scale=32).rvs, 
                    gamma(a=2,loc=0,scale=10).rvs,
                    norm(loc=0, scale=0.5).rvs,
                    norm(loc=0, scale=0.5).rvs])
obs = january.loc()[:,["Dew Point (F)","Humidity (%)","Wind Speed (mph)","Wind Gust (mph)","Pressure (in)","Precip (in)"]].values
state = january.loc()[:,"Temp (F)"].values


pf = ParticleFilter(prior_fn = prior_fn, observe_fn=obs, dynamics_fn = state)
pf.update()