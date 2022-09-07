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


def pf_raiser(hh_text):
    pf_action = hh_text.split("*** HOLE CARDS ***")[1].split("*** FLOP ***")[0].strip()
    if has_pfr(pf_action):
        lines = pf_action.split("\n")
        for line in lines:
            if "raises" in line:
                raiser = line.split(":")[0]
                return raiser


def pf_caller(hh_text):
    pf_action = hh_text.split("*** HOLE CARDS ***")[1].split("*** FLOP ***")[0].strip()
    if has_pfr(pf_action):
        lines = pf_action.split("\n")
        for line in lines:
            if "calls" in line:
                caller = line.split(":")[0]
                return caller


def cbet_and_fold(hh_text):

    pfrer = pf_raiser(hh_text)
    pfcer = pf_caller(hh_text)
    f_action = hh_text.split("*** FLOP ***")[1].split("*** SUMMARY ***")[0].strip()
    lines = f_action.split("\n")
    i = 0
    result = ""
    for line in lines:
        if pfcer in line and "bets" in line:
            print("\n")
            print("DONK")
            print("DONK")
            print("DONK")
            print(hh_text)
            result = "donk"
            break
        if pfrer in line and "checks" in line:
            print("\n")
            print("DOESN'T CBET")
            print("DOESN'T CBET")
            print("DOESN'T CBET")
            print(hh_text)
            result = "no_cbet"
            break
        if pfcer in line and "raises" in line:
            print("\n")
            print("FAILED CBET")
            print("FAILED CBET")
            print("FAILED CBET")
            print(hh_text)
            result = False
            break
        if pfcer in line and "calls" in line:
            print("\n")
            print("FAILED CBET")
            print("FAILED CBET")
            print("FAILED CBET")
            print(hh_text)
            result = False
            break

    if result == "":
        print("\n")
        print("SUCCESSFUL CBET")
        print("SUCCESSFUL CBET")
        print("SUCCESSFUL CBET")
        print(hh_text)
        result = True

    return result

def has_no_turn(hh_text):
    if "*** TURN ***" not in hh_text:
        return True

def read_data():

    connection = connect_postgres_db()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from cash_hand_histories limit 10000;"

    cursor.execute(postgreSQL_select_Query)
    histories = cursor.fetchall()

    # TODO: limit, heads up, PF raise and call, F xf/f
    print("Print each row and it's columns values")
    count_cbet_fold = 0
    count_failed_cbet = 0
    count_no_cbet = 0
    count_donk = 0
    for row in histories:
        if limit_10nl(row[1]):
            if has_flop(row[1]):
                if srp_pf(row[1]) and has_no_turn(row[1]):
                    if cbet_and_fold(row[1]) == "donk":
                        count_donk += 1
                        print(count_donk)
                        continue
                    if cbet_and_fold(row[1]) == "no_cbet":
                        count_no_cbet += 1
                        print(count_no_cbet)
                        continue
                    if cbet_and_fold(row[1]):
                        count_cbet_fold += 1
                        print(count_cbet_fold)
                    else:
                        count_failed_cbet += 1
                        print(count_failed_cbet)

    print(count_cbet_fold)
    print(count_failed_cbet)
    print(count_no_cbet)
    print(count_donk)

    cursor.close()
    connection.close()

if __name__ == "__main__":

    read_data()