import streamlit as st
import pandas as pd
import emoji

st.set_page_config(
    page_title="Global CO₂ emissions",
    page_icon="💨",
    layout="wide",
    )

# scrape data from Wikipedia using pandas
df = pd.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions#Notes_and_references")[2]

# ===== CLEAN DATA
# reduce columns and rename headers 
df = df[df.columns[:7]]
df.columns = df.columns.droplevel()
df.columns = ["Country", "1990",  "2005", "2017", "2021", "2017 (% of world)", "2017 vs 1990 (% change)"]
df = df.loc[~df["Country"].isin(["European Union", "World", "World – International Aviation", "World – International Shipping"])].reset_index(drop=True)
df.loc[df["Country"]=="Germany", "1990"] = "1018.097"

# prepare columns for visualising data in table
df["Emissions 1990 to 2021"] = [list(df[["1990",  "2005", "2017", "2021"]].iloc[x]) for x in range(len(df))]
df["2017 (% of world)"] = df["2017 (% of world)"].str[:-1]  # remove % at the end
df["2017 vs 1990 (% change)"] = df["2017 vs 1990 (% change)"].str[:-1]  # remove % at the end

# get flag emojis
df["Country_helper"] = df["Country"].str.split("\xa0").str[0]
cleaned_names = {"Congo": "Congo_-_Brazzaville", "Czech Republic": "Czechia", 
         "East Timor": "Timor-Leste", "Hong Kong": "Hong_Kong_SAR_China", "Ivory Coast": "Côte_d’Ivoire", "Macau": "Macao_SAR_China",
         "Myanmar": "myanmar", "Saint Helena, Ascension and Tristan da Cunha": "St._Helena", "Saint Vincent and the Grenadines": "St._Vincent_&_Grenadines:", 
         "Serbia & Montenegro": "Serbia", "The Gambia": "gambia" }
# "Democratic Republic of the Congo": "Congo_-_Kinshasa", 
for key, value in cleaned_names.items():
    df["Country_helper"] = df["Country_helper"].str.replace(key, value)
df["Country_helper"] = df["Country_helper"].str.replace(" ", "_").str.replace("_and_", "_&_").str.replace("Saint", "St.").str.replace("Democratic_Republic_of_the_Congo_-_Brazzaville", "Congo_-_Kinshasa")
df["flag"] = [emoji.emojize(':%s:'  %(x), language="alias" ) for x in df["Country_helper"]]
df["Country"] = df["Country"].str.replace("\xa0", ", ")
df["Country_display"] = df["flag"] + "   " + df["Country"]

# ===== DISPLAY DATA
col_text, col_table = st.columns([1,2])

# display dataframe
with col_table:
    st.dataframe(
        df[["Country_display",  "Emissions 1990 to 2021", "2017 (% of world)", "2017 vs 1990 (% change)"]],
        column_config={
            "Country_display": st.column_config.TextColumn(
                "Country", width="Large"
            ),       
            "Emissions 1990 to 2021": st.column_config.LineChartColumn(
                "Fossil CO₂ 1990, 2005, 2017, 2021 (Mt CO₂)", 
                y_min=0, y_max=None, width="Large"
            ),
            "2017 (% of world)": st.column_config.ProgressColumn(
                "% of world (2017)",
                format="%.1f%%", 
                min_value=0, max_value=100, width="medium"
            ),
            "2017 vs 1990 (% change)": st.column_config.NumberColumn(
                "2017 vs 1990",
                format="%.1f%%", width="small"
            ),
        },
        hide_index=True,
        width = 950, 
        height = 550
    )
    
# Text
with col_text:
    st.title("Global CO₂ Emissions")
    st.subheader("Emissions by country")
    st.write("")
    st.markdown("The table shows Carbon dioxide (CO₂) emissions per country for 1990, 2005, 2017 and 2021 (in megatonnes). It only includes emissions from fossil fuels and industry not from land use.")
    st.write("")
    st.markdown("Data sourced from Wikipedia ([List of countries by carbon dioxide emissions](https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions)). For more detailed analysis of worldwide emissions, check out [Our World in Data](https://ourworldindata.org/co2-emissions).")

# Footer
st.divider()
st.markdown("Made by Lisa Hornung using 🎈Streamlit 1.23.1 - Full code available [here](https://github.com/liloho/interactive-tables). Follow me on [Github](https://github.com/Lisa-Ho), [Mastodon](https://fosstodon.org/@LisaHornung), [Linkedin](https://www.linkedin.com/in/lisa-maria-hornung/), and [Twitter](https://twitter.com/LisaHornung_)")