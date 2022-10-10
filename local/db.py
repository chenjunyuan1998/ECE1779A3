import mysql.connector

from app.config import db_config


def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])


def get_images():
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = "SELECT * FROM `ImageDB`.`Image`;"
    cursor.execute(query)

    lst_of_images = []
    for row in cursor:
        lst_of_images.append(row)
    return lst_of_images


def put_image(name, location):
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "INSERT INTO `ImageDB`.`Image` (`name`, `location`) VALUES ('{}', '{}');"
    cursor.execute(query.format(name, location))
    cnx.commit()


def delete_image(name):
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "DELETE FROM `ImageDB`.`Image` WHERE `name` = '{}'"
    cursor.execute(query.format(name))

    cnx.commit()


def get_stats():
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = "SELECT * FROM `ImageDB`.`Stats`;"
    cursor.execute(query)

    # return the latest statistic stored in `ImageDB`.`Stats`
    latest = None
    for row in cursor:
        print(row)
        latest = row
    return latest


def put_stats(num_items, size_items, num_requests, db_num_hit, db_num_miss):
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "INSERT INTO `ImageDB`.`Stats` (`num_items`, `size_items`, `num_requests`, " \
            + "`num_hit`, `num_miss`, `_timestamp`)" \
            + "VALUES ({}, {}, {}, {}, {}, CURRENT_TIMESTAMP);"
    cursor.execute(query.format(num_items, size_items, num_requests, db_num_hit, db_num_miss))
    cnx.commit()


def get_config():
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = "SELECT capacity, replacement_policy FROM `ImageDB`.`Config`;"
    cursor.execute(query)

    for row in cursor:
        return row


def put_config(capacity, replace_policy):
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "SELECT capacity, replacement_policy FROM `ImageDB`.`Config`;"
    cursor.execute(query)

    rowcount = 0
    for _ in cursor:
        rowcount += 1
    print("put_config rowcount: ", rowcount)

    if rowcount == 0:  # table `ImageDB`.`Config` is empty
        query = "INSERT INTO `ImageDB`.`Config` (`capacity`, `replacement_policy`) VALUES ({}, '{}');"
        cursor.execute(query.format(capacity, replace_policy))
    else:  # table `ImageDB`.`Config` is not empty
        query = "UPDATE `ImageDB`.`Config` SET `capacity` = {}, `replacement_policy` = '{}';"
        cursor.execute(query.format(capacity, replace_policy))

    cnx.commit()

    return cursor.rowcount


# for testing
def clear_stats():
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "DELETE FROM `ImageDB`.`Stats` WHERE NOT `sid` = 1"
    cursor.execute(query)

    cnx.commit()


if __name__ == "__main__":
    # test get/put image
    print("========== test get/put image ==========")
    no_image = get_images()
    print("no_image get_image result: ", no_image)

    put_image("img1.png", "/Users/images/img1")
    first_image = get_images()
    print("first put_image result: ", first_image)

    put_image("img2.png", "/Users/images/img2")
    second_image = get_images()
    print("second put_image result: ", second_image)

    delete_image("img1.png")
    delete_image = get_images()
    print("delete_image img1 result: ", delete_image)

    # test get/put stats
    print("")
    print("========== test get/put stats ==========")
    put_stats(1, 1, 1, 1, 1)
    latest_stat = get_stats()
    print("get_stats() result: ", latest_stat)

    clear_stats()
    stat = get_stats()
    print("clear_stats() result: ", stat)

    # test get/put config
    print("")
    print("========== test get/put config ==========")
    empty_config = get_config()
    print(empty_config)

    put_config(1 * 1024 * 1024, "LRU")
    first_config = get_config()
    print("first put_config result: ", first_config)

    put_config(0, "Random")
    second_config = get_config()
    print("second put_config result: ", second_config)
