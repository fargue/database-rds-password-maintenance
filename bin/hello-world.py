#!/usr/bin/env python3

import boto3
import PySimpleGUI as sg
import cx_Oracle


def GenerateBasicConnectSting(db):
    return

def DatabaseFromRDS():
    rds = boto3.client('rds')
    # create dictionary of db's keyed by id
    databases={}
    try:
        # get all of the db instances
        dbs = rds.describe_db_instances()
        for db in dbs['DBInstances']:
            dbInfo = {}
            print(db)
            print("Engine        : % s" % (db['Engine']))
            if 'oracle' not in db['Engine']:
                print("Skipping db type % s" % (db['Engine']))
                continue
            if 'DBName' not in db:
                print("No DBName defined for : % s" % (db['Endpoint']['Address']))
                continue
            if db['DBInstanceStatus'] != 'available':
                print("Instance: % s is not available" % (db['Endpoint']['Address']))
                continue
            # print("Address        : % s" % (db['Endpoint']['Address']))
            # print("Port           : % s" % (db['Endpoint']['Port']))
            # print("DBName         : % s" % (db['DBName']))
            dbInfo = {
                'id': db['DBInstanceIdentifier'],
                'address': db['Endpoint']['Address'],
                'port': db['Endpoint']['Port'],
                'name': db['DBName']
            }
            databases[db['DBInstanceIdentifier']] = dbInfo
    except Exception as error:
        print("error:")
        print(error)

    return databases

def DatabaseChoose(databases):

    # extract dbname from dictionary
    dbList=[]
    for dbId in databases:
        dbList.append(dbId)

    layout = [
        [sg.Text('Database Selector', font=("Helvetica", 15), size=(20, 1), text_color='green')],
        [sg.Text('File Selection', font=("Helvetica", 15), size=(20, 1))],
        [sg.Text('UserName', size=(22,1)), sg.InputText(size=(65, 1), key='username')],
        [sg.Text('_' * 250, auto_size_text=False, size=(100, 1))],
        [   sg.Text('Choose Database', size=(22, 1)),
            sg.InputCombo(values=dbList, size=(30, 1), key='database')
        ],
        [sg.Text('_' * 250, auto_size_text=False, size=(100, 1))],
        [sg.Text(size=(40,1), key='-OUTPUT-', text_color='red')],
        [
            sg.Submit(size=(8, 1), button_color=('red', 'white'), font=("Helvetica", 15), bind_return_key=True), 
            sg.Text(' ' * 2, size=(4, 1)),
            sg.Cancel(size=(8, 1), font=("Helvetica", 15))
        ]
    ]

    window = sg.Window('Database Selector', auto_size_text=False, default_element_size=(30, 1), font=("Helvetica", 12)).Layout(layout)
    while True:
        event, values = window.read()
        print('button is: {}, values is: {}'.format(event, values))
        if event == 'Submit':
            print('user hit submit button. values: {}'.format(values))
            message = ''
            if not values['username']:
                message += 'You must enter a username. '
            if not values['database']:
                message += 'You must select one database. '
            # message is not null so display it and try again
            if message:
                window['-OUTPUT-'].update(message)
            else:
                print('got what we needed')
                break
        elif event in (sg.WIN_CLOSED,'Cancel'):
            print('breaking out of loop due to event {}'.format(event))
            break
        else:
            print('Unknown event: {}'.format(event))

    window.close()
    return values

# main
sg.ChangeLookAndFeel('LightGreen')      
sg.SetOptions(element_padding=(0, 0))  

# ------ Menu Definition ------ #      
menu_def = [
    ['Main', ['Exit' ]],      
    ['Database', ['Load','Add', 'Update', 'Delete']],
    ['Help', 'About...']
]      

# ------ GUI Defintion ------ #      
layout = [
    [sg.Menu(menu_def, )],
    [sg.Text('Current Database', size=(22,1)), sg.Text(size=(40,1), key='database', text_color='red')],
    [sg.Text('Current UserName', size=(22,1)), sg.Text(size=(40,1), key='username', text_color='red')],
    [sg.Text('_' * 250, auto_size_text=False, size=(100, 1))],
    [sg.Text(size=(100,5), key='-OUTPUT-', text_color='red')]
]     

window = sg.Window(
    "Database Maintenance", layout, default_element_size=(12, 1), auto_size_text=False,
    auto_size_buttons=True,      
    default_button_element_size=(12, 1)
    )

databases=[]
# ------ Loop & Process button menu choices ------ #      
while True:
    message=''
    event, values = window.read()      
    if event == sg.WIN_CLOSED or event == 'Exit':      
        break
    print('Button = ', event)
    # ------ Process menu choices ------ #      
    if event == 'About...':      
        sg.popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...')      
    elif event == 'Load':
        databases = DatabaseFromRDS()
        message += 'loaded {} databases from rds.'.format(len(databases))
    elif event == 'Update':
        if not databases:
            message += 'You must load databases first'
        else:
            db = DatabaseChoose(databases)   
            print('user selected database: {}'.format(db))
            window['username'].update(db['username'])
            window['database'].update(db['database'])
    else:
        print('unknown event: {}'.format(event))
    # message is not null so display it and try again
    if message:
        window['-OUTPUT-'].update(message)

window.close()
print('done...')