import psycopg2

try:
    connection = psycopg2.connect(user='ibs',
                                host='127.0.0.1',
                                port='5432',
                                database='IBSng')
    cursor = connection.cursor()
    query = "SELECT change_time,credit_change_id,user_id,before_credit,credit_index FROM credit_change WHERE before_credit < -50"
    cursor.execute(query)
    records = cursor.fetchall()

    with open('negative_credit_change','w') as f:
        f.write('change_time,credit_change_id,user_id,before_credit,credit_index\n')
        for record in records:
            f.write("%s,%s,%s,%s,%s\n" % (record[0],record[1],record[2],record[3],record[4]))

except (Exception,psycopg2.Error) as error:
    print("connection failed !!!",error)


finally:

    if(connection):
        cursor.close()
        connection.close()
        print("Finished")
