import mysql.connector

from BackendApp.config import db_config


def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])


def get_key_list():
    """
    :return: a list of tuples of keys
    """
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = "SELECT `_key` FROM `ImageDB`.`Image`;"
    cursor.execute(query)

    lst_of_images = []
    for row in cursor:
        lst_of_images.append(row)
    return lst_of_images


def get_image_with_key(key):
    """
    :param key: key(unique)
    :return: a tuple of (name, location) of the image if key exists; None if key doesn't exist
    """
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = "SELECT `name`, `location` FROM `ImageDB`.`Image` WHERE `_key` = '{}';"
    cursor.execute(query.format(key))

    for row in cursor:
        return row


def put_image(key, name, location):
    """
    This function
    1. insert into the table a new instance of image if key doesn't exist
    2. replace the image name and location if key already exists
    :param key: key (unique)
    :param name: name of image
    :param location: location of image
    :return: -1 if error occurs
    """
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "SELECT `name`, `location` FROM `ImageDB`.`Image` WHERE `_key` = '{}';"
    cursor.execute(query.format(key))

    count = 0
    for _ in cursor:
        count += 1

    if count == 0:
        query = "INSERT INTO `ImageDB`.`Image` (`_key`, `name`, `location`) VALUES ('{}', '{}', '{}');"
        cursor.execute(query.format(key, name, location))
        cnx.commit()
    elif count == 1:
        query = "UPDATE `ImageDB`.`Image` SET `name` = '{}', `location` = '{}' WHERE `_key` = '{}';"
        cursor.execute(query.format(name, location, key))
        cnx.commit()
    else:
        return -1


def delete_image(key):
    """
    :param key: key (unique)
    :return: -1 if key doesn't exist
    """
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "SELECT `name`, `location` FROM `ImageDB`.`Image` WHERE `_key` = '{}';"
    cursor.execute(query.format(key))

    count = 0
    for _ in cursor:
        count += 1

    if count == 1:
        query = "DELETE FROM `ImageDB`.`Image` WHERE `_key` = '{}'"
        cursor.execute(query.format(key))
        cnx.commit()
    else:
        return -1


def get_stats():
    """
    :return: a tuple of latest statistics
    (num_items, size_items, num_requests, db_num_hit, db_num_miss, _timestamp)
    """
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = "SELECT `num_items`, `size_items`, `num_requests`, `num_hit`, " \
            "`num_miss`, `_timestamp` FROM `ImageDB`.`Stats`;"
    cursor.execute(query)

    # return the latest statistic stored in `ImageDB`.`Stats`
    latest = None
    for row in cursor:
        # print(row)
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
    """
    :return: a tuple of configuration (capacity, replace_policy)
    """
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = "SELECT `capacity`, `replacement_policy` FROM `ImageDB`.`Config`;"
    cursor.execute(query)

    for row in cursor:
        return row


def put_config(capacity, replace_policy):
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "SELECT `capacity`, `replacement_policy` FROM `ImageDB`.`Config`;"
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


# ========== functions for testing ==========
def get_image_list():
    """
    :return: a list of tuples of images
    """
    cnx = connect_to_database()
    cursor = cnx.cursor()
    query = "SELECT `_key`, `name`, `location` FROM `ImageDB`.`Image`;"
    cursor.execute(query)

    lst_of_images = []
    for row in cursor:
        lst_of_images.append(row)
    return lst_of_images


def clear_stats():
    cnx = connect_to_database()
    cursor = cnx.cursor()

    query = "DELETE FROM `ImageDB`.`Stats` WHERE NOT `sid` = 1"
    cursor.execute(query)

    cnx.commit()


if __name__ == "__main__":
    # test get/put image
    print("========== test get/put image ==========")
    no_image = get_image_list()
    print("no_image get_image result: ", no_image)

    put_image("key1", "img1.png", "/Users/images/img1")
    first_image = get_image_list()
    print("first put_image result: ", first_image)

    put_image("key2", "img2.png", "/Users/images/img2")
    second_image = get_image_list()
    print("second put_image result: ", second_image)

    lst_of_keys = get_key_list()
    print(lst_of_keys)

    put_image("key1", "img1.png", "/Users/images/new_img1")
    update_image = get_image_list()
    print("same image update put_image result: ", update_image)

    specific_image = get_image_with_key("key1")
    print("get_image_with_key result: ", specific_image)

    specific_key3_image = get_image_with_key("key3")
    print("get_image_with_key result: ", specific_key3_image)

    delete_image("key1")
    delete_image1 = get_image_list()
    print("delete_image key1 result: ", delete_image1)

    result = delete_image("key3")
    print("return value of delete_image('key3'): ", result)
    delete_image_error = get_image_list()
    print("delete_image key3 result: ", delete_image_error)

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
