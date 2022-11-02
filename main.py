import os
import streamlit as st
import requests
import pandas as pd
import json
import streamlit.components.v1 as components
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static
import folium
import requests
from requests.exceptions import ConnectionError

st.set_page_config(page_title = "Weather App", page_icon = "⛅") # Configures the default settings of the page.

st.header("Weather App")
st.subheader("Exploring Realtime Weather API")

url = "https://weatherapi-com.p.rapidapi.com/current.json"

headers = {
	"X-RapidAPI-Key": "54bcf1846fmsh1b05a5481dce663p109f16jsn4614e548a17d",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

location = st.text_input("Enter the location", "Chennai")

querystring = {"q":{location}}

response = requests.request("GET", url, headers=headers, params=querystring) ## Output: <Response [200]>
result = response.text # Returns the content of the response

if(response.status_code == 400):
    st.error("No location found matching parameter 'q', try searching for a different location.")

else:
    data = json.loads(result)
    col1, col2 = st.columns(2)

    with col1:

        st.write(f'Name: {data["location"]["name"]}')
        st.write(f'Region: {data["location"]["region"]}')
        st.write(f'Country: {data["location"]["country"]}')
        st.write(f'Local Time: {data["location"]["localtime"]}')
        st.metric(label="wind_kph", value= f'{data["current"]["wind_kph"]}')
        st.write(f'Feels like: {data["current"]["feelslike_c"]} ℃')

    with col2:

        st.write(f'Temp in Celcius: {data["current"]["temp_c"]}')
        st.write(f'Temp in Farenheit: {data["current"]["temp_f"]}')
        st.write(f'Condition: {data["current"]["condition"]["text"]}')
        st.image(f'http:{data["current"]["condition"]["icon"]}')
        st.metric(label = "Humidity", value = f'{data["current"]["humidity"]}')

    st.info('⛅ Current weather or realtime weather API method allows a user to get up to date current weather information in json and xml. The data is returned as a Current Object.')

    components.html(
        """
        <a href="https://www.weatherapi.com/" title="Free Weather API"><img src='//cdn.weatherapi.com/v4/images/weatherapi_logo.png' alt="Weather data by WeatherAPI.com" border="0" target="_blank"></a>
        """
    )




    def config():

        # code to check turn of setting and footer
        st.markdown(""" <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

        # encoding format
        encoding = "utf-8"

        st.markdown(
            """
            <style>
                .stProgress > div > div > div > div {
                    background-color: #1c4b27;
                }
            </style>""",
            unsafe_allow_html=True,
        )

        st.balloons()
        # I want it to show balloon when it finished loading all the configs


    def get_geolocation():
        key = "d574922aa0844f5e8f2b371edd4958b1"
        response = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=" + key)
        return response.json()


    def other_tab():
        st.header("Other TAB")


    def home():
        try:
            with st.spinner("Please wait your request is being processed ......"):
                response = get_geolocation()
                st.header("IP Geolocation App 🕵️‍♂️")
                col1, col2 = st.columns([8, 4])

                with col1:
                    m = folium.Map(location=[response["latitude"], response["longitude"]], zoom_start=16)
                    tooltip = "The Approx Location"
                    folium.Marker(
                        [response["latitude"], response["longitude"]],
                        popup="The Approx Location", tooltip=tooltip
                    ).add_to(m)
                    folium_static(m, width=500, height=400)

                with col2:
                    st.markdown(f"""
                    <table>
                    <thead>
                       <th>Data</th>
                       <th>Value</td>
                    </thead>

                    <tr>
                       <td>Ip Address</td>
                       <td>{response["ip"]}</td>
                    </tr>

                    <tr>
                       <td>City</td>
                       <td>{response["city"]}</td>
                    </tr>

                    <tr>
                       <td>District</td>
                       <td>{response["district"]}</td>
                    </tr>

                    <tr>
                       <td>Province</td>
                       <td>{response["state_prov"]}</td>
                    </tr>

                    <tr>
                       <td>Calling Code</td>
                       <td>{response["calling_code"]}</td>
                    </tr>
                    <tr>
                       <td>Latitude</td>
                       <td>{response["latitude"]}</td>
                    </tr>

                    <tr>
                       <td>Longitude</td>
                       <td>{response["longitude"]}</td>
                    </tr>

                    <tr>
                       <td>Country</td>
                       <td><img src="{response['country_flag']}" style="width:30%;max-width:40%"> {response["country_name"]}</td>
                    </tr>


                    </table>
    """, unsafe_allow_html=True)

                with st.expander("More Information regarding this IP"):
                    st.subheader("Currency")
                    df = pd.DataFrame.from_dict(response["currency"], orient="index", dtype=str, columns=['Value'])
                    st.write(df)
                    st.subheader("ISP")
                    st.write("isp", {response["isp"]})
                    st.write("connection_type", {response["connection_type"]})
                    st.write("organization", {response["organization"]})

                    st.subheader("TimeZone")
                    df_1 = pd.DataFrame.from_dict(response["time_zone"], orient="index", dtype=str, columns=['Value'])
                    st.write(df_1)








        except ConnectionError as e:
            st.error("The APP has failed to connect please check your connection 😥")


    def main():
        config()

        home()


    if __name__ == '__main__':
        main()


num1 = st.number_input('Insert the first number for sum:')
st.write('The current first number is: ', num1)

num2 = st.number_input('Insert the second number for sum:')
st.write('The current second number is: ', num2)

url1='https://oe6pwzxigcj7wygntothidvy4e0kscwh.lambda-url.us-east-1.on.aws/?num1=%f&num2=%f' %(num1,num2)
response1 = requests.get(url1)

st.write(response1.text)

num3 = st.number_input('Insert the first number for multiplication:')
st.write('The current first number is: ', num3)

num4 = st.number_input('Insert the second number for multiplication:')
st.write('The current second number is: ', num4)

url2='https://ewpqdd22cbf7qynynquei6kn6i0whfay.lambda-url.us-east-1.on.aws/ ?num3=%f&num4=%f' %(num3,num4)
response2 = requests.get(url2)

st.write(response2.text)

num5 = st.number_input('Insert the first number for the division:')
st.write('The current number is: ', num5)

num6 = st.number_input('Insert the second number for the division:')
st.write('The current number is: ', num6)

url3='https://axdqsg57axbtspvilmf5saj6w40bcjtb.lambda-url.us-east-1.on.aws/ ?num5=%f&num6=%f' %(num5,num6)
response3 = requests.get(url3)

st.write(response3.text)


