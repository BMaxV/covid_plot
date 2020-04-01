import os
import matplotlib.pyplot as plt
import datetime

def read_data2():
    os.chdir("../COVID-19/csse_covid_19_data/csse_covid_19_time_series/")
    with open("time_series_covid19_confirmed_global.csv","r") as f:
        t=f.read()
    t=t.split("\n")
    columns=t.pop(0)
    #print(columns)
    columns=columns.split(",")
    dates=columns[4:]
    #print(dates)
    new_dates=[]
    for x in dates:
        xi=x.split("/")
        date=datetime.date(day=int(xi[1]),month=int(xi[0]),year=2020)
        new_dates.append(date)
    data_d={}
    data_d["dates"]=new_dates
    for x in t:
        #print(x)
        x=x.split(",")
        if len(x)<3:
            break
        province=x[0]
        country=x[1]
        if country not in data_d:
            data_d[country]={}
        if province!='':
            data_d[country][province]={}
            local_d=data_d[country][province]
        else:
            local_d=data_d[country]
        y=x[4:]
        yn=[]
        for yi in y:
            yn.append(float(yi))
        local_d["values"]=yn
        
    return data_d


    
def plot2(data_d,my_country,last_x_days=40):
    
    dates=data_d["dates"]
    values=data_d[my_country]["values"]
    new_dates=dates[-last_x_days:]
    yn=values[-last_x_days:]
    diffs=[]
    last=0
    for x in yn:
        diffs.append(x-last)
        last=x
        
    fig, ax = plt.subplots()
    plt.plot(new_dates,yn,label="total")
    plt.plot(new_dates,diffs,label="diffs")
    plt.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.grid()
    plt.show()
        
def main2():
    data_d=read_data2()
    plot2(data_d,"Germany")

def read_data():

    os.chdir("../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports")
    ls = os.scandir()
    all_data = {}
    for x in ls:
        if ".csv" in x.name:
            with open(x.name) as f:
                text_lines = f.readlines()

            date = str(x.name)
            date = date.split(".")[0]

            columns = text_lines.pop(0)
            columns = columns.strip("\n")
            columns = columns.split(",")

            all_data[date] = {}
            m = len(columns)

            for line in text_lines:
                line = line.replace("\"", "")
                line = line.strip("\n")
                line = line.split(",")
                country = line[1]
                province = line[0]
                if country not in all_data[date]:
                    all_data[date][country] = {}
                if province not in all_data[date][country]:
                    all_data[date][country][province] = {}

                # ok, this is stupid. probably because I should have
                # used a package, but here we are.

                col_c = 3
                c = 0

                found = False
                found_c = 0
                while c < len(line) and found_c < 3:
                    if found == False:
                        try:
                            mydatetime = datetime.datetime.fromisoformat(
                                line[c])
                            # if it works, I found my c
                            c += 1
                            found = True
                        except:
                            c += 1
                            continue
                    line_c = line[c]
                    if line_c == "":
                        line_c = 0

                    all_data[date][country][province][columns[col_c]
                                                      ] = float(line_c)
                    col_c += 1
                    found_c += 1
                    c += 1
    return all_data


def date_cleanup(all_data):
    new_dict = {}
    keys = list(all_data.keys())
    keys.sort()
    # thanks for imperial dates you... ;)
    for date in keys:
        plot_date = date.split("-")
        plot_date = [int(v) for v in plot_date]
        plot_date = datetime.date(
            month=plot_date[0], day=plot_date[1], year=plot_date[2])
        new_dict[plot_date] = all_data[date]

    all_data = new_dict
    return all_data


def plot(all_data, my_country="Germany", my_keys=["Confirmed","Deahts"],last_x_days=None):
    dates = []
    values = []

    keys = list(all_data.keys())
    keys.sort()

    fig, ax = plt.subplots()

    for my_stat in my_keys:
        values = []
        dates = []
        diff_values=[]
        last_value=0
        for date in keys:
            if date not in dates:
                dates.append(date)
            data_on_date = all_data[date]
            val = 0
            for country in data_on_date:
                if country == my_country:
                    for province in data_on_date[country]:
                        if my_stat in data_on_date[country][province]:
                            val += data_on_date[country][province][my_stat]
                        else:
                            val += 0
            diff_values.append(val-last_value)
            values.append(val)
            last_value=val
        if last_x_days!=None:
            dates=dates[-last_x_days:]
            values=values[-last_x_days:]
            diff_values=diff_values[-last_x_days:]
        plt.plot(dates, values, label=my_stat)
        plt.plot(dates,diff_values, label="diff "+my_stat)
    plt.legend()
    plt.title(my_country)

    fig.autofmt_xdate()
    fig.tight_layout()
    plt.grid()

    if True:
        plt.savefig("plot.svg")
    else:
        plt.show()


def main():
    old_dir = os.getcwd()
    all_data = read_data()
    os.chdir(old_dir)

    all_data = date_cleanup(all_data)
    plot(all_data,
        my_country="Italy",
        my_keys=["Confirmed","Deaths"],last_x_days=40)


if __name__ == "__main__":
    #main()
    main2()#read_data2()
