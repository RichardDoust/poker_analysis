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
            # print("\n")
            # print("DONK")
            # print("DONK")
            # print("DONK")
            # print(hh_text)
            result = "donk"
            break
        if pfrer in line and "checks" in line:
            # print("\n")
            # print("DOESN'T CBET")
            # print("DOESN'T CBET")
            # print("DOESN'T CBET")
            # print(hh_text)
            result = "no_cbet"
            break
        if pfcer in line and "raises" in line:
            # print("\n")
            # print("FAILED CBET")
            # print("FAILED CBET")
            # print("FAILED CBET")
            # print(hh_text)
            result = False
            break
        if pfcer in line and "calls" in line:
            # print("\n")
            # print("FAILED CBET")
            # print("FAILED CBET")
            # print("FAILED CBET")
            # print(hh_text)
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


def cbet(hh_text):
    result = ""
    pfrer = pf_raiser(hh_text)
    if "*** TURN ***" in hh_text:
        f_action = hh_text.split("*** FLOP ***")[1].split("*** TURN ***")[0].strip()
    else:
        f_action = hh_text.split("*** FLOP ***")[1].split("*** SUMMARY ***")[0].strip()

    lines = f_action.split("\n")
    i = 0
    for line in lines:
        if pfrer in line and "bets" in line:
            if "folds" in lines[i+1]:
                result = "cbet_success"
                print("\n")
                print(hh_text)
            else:
                result = "cbet_failed"
            break
        i += 1

    return result


def heads_up(hh_text):
    result = False
    pf_action = hh_text.split("*** HOLE CARDS ***")[1].split("*** FLOP ***")[0].strip()
    no_calls = pf_action.count("calls")
    if no_calls < 2:
        result = True

    return result


def read_data():

    # connection = connect_postgres_db()

    connection = psycopg2.connect(user="postgres",
                                  password="dbpass",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="PT4 DB")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from cash_hand_histories order by id_hand limit 100000;"

    cursor.execute(postgreSQL_select_Query)
    histories = cursor.fetchall()

    # TODO: limit, heads up, PF raise and call, F xf/f
    print("Print each row and it's columns values")
    count_cbet_success = 0
    count_cbet_failed = 0
    for row in histories:
        if limit_10nl(row[1]):
            if has_flop(row[1]):
                if srp_pf(row[1]):
                    if heads_up(row[1]):
                        if cbet(row[1]) == "cbet_success":
                            count_cbet_success += 1
                            continue
                        if cbet(row[1]) == "cbet_failed":
                            count_cbet_failed += 1
                            continue

    print("cbet success: " + str(count_cbet_success))
    print("cbet failed: " + str(count_cbet_failed))
    print("total hands cbet: " + str(count_cbet_success + count_cbet_success))
    print("cbet success %: " + str(count_cbet_success/ (count_cbet_success + count_cbet_failed)))

    cursor.close()
    connection.close()


if __name__ == "__main__":

    read_data()