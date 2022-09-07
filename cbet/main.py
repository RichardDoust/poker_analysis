import psycopg2

def connect_postgres_db():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="dbpass",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="PT4 DB")

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    return connection


def read_data():

    connection = connect_postgres_db()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from cash_hand_histories limit 100;"

    cursor.execute(postgreSQL_select_Query)
    histories = cursor.fetchall()

    print("Print each row and it's columns values")
    for row in histories:
        print(row[0])
        print(row[1])


if __name__ == "__main__":

    read_data()