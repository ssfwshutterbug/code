# encoding: utf-8

import sys
import getopt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime



pd.set_option('max_colwidth', 40)
pd.set_option('max_rows', None)  
high_risk_port = ['21', '22', '23', '137', '139', '445', '3306', '3389']

# help message
help_msg = "simple usage: python analysis.py -f file-name \n\t\
default will analyse outside access, top visit shows 30 lines with more than 100 times block. host scan shows more than 20 times block. port scan shows more than 10 times block. \n\t\
python analysis.py -f file-name\t\t--file=file-name\texcel file or csv file \n\t\
python analysis.py -m tcp/udp/all\t--protocol=tcp/udp/all\tcheck tcp/udp/all protocol, default tcp \n\t\
python analysis.py --higher-port\t\t\t\tshow all ports include 10000-65535, default 1-10000 \n\t\
python analysis.py --inner\t\t\t\t\tshow  inside network access \n\t\
python analysis.py --outer\t\t\t\t\tshow  outside network access,default \n\t\
python analysis.py --port-check=n\t\t\t\tchange port check point,default 20\n\t\
python analysis.py --host-check=n\t\t\t\tchange host check point,default 10\n\t\
python analysis.py --head=n/all\t\t\t\t\tchange top scan line shows,default 30, any means print all\n\t\
python analysis.py --top-check=n\t\t\t\tchange top check point,default 100\n\t\
python analysis.py -h\t\t\t --help\t\t\tshow help info \n\t\
"

# header
header = ['statue', 'local_ip', 'service', 'remote_ip', 'remote_host_ip', 'remote_host_uuid', \
            'remote_hostname', 'block_times', 'block_first_time', 'block_last_time']

# remove default index showing
def remove_index_show(df):
    blankIndex=[''] * len(df)
    df.index=blankIndex

# terminal top line
def dis_line(info):
    print("==========================================\t{}\t============================================= ".format(info))

# get parameter from commandline or use default
def set_parameter(argv):
    global protocol, port, file, render, visitor, host_check_points, port_check_points, head, top_check_points
    protocol = 'tcp'
    port = 'lower'
    render = 'No'
    visitor = 'outer'
    host_check_points = 10
    port_check_points = 10
    head = 30
    top_check_points = 100
    try:
        opts, args = getopt.getopt(argv, 'f:hm:prio', ['file=', 'help', 'protocol=',  'higher-port',  'render', \
            'inner', 'outer', 'host-check=', 'port-check=', 'head=', 'top-check='])
    except getopt.GetoptError:
        print("run 'python analysis.py -h' to see help message")
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-m', '--protocol'):
            protocol = arg
        elif opt in ('-p', '--higher-port'):
            port = 'higher'
        elif opt in ('-f', '--file'):
            file = arg
        elif opt in ('-r', '--render'):
            render = 'Yes'
        elif opt in ('-i', '--inner'):
            visitor = 'inner'
        elif opt in ('-o', '--outer'):
            visitor = 'outer'
        elif opt == '--host-check':
            try:
                host_check_points = int(arg)
            except:
                print("wrong parameters! run 'python analysis.py -h' to see help message")
                sys.exit(1)
        elif opt == '--port-check':
            try:
                port_check_points = int(arg)
            except:
                print("wrong parameters! run 'python analysis.py -h' to see help message")
                sys.exit(1)
        elif opt == '--head':
            try:
                if arg == 'all':
                    head = 1048576
                else:
                    head = int(arg)
            except:
                print("wrong parameters! run 'python analysis.py -h' to see help message")
                sys.exit(1)
        elif opt == '--top-check':
            try:
                top_check_points = int(arg)
            except:
                print("wrong parameters! run 'python analysis.py -h' to see help message")
                sys.exit(1)
        elif opt in ('-h', '--help'):
            print(help_msg)
            sys.exit(1)
        else:
            print("wrong parameters! run 'python analysis.py -h' to see help message")
            sys.exit(1)



# read from excel or csv without header, add header manually
def read_file_toDF():
    if file.endswith('.csv'):
        df = pd.read_csv(file, skiprows=0, usecols=[0,1,5,6,7,8,9,10,11,12])
    elif file.endswith('.xlsx'):
        df = pd.read_excel(file, skiprows=1, usecols=[0,1,5,6,7,8,9,10,11,12])
    else:
        print("not support file type only excel and csv allowed")
        sys.exit(1)
    df.columns = header
    return df

# filter data with protocol. default use tcp
def portocol_filter(df):
    if protocol == 'tcp':
        df = df[df['service'].str.contains('tcp')]
    elif protocol == 'udp':
        df =df[df['service'].str.contains('udp')]
    elif protocol == 'all':
        pass
    return df

# choose outside or inside ip access. default outside ip
def ip_location_filter(df):
    df = df.sort_values('remote_ip')
    if np.isnan(df['remote_ip'].values.all()):
        start = np.where(df['remote_ip'].isnull())[0][0]
        outer = df[:start]
        inner = df[start:]
        if visitor == 'outer':
            return outer
        elif visitor == 'inner':
            return inner
    else:
        outer = df       
    if visitor == 'outer':
        return outer
    elif visitor == 'inner':
        print("no inside access! program will exit...")
        sys.exit(0)

# create a new column with service's port, in order to sort with port
def new_column(df):
    new_line = df['service'].str.split('/',expand=True)[1]
    new_line = new_line.replace('',np.nan)
    df = df.merge(new_line, how='left',left_index=True,right_index=True)
    df.rename(columns={1:'port_num'}, inplace = True)
    return df

# filter data with port. default use 1-10000
def port_filter(df):
    # if protocol is all, sometimes may contain ospf and igmp info. we need filter them out first for sorting
    if protocol == 'all':
        df = df.sort_values('port_num', ascending=True)
        if len(np.where(df['port_num'].isnull())[0]) >= 1:
            nan_begin = np.where(df['port_num'].isnull())[0][0]
            table_int = df[:nan_begin]
            table_nan = df[nan_begin:]
            df = table_int[:]
        df['port_num'] = df['port_num'].astype(int)
        df = df.sort_values('port_num', ascending=True)
    else:
        df['port_num'] = df['port_num'].astype(int)
        df = df.sort_values('port_num', ascending=True)
    if port == 'lower':
        df = df[df['port_num'] <= 10000]
    # after sorting and port filtering, we need to add them back to table if protocol is all
    try:
        df = df.append(table_nan)
    except:
        pass
    return df

# top n times scan
def top_visit(render, head=30, check_points=50):
    ftv = df[:]
    ftv = ftv.sort_values(by=['block_times'], ascending=False)
    ftv = ftv[ftv.block_times > check_points]
    ftv = ftv.head(head)
    # note sort order: first one is the main order
    ftv = ftv.sort_values(['block_times','remote_ip','local_ip'], ascending=[False, True, True])
    if render == 'No':
        dis_line('top n scan')
        if visitor == 'outer':
            ftv = ftv[['local_ip', 'remote_ip', 'service', 'block_times', 'block_first_time', 'block_last_time']]
        elif visitor == 'inner':
            ftv = ftv[['local_ip', 'remote_host_ip', 'service', 'block_times', 'block_first_time', 'block_last_time']]
        remove_index_show(ftv)
        if ftv.shape[0] > 0: print(ftv)
    if render == 'Yes':pic_render(ftv, 'remote_ip','block_times','green','top {} visit'.format(head))
    
# host scan: one scan serveral hosts with the same port
def host_scan(render, host_check_points=0):
    if render == 'No': dis_line('host scan')
    fsh = df[:]
    rfsh = fsh['remote_ip'].value_counts()
    rfsh = rfsh[rfsh > host_check_points]

    # calculate access time delta and show total info
    dis_line("total count")
    for ip in rfsh.index:
        tmp_df = fsh[fsh.remote_ip == ip]
        tmp_df = tmp_df.sort_values('block_last_time')
        begin_time = tmp_df['block_last_time'].values[0]
        end_time = tmp_df['block_last_time'].values[-1]
        begin_time = datetime.datetime.strptime(begin_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        time_delta = end_time - begin_time
        # print(time_delta, ip, tmp_df['block_times'])
        block_count = tmp_df.shape[0]
        if render == 'Yes':
            pass
        else:
            print("ip:%-20s scan %6s times in:     ( %-20s ~ %-20s) still %-5s"%(ip, block_count, begin_time, end_time, time_delta))

    # search host scan info
    dis_line("real host scan")
    for ip in rfsh.index:
        group_ip = fsh[fsh.remote_ip == ip]
        group_ip = group_ip.sort_values('block_last_time')
        group_service = group_ip['service'].value_counts()
        group_service = group_service[group_service > host_check_points]
        for service in group_service.index:
            host = group_ip[group_ip.service == service]
            host_count = host.shape[0]
            begin_time = group_ip['block_last_time'].values[0]
            end_time = group_ip['block_last_time'].values[-1]

            if render == 'Yes':
                pic_render( host, 'local_ip','block_times','orange','{} scan host via {}'.format(ip, service), method='barh')
            else:
                print("ip:%-20s scan %6s hosts via:     %-10s in ( %-10s ~ %-20s)"%(ip, host_count, service, begin_time, end_time))

# port scan: scan one host with several ports
def port_scan(render, port_check_points):
    if render == 'No': dis_line('port scan')
    fps = df[:]
    # find remote_ip which count more than check_points
    rfps = fps['remote_ip'].value_counts()
    rfps = rfps[rfps > port_check_points]

    # loop remote_ip
    for ip in rfps.index:
        # group dataframe with same remote_ip 
        group_ip = fps[fps.remote_ip == ip]
        # count above dataframe which scan local_ip with different ports
        group_host = group_ip['local_ip'].value_counts()
        group_host = group_host[group_host == port_check_points]
        # loop local_ip which matched with check_points
        for host in group_host.index:
            port_df = group_ip[group_ip.local_ip == host]
            # if not all protocol, already sorted in filter port
            if protocol != 'all':
                begin = port_df['port_num'][port_df['port_num'].index[0]]
                end = port_df['port_num'][port_df['port_num'].index[-1]]
                length = port_df.shape[0]
                step = length//10 + 1

                table_int = port_df.sort_values('block_last_time')
                begin_time = table_int['block_last_time'].values[0]
                end_time = table_int['block_last_time'].values[-1]

            elif protocol == 'all':
                if np.isnan(port_df['port_num'].values.all()):
                    # find port's begin nan position
                    nan_begin = np.where(fps['port_num'].isnull())[0][0]
                    table_int = fps[:nan_begin]
                    table_nan = fps[nan_begin:]
                else:
                    table_int = port_df[:]
                    begin_time = table_int['block_last_time'].values[0]
                    end_time = table_int['block_last_time'].values[-1]

                # convert column to int type
                table_int['port_num'] = table_int['port_num'].astype(int)
                table_int = table_int.sort_values('port_num', ascending=True)

                # find scan port range and calculate axis step
                begin = table_int['port_num'][table_int['port_num'].index[0]]
                end = table_int['port_num'][table_int['port_num'].index[-1]]
                length = table_int.shape[0]
                step = length//10 + 1
               
                if np.isnan(port_df['port_num'].values.all()):
                    table = table_int.append(table_nan)
                    table = table.sort_values('block_last_time')
                    begin_time = table['block_last_time'].values[0]
                    end_time = table['block_last_time'].values[-1]

            if render == 'Yes':
                pic_render(table_int, 'service','block_times','brown','{} scan port of {} in  ({} ~ {})'.format(ip, host, begin, end))
                px = plt.gca()
                px.set_xticks([i for i in range(0,length,step)])
                plt.show()  
            else:
                print("ip:%-20s scan %-16s port: (% -5s ~ %-5s) in %-10s %-10s"%(ip, host, begin, end, begin_time, end_time))

# render
def pic_render(dataFrame, x, y, color, title, method=None):
    try:
        if method == 'barh':
            dataFrame.plot.barh(x=x, y=y, color=color, figsize=(10,30), width=0.4)
        if method == 'bar':
            dataFrame.plot.bar(x=x, y=y, color=color, figsize=(18,5), width=0.5)
        if method == 'scatter':
            dataFrame.plot.scatter(x=x, y=y, color=color, figsize=(20,10))
        if method == None:
            if dataFrame.shape[0] <= 50:
                dataFrame.plot.bar(x=x, y=y, color=color, figsize=(18,5), width=0.5)
                plt.xticks(rotation=30)
            if dataFrame.shape[0] > 50:
                dataFrame.plot.scatter(x=x, y=y, color=color, figsize=(20,10))
                plt.xticks(rotation=30)
        plt.title(title)
    except:
        pass

if __name__ == "__main__":
    # sys.argv[1:] = ['-f','/hoem/blueocean/Desktop/blocklogscsv', '-h']
    sys.argv[1:] = ['-f', r'C:\Users\qiyue\Desktop\blocklogs6.2.xlsx']
    # read commandline parameter
    argv = sys.argv[1:]
    set_parameter(argv)

    # filter data
    df = read_file_toDF()
    df = portocol_filter(df)
    df = ip_location_filter(df)
    df = new_column(df)
    df = port_filter(df)


    # data analysis
    # 打印阻断次数的排名（从高到低的排序），默认设置阻断次数大于100次才打印
    top_visit(render, head=head, check_points=top_check_points)
    # 打印单个主机发生阻断行为的统计
    # 打印单个主机针对不同主机进行扫描的行为次数，默认为扫描20个主机：  认为同一个主机使用相同端口对另外20个主机进行了连接，即为主机扫描
    host_scan(render, host_check_points)
    # 打印单个主机针对同一个主机进行端口扫描的行为次数，默认使用10个不同端口:   认为同一个主机对另一个主机进行了10次不同端口的连接，即为端口扫描
    port_scan(render, port_check_points)
