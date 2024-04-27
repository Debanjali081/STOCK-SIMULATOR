from taipy import Gui
import pandas as pd 

data={
    "Date":pd.date_range("2023-01-01",periods=4,freq="D"),
    
    "Min":[222,419.7,662.7,323.5],
    "Max":[28.6,68.2,666.5,173.5]
}
title="Stock Simulator By Debu"
company_name="Google"
path="logo.png"
company_minp=340
company_maxp=400
def deb(state):
    print("Hey Debu How Are You !!")
    print(state.path)
    print(state.company_minp)
    print(state.company_maxp)

    with open("data.txt","w") as f:
        f.write(f"{state.company_name},{state.company_minp},{state.company_maxp}")

page="""
<|text-center|
<|{title}|hover_text=Welcome To Stock Screener|>
<|{path}|image|>

Nmae Of Stock :<|{company_name}|input|>

Min Price :<|{company_minp}|input|>

Max Price :<|{company_maxp}|input|>

<|Run Simulation|button|on_action=deb|>

<|{title}|hover_text=Your Simulation>

<|{data}|chart|mode=lines|x=Date|y[1]=Min|y[2]=Max|line[2]=dash|color[2]=blue|>


>
"""

if __name__=="__main__":
    app=Gui(page)
    app.run(use_reloader=True)
