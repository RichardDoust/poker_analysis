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


def limit_10nl(hh_text):
    lines = hh_text.split("\n")
    for line in lines:
        if "($0.05/$0.10)" in line:
            return True


def has_flop(hh_text):
    if "*** FLOP ***" in hh_text:
        return True


def has_pfr(pf_text):
    if "raises" in pf_text:
        return True


def srp_pf(hh_text):
    pf_action = hh_text.split("*** HOLE CARDS ***")[1].split("*** FLOP ***")[0].strip()
    if has_pfr(pf_action):
        lines = pf_action.split("\n")
        if len(lines) == 7:
            return True

def read_data():

    connection = connect_postgres_db()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from cash_hand_histories limit 10000;"

    cursor.execute(postgreSQL_select_Query)
    histories = cursor.fetchall()

    # TODO: limit, heads up, PF raise and call, F xf/f
    print("Print each row and it's columns values")
    count = 0
    for row in histories:
        if limit_10nl(row[1]) and has_flop(row[1]):
            if srp_pf(row[1]):
                count += 1

    print(count)

if __name__ == "__main__":

    read_data()