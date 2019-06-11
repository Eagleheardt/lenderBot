import sqlite3
import numpy as np

MAIN_CONNECTION = None

def EXEC(sqlCmd): # fetches data from the database
	try:
		someCursor = MAIN_CONNECTION.cursor()
		someCursor.execute(sqlCmd)
		someCursor.close()
		MAIN_CONNECTION.commit() 

		return 0

	except TypeError:
		return 7

	except ValueError:
		return 8

	except:
		return 9

def GET(sqlCmd):
	try:
		someCursor = MAIN_CONNECTION.cursor()
		someCursor.execute(sqlCmd)
		result = someCursor.fetchall()

	except:
		return -1

	finally:
		someCursor.close()

	return result

def SELECT_ALL(tableName): # returns a list of lists
	cmd = """
		SELECT * 
		FROM {0};
	""".format(tableName)

	return GET(cmd)

def SIMPLE_INSERT(tableName, column, value):
	cmd = """
		INSERT INTO 
			{0} ({1})
		VALUES
			({2});
	""".format(tableName, column, value)

	return EXEC(cmd)

def VARIABLE_INSERT(tableName, amtOfColumns, vArgs): 
	if len(vArgs) % amtOfColumns != 0:
		return 2

	comma =","
	argList = np.reshape(vArgs, (-1, amtOfColumns))

	columnsToUse = ""
	valuesToUse = []
	
	for x, i in enumerate(argList):
		i = np.array2string(i, separator=',').replace('[','').replace(']','')
		if x == 0:
			columnsToUse = i
			continue
		valuesToUse.append(i)

	code = 0

	for i in valuesToUse:
		code = SIMPLE_INSERT(tableName, columnsToUse, i)
		if code != 0:
			return code

	return code

def SIMPLE_UPDATE(tableName, updateColumn, updateValue, whereColumn, whereCondition):
	cmd = """
		UPDATE {0}
		SET {1} = {2}
		WHERE {3} = {4};
	""".format(tableName, updateColumn, updateValue, whereColumn, whereCondition)

	return EXEC(cmd)

def SIMPLE_DELETE(tableName, whereColumn, whereCondition):
	cmd = """
		DELETE FROM {0}
        WHERE {1} = {2};
	""".format(tableName, whereColumn, whereCondition)

	return EXEC(cmd)

#################################
###   Parameterized Queries   ###
#################################

# # example 1 -- simple placeholders
# db.execute('update players set name=?, score=?, active=? where jerseyNum=?', ('Smith, Steve', 42, True, 99))
 
# # example 2 -- named placeholders
# db.execute('update players set name=:name, score=:score, active=:active where jerseyNum=:num',
#     {'num': 100,
#      'name': 'John Doe',
#      'active': False,
#      'score': -1}
# )