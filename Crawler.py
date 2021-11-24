from logging import exception
from typing_extensions import Required
from random import shuffle , choice
import psycopg
from psycopg import sql
import argparse

def connectToDatabase(username: str, _password: str, database: str):
    print("host=localhost dbname=" + database + " user=" + username + "  password='" + _password + "'")
    conn = psycopg.connect(host ='localhost', dbname = database, user= username, password= _password)
    conn.autocommit= True
    return conn

def createRole(roleName: str, password: str, conn : psycopg.Connection):
    cursor = conn.cursor()
    cursor.execute(sql.SQL("CREATE ROLE '{}' WITH LOGIN PASSWORD '{}' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT NOREPLICATION CONNECTION LIMIT -1;").format(
        sql.Identifier(roleName),
        sql.Identifier(password)
    ))

def createDatabase(databaseName: str, owner: str, conn: psycopg.Connection):
    cursor =  conn.cursor()   
    cursor.execute(sql.SQL("CREATE DATABASE {} OWNER {}").format(sql.Identifier(databaseName), sql.Identifier(owner)))

def seedTables(conn: psycopg.Connection):
    cursor = conn.cursor()
    cursor.execute('')

def generatePassword(length:int, minSpecialChars:int, minUppercase:int, minLowercase:int, minNumber:int ):
    if (length < (minSpecialChars + minUppercase + minLowercase +minNumber)):
        raise Exception('You are really bad at math.') 
    
    password = "".rjust(minSpecialChars,"S")
    password += "".rjust(minUppercase, "U")
    password += "".rjust(minLowercase,"L")
    password += "".rjust(minNumber, "N")
    password = password.rjust(length, "L")
    i = 0
    temp = []
    while i < length: 
        temp.append(chr(choice({'S': list(range(40,43)),'U': list(range(65,90)),'L': list(range(97,122)), 'N': list(range(48,57))}[password[i]])))
        i += 1
    shuffle(temp)
    return "".join(temp)

parser  = argparse.ArgumentParser()

parser.add_argument('-username' ,metavar='N', type=str, help='Database Username', required=True)
parser.add_argument('-password' ,metavar='N', type=str, help='Database Password', required=True)
parser.add_argument('-database' ,metavar='N', type=str, help='Database to connect to', required=True)
parser.add_argument('--createDatabaseUser' ,metavar='Y', type=bool, help='Create Database User', required=False)
parser.add_argument('--createUserNamed' ,metavar='Y', type=bool, help='Create Database User', required=False)
parser.add_argument('--createDatabase' ,metavar='Y', type=bool, help='Create Database', required=False)
args = parser.parse_args()
print(args)

conn = connectToDatabase(args.username, args.password, args.database)
if args.createDatabase:
    createDatabase('test', args.username, conn)
if args.createUser & args.createUserNamed:
    createRole() 
    
print(conn.closed)
print(conn.close())
