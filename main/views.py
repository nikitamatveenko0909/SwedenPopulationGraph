from django.shortcuts import render
from pyscbwrapper import SCB
import re


scb = SCB("sv", "BE", "BE0101", "BE0101A", "BefolkningNy")
regioner = scb.get_variables()["region"]
r = re.compile(r".* län")
lan = list(filter(r.match, regioner))
scb.set_query(år=["2017", "2018", "2019"], region=lan)
koder = scb.get_query()["query"][1]["selection"]["values"]
scb_uttag = scb.get_data()["data"]
landic = {}
for i in range(len(koder)):
    landic[koder[i]] = lan[i]


landata = {}

for kod in landic:
    landata[landic[kod]] = {}
    for i in range(len(scb_uttag)):
        if scb_uttag[i]["key"][0] == kod:
            landata[landic[kod]][scb_uttag[i]["key"][1]] = float(
                scb_uttag[i]["values"][0]
            )

# Create your views here.
def index(request):
    scb.set_query(år=["2017", "2018", "2019"])
    data = scb.get_data()["data"]
    scb.set_query(år=["2017", "2018", "2019"], region=lan)
    region_data = scb.get_data()["data"]
    years = []
    population = []
    population_increase = []
    region_population = []
    regions = {}

    for i in data:
        years.append(i["key"][0])
        population.append(i["values"][0])
        population_increase.append(i["values"][1])

    for i in region_data:
        key = i["key"][0]
        if regions.get(landic[key], None):
            regions[landic[key]].append(i["values"][0])
        else:
            regions[landic[key]] = [i["values"][0]]

    for key, value in regions.items():
        region_population.append({"name": key, "values": value})

    population_increase_percent = [
        f"{(int(population_increase[i])/int(population[i])) * 100}"
        for i in range(len(population))
    ]

    return render(
        request,
        "main/index.html",
        context={
            "population": population,
            "population_increase": population_increase_percent,
            "region_population": region_population,
        },
    )
