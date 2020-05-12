import os
import matplotlib
import matplotlib.pyplot as plt
import datetime

def read_data2():
    base=os.getcwd()
    os.chdir("../COVID-19/csse_covid_19_data/csse_covid_19_time_series/")
    with open("time_series_covid19_confirmed_global.csv","r") as f:
        t=f.read()
    t=t.split("\n")
    columns=t.pop(0)
    
    columns=columns.split(",")
    dates=columns[4:]
    
    new_dates=[]
    for x in dates:
        xi=x.split("/")
        date=datetime.date(day=int(xi[1]),month=int(xi[0]),year=2020)
        new_dates.append(date)
    data_d={}
    data_d["dates"]=new_dates
    for x in t:
        
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
    os.chdir(base)
    return data_d

def averages(diffs,last_x_days,days=14):
    averages=[]
    c=1
    while c < last_x_days+1:
        sub_sum=sum(diffs[-c-days:-c])
        avg=sub_sum/days
        averages.append(avg)
        c+=1
    #going backwards, so we need to reverse for plot
    averages.reverse()
    return averages

def plot21(new_dates,yn,diffs,my_country,save):
    
    fig, ax = plt.subplots()
    plt.plot(new_dates,yn,label="total")
    plt.plot(new_dates,diffs,label="diffs")
    plt.legend()
    
    extraticks=[matplotlib.dates.date2num(new_dates[-1])]
    plt.xticks(list(plt.xticks()[0]) + extraticks)
    
    fig.autofmt_xdate()
    plt.title("Cases in "+my_country)
    fig.tight_layout()
    plt.grid()
    
    if save:
        plt.savefig(my_country+"plot.svg")
    else:
        plt.show()

def calculate_averages(diffs,last_x_days):
    one_week_averages=averages(diffs,last_x_days,7)
    two_week_averages=averages(diffs,last_x_days,14)
    three_week_averages=averages(diffs,last_x_days,21)
    
    one_week_averages=one_week_averages[-last_x_days:]
    two_week_averages=two_week_averages[-last_x_days:]
    three_week_averages=three_week_averages[-last_x_days:]
    
    return one_week_averages,two_week_averages,three_week_averages

def plot22(new_dates,all_averages,diffs,my_country,last_x_days,save):
    
    [one_week_averages,two_week_averages,three_week_averages]=all_averages
        
    fig, ax = plt.subplots()
    #plt.plot(new_dates,yn,label="total")
    main_dates=new_dates[-last_x_days:]
    plt.plot(main_dates,diffs,label="diffs")
    #plt.plot([new_dates[0],new_dates[-1]],[three_week_avg,three_week_avg],label="three week avg diffs")
    
    #modify the dates a bit so they're more accurately displayed
    new_d_w1=new_dates[-last_x_days-3:-3]
    new_d_w2=new_dates[-last_x_days-7:-7]
    new_d_w3=new_dates[-last_x_days-10:-10]
    plt.plot(new_d_w1,one_week_averages,label="one week avg diffs")
    plt.plot(new_d_w2,two_week_averages,label="two week avg diffs")
    plt.plot(new_d_w3,three_week_averages,label="three week avg diffs")
    plt.legend()
    
    my_ticks=plt.xticks()
    my_ticks=list(my_ticks[0])
    
    interesting_ts=[]
    c=21
    while c < last_x_days:
        interesting_ts.append(-c)
        c+=7
    real_interesting_ts=[]
    labels=[]
    for x in interesting_ts:
        real_interesting_ts.append(matplotlib.dates.date2num(new_dates[x]))
        labels.append(str(new_dates[x]))
    
    #t_b=matplotlib.dates.date2num(datetime.date(day=23,month=3,year=2020))
    #real_interesting_ts.append(t_b)
    #labels.append("start of measures")
    
    t1=matplotlib.dates.date2num(new_dates[-14])
    real_interesting_ts.append(t1)
    labels.append("max inc 14d")
    
    t2=matplotlib.dates.date2num(new_dates[-6])
    real_interesting_ts.append(t2)
    labels.append("avg inc 6d")
    
    t3=matplotlib.dates.date2num(new_dates[-1])
    real_interesting_ts.append(t3)
    labels.append("today, "+str(new_dates[-1]))
    
    a=real_interesting_ts
    b=labels
        
    plt.xticks(a,b)
    
    fig.autofmt_xdate()
    plt.title(my_country+" diffs")
    fig.tight_layout()
    plt.grid()
    
    if save:
        plt.savefig(my_country+"plot_diffs.svg")
    else:
        plt.show()

def calculate_diffs(values):
    diffs=[]
    last=0
    for x in values:
        diffs.append(x-last)
        last=x
    return diffs
    
def plot2(data_d,my_country,last_x_days=40,save=True):
    
    dates=data_d["dates"]
    values=data_d[my_country]["values"]
    diffs=calculate_diffs(values)
    
    #a bit ugly, side effect wise
    data_d[my_country]["diffs"]=diffs
    
    trimmed_dates1=dates[-last_x_days:]
    trimmed_dates2=dates#[-last_x_days:]
    trimmed_values=values[-last_x_days:]
    
    all_averages=calculate_averages(diffs,last_x_days)
    diffs=diffs[-last_x_days:]
    
    #also writing averages to data_d
    data_d[my_country]["all_averages"]=all_averages
    
    plot21(trimmed_dates1,trimmed_values,diffs,my_country,save)
    plot22(trimmed_dates2,all_averages,diffs,my_country,last_x_days,save)
    

def plot3(data_d,country_list,last_x_days,save=True):
    
    dates=data_d["dates"]
    trimmed_dates=dates[-last_x_days:]
    
    c=0
    while c < 3:
        fig, ax = plt.subplots()
        for my_country in country_list:
            diffs=data_d[my_country]["diffs"]
            trimmed_diffs=diffs[-last_x_days:]
            all_averages=data_d[my_country]["all_averages"]
            #plt.plot(trimmed_dates,trimmed_diffs,label=my_country+" diffs")
            
            avgs=all_averages[c]
            trimmed_avgs=avgs[-last_x_days:]
            plt.plot(trimmed_dates,avgs,label=my_country)
        
        plt.xticks(list(plt.xticks()[0])+[matplotlib.dates.date2num(dates[-1])])
        plt.legend()
        plt.grid()
        plt.title("country diffs compared"+" "+str((c+1)*7)+"d avg")
        fig.autofmt_xdate()
        
        if save:
            plt.savefig("countries_compared"+str((c+1)*7)+"d_avg.svg")
        else:
            plt.show()
        c+=1

def main2(last_x_days=80):
    data_d=read_data2()
    
    country_list=["Germany","Italy","India","Iran","Sweden","United Kingdom"]
    #side effect, plot writes diffs to data_d
    for x in country_list:
        plot2(data_d,x,last_x_days=last_x_days)
   
    #which is why they're available here
    plot3(data_d,country_list,last_x_days=last_x_days)
    
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
