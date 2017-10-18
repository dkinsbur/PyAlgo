def FreestockTimeToMyCsvTime(fs_time):
    fs_time = fs_time.strip()
    date, time, am_pm = fs_time.split()
    h, m, s = time.split(':')
    mn, dt, yr = date.split('/')

    if am_pm == 'PM' and h.strip() != '12':
        h = str(int(h) + 12)

    return '{year}-{month}-{day}-{hour}-{min}'.format(year=yr, month=mn, day=dt, hour=h, min=m)

def ConvertFreestockCsvToMyCsv(fs_path, out_path):
    with open(out_path, 'w') as out_fl:
        out_fl.write('date,high,low,open,close,volume\n')
        with open(fs_path) as in_fl:
            assert in_fl.readline().strip() == 'Date,Open,High,Low,Close,Volume'
            for line in in_fl:
                Date, Open, High, Low, Close, Volume = line.strip().split(',')
                Date = FreestockTimeToMyCsvTime(Date)
                out_fl.write('{},{},{},{},{},{}\n'.format(Date, High, Low, Open, Close, Volume))
