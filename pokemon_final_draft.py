"""
Adrian Gonzales
ISTA 350 Final Project
Summary: This project web scrapes data from a pokemon data page and creates
a pokemon dataframe. From this dataframe, we create 3 images looking at 
different comparisons such as attack + speed and their correlation with 
defense capabilties, the strongest primary type of pokemon, and the top 10 
strongest pokemon
"""

import requests, pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

#Proper format for names
def clean_names(name):
    """
    Cleans the names of every pokemon. This is so they are
    properly formatted. For example: Mega Mewtwo Y would appear
    as Mewtwo Mega Mewtwo Y, so this function corrects it to be 
    Mega Mewtwo Y.

    PARAMETER:
        name: name column from dataframe

    RETURN:
        new_name: properly formatted name
    """
    parts = name.split()
    check = ["Mega", "Ultra", "Primal"]
    for i in range(len(parts)):
        if parts[i] in check:
            new_name = parts[i]
            for j in range(i + 1, len(parts)):
                new_name = new_name + " " + parts[j]
            return new_name
    if len(parts) > 1 and parts[0] == parts[1]:
        new_name = parts[1]
        for i in range(2, len(parts)):
            new_name = new_name + " " + parts[i]
        return new_name
    
    new_name = parts[0]
    for i in range(1, len(parts)):
        new_name = new_name + " " + parts[i]
    return new_name

#Glass cannon
def glass_cannon(df):
    """
    Creates a scatter plot w linear regression showing 
    correlation between attack + speed on HP + defense + 
    sp. defense

    PARAMETER: 
        df: pokemon dataframe
    """
    #Calculates pokemon power
    x = df["Attack"] + df["Speed"]
    #Calculates pokemon durability
    y = df["HP"] + df["Defense"] + df["Sp. Def"]

    #Used to find linear regression line
    x_const = sm.add_constant(x)
    model = sm.OLS(y, x_const)
    results = model.fit()
    slope = results.params.iloc[1]
    intercept = results.params.iloc[0]
    predicted = slope * x + intercept

    plt.figure()
    plt.scatter(x, y, alpha = 0.5)
    plt.plot(x, predicted, color = "red")
    plt.title("How High Attack + High Speed Impacts Durability", fontsize = 20)
    plt.xlabel("Attack + Speed Value", fontsize = 14)
    plt.ylabel("Durability Value (HP + Defense + Sp. Defense)", fontsize = 14)

    plt.show()

#Best primary type
def primary_stats(df):
    """
    Creates a bar chart showing the average total stats
    for each Pokémon primary type.

    PARAMETER:
        df: pokemon dataframe
    """
    df["Primary Type"] = df["Type"].str.split().str[0]
    mean_stat = df.groupby("Primary Type")["Total"].mean()
    mean_stat = mean_stat.sort_values(ascending = False)
    mean_stat = mean_stat.round(2)

    plt.figure()
    bars = plt.bar(mean_stat.index, mean_stat.values, edgecolor = "black")
    plt.bar_label(bars)
    plt.title("Average Total Stats by Primary Type", fontsize = 20)
    plt.xlabel("Primary Type", fontsize = 14)
    plt.ylabel("Average Total Stats", fontsize = 14)
    plt.xticks(rotation = 90)
        
    plt.show()


def main():
    url = "https://pokemondb.net/pokedex/all"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    r = requests.get(url, headers = headers)
    table = pd.read_html(r.text)

    pokemon_df = table[0]
    pokemon_df["Name"] = pokemon_df["Name"].apply(clean_names)
    
    glass_cannon(pokemon_df)
    primary_stats(pokemon_df)
    

main()
