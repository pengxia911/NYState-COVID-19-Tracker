import csv
from matplotlib import pyplot as plt
import arrow

plt.figure()

with open("data/positive_cases.csv") as fp:
    reader = csv.DictReader(fp)
    for area_data in reader:
        if area_data["Location"] not in {
            "New York City",
            "Total Positive Cases (Statewide)"
        }: continue
        location = area_data["Location"]
        area_data = dict(
            (arrow.get(time), int(count))
            for time, count in list(area_data.items())[1:]
            if count != ""
        )
        time_array = list(area_data.keys())
        count_array = list(area_data.values())
        line, = plt.plot_date(
            time_array, count_array,
            ls="-", marker="o", lw=1.5,
            label=location
        )

        for x, y in zip(time_array, count_array):
            if y < 10: continue
            plt.text(x, y*1.1, str(y), va="bottom", ha="center", size=6, c=line.get_color())


plt.semilogy()

plt.xlabel("Time")
plt.ylabel("Positive case")

from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import LogLocator, NullLocator, LogFormatter
from util import LogFormatterSI
import numpy

plt.gca().xaxis.set_major_locator(AutoDateLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter("%m/%d"))
#plt.gca().xaxis.set_minor_locator(AutoDateLocator())
plt.gca().yaxis.set_major_locator(LogLocator(subs=(1, 2, 5)))
plt.gca().yaxis.set_major_formatter(LogFormatterSI(labelOnlyBase=False, minor_thresholds=(numpy.inf, numpy.inf)))
plt.gca().yaxis.set_minor_locator(NullLocator())

plt.title("New York State COVID-19 positive case count")

plt.xlim(left=arrow.get("2020-03-01"))
plt.ylim(bottom=10)

plt.legend()
plt.savefig("plots/NYState3.png", dpi=300)

