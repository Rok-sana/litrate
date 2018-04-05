from usefull_classes.database import MySqlDatabase
from misc.configs import DATABASE_CONFIG
from mySql.basic_information_add import add_information
import os
import shutil

tables = ['Types_Proses', 'Types_Poems', 'Accepted_Proses_Dialogs', 'Accepted_Collections_Dialogs', 'Accepted_Collections', 'Accepted_Proses', 'Offer_Statuses', 'Issues', 'Sent_Collections', 'Sent_Proses', 'Poems_Collections', 'Collections',
          'Comments', 'Proses', 'Poems', 'Poem_types', 'Prose_types', 'Compositions',
          'Moderators', 'Publishers', 'Creators', 'Users', 'User_types']


def _delete_all_tables(db: MySqlDatabase):
    for table in tables:
        query = "DROP TABLE IF EXISTS {0} CASCADE;".format(table)
        db.execute_query(query)


def _create_table_user_types(db: MySqlDatabase):
    query = "CREATE TABLE User_types ( " \
            "user_type VARCHAR(30) CHARACTER SET utf8 NOT NULL PRIMARY KEY );"
    db.execute_query(query)


def _create_table_users(db: MySqlDatabase):
    query = "CREATE TABLE Users ( " \
            "user_id INT NOT NULL PRIMARY KEY, " \
            "user_name VARCHAR(60) CHARACTER SET utf8, " \
            "user_surname VARCHAR(60) CHARACTER SET utf8, " \
            "user_patronymic VARCHAR(60) CHARACTER SET utf8, " \
            "user_mail VARCHAR(60) CHARACTER SET utf8 NOT NULL, " \
            "user_login VARCHAR(60) NOT NULL, " \
            "user_password VARCHAR(320) NOT NULL, " \
            "user_additional_info VARCHAR(100), " \
            "user_phone VARCHAR(15), " \
            "user_birth DATE, " \
            "banned BOOL DEFAULT FALSE, " \
            "user_type VARCHAR(30) CHARACTER SET utf8 NOT NULL," \
            "UNIQUE(user_login), " \
            "UNIQUE(user_mail), " \
            "FOREIGN KEY (user_type) " \
            "REFERENCES User_types(user_type) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_creators(db: MySqlDatabase):
    query = "CREATE TABLE Creators ( " \
            "creator_id INT NOT NULL PRIMARY KEY, " \
            "rating INT NOT NULL, " \
            "country VARCHAR(60) CHARACTER SET utf8, " \
            "city VARCHAR(60) CHARACTER SET utf8, " \
            "FOREIGN KEY (creator_id) " \
            "REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_publishers(db: MySqlDatabase):
    query = "CREATE TABLE Publishers ( " \
            "publisher_id INT NOT NULL PRIMARY KEY, " \
            "rating INT NOT NULL, " \
            "publisher_house_name VARCHAR(60) CHARACTER SET utf8 NOT NULL, " \
            "country VARCHAR(60) CHARACTER SET utf8, " \
            "city VARCHAR(60) CHARACTER SET utf8, " \
            "street VARCHAR(60) CHARACTER SET utf8, " \
            "FOREIGN KEY (publisher_id) " \
            "REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_moderators(db: MySqlDatabase):
    query = "CREATE TABLE Moderators ( " \
            "moderator_id INT NOT NULL PRIMARY KEY, " \
            "FOREIGN KEY (moderator_id) " \
            "REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_compositions(db: MySqlDatabase):
    query = "CREATE TABLE Compositions ( " \
            "composition_id INT NOT NULL PRIMARY KEY, " \
            "composition_name VARCHAR(60) CHARACTER SET utf8 NOT NULL, " \
            "creator_id INT NOT NULL, " \
            "rating INT NOT NULL, " \
            "posting_date DATE NOT NULL, " \
            "composition_type VARCHAR(60) CHARACTER SET utf8 NOT NULL, " \
            "modifier VARCHAR(60) NOT NULL, " \
            "FOREIGN KEY (creator_id) " \
            "REFERENCES Creators(creator_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_prose_types(db: MySqlDatabase):
    query = "CREATE TABLE Prose_types ( " \
            "prose_type VARCHAR(40) CHARACTER SET utf8 NOT NULL PRIMARY KEY );"
    db.execute_query(query)


def _create_table_poem_types(db: MySqlDatabase):
    query = "CREATE TABLE Poem_types ( " \
            "poem_type VARCHAR(40) CHARACTER SET utf8 NOT NULL PRIMARY KEY );"
    db.execute_query(query)


def _create_table_poems(db: MySqlDatabase):
    query = "CREATE TABLE Poems ( " \
            "poem_id INT NOT NULL PRIMARY KEY, " \
            "FOREIGN KEY (poem_id) " \
            "REFERENCES Compositions(composition_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_proses(db: MySqlDatabase):
    query = "CREATE TABLE Proses ( " \
            "prose_id INT NOT NULL PRIMARY KEY, " \
            "FOREIGN KEY (prose_id) " \
            "REFERENCES Compositions(composition_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_types_proses(db: MySqlDatabase):
    query = "CREATE TABLE Types_Proses ( " \
            "prose_id INT NOT NULL, " \
            "prose_type VARCHAR(40) CHARACTER SET utf8 NOT NULL, " \
            "FOREIGN KEY (prose_id) " \
            "REFERENCES Proses(prose_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (prose_type) " \
            "REFERENCES Prose_types(prose_type) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_types_poems(db: MySqlDatabase):
    query = "CREATE TABLE Types_Poems ( " \
            "poem_id INT NOT NULL, " \
            "poem_type VARCHAR(40) CHARACTER SET utf8 NOT NULL, " \
            "FOREIGN KEY (poem_id) " \
            "REFERENCES Poems(poem_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (poem_type) " \
            "REFERENCES Poem_types(poem_type) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_comments(db: MySqlDatabase):
    query = "CREATE TABLE Comments ( " \
            "comment_id INT NOT NULL PRIMARY KEY, " \
            "user_id INT NOT NULL, " \
            "composition_id INT NOT NULL, " \
            "post_date DATE NOT NULL, " \
            "FOREIGN KEY (user_id) " \
            "REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (composition_id) " \
            "REFERENCES Compositions(composition_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_collections(db: MySqlDatabase):
    query = "CREATE TABLE Collections ( " \
            "collection_id INT NOT NULL PRIMARY KEY, " \
            "creator_id INT NOT NULL, " \
            "post_date DATE NOT NULL, " \
            "collection_name VARCHAR(60) CHARACTER SET utf8 NOT NULL, " \
            "FOREIGN KEY (creator_id) " \
            "REFERENCES Creators(creator_id) ON UPDATE CASCADE ON DELETE CASCADE);"
    db.execute_query(query)


def _create_table_poems_collections(db: MySqlDatabase):
    query = "CREATE TABLE Poems_Collections ( " \
            "collection_id INT NOT NULL, " \
            "poem_id INT NOT NULL, " \
            "FOREIGN KEY (collection_id) " \
            "REFERENCES Collections(collection_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (poem_id) " \
            "REFERENCES Poems(poem_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_sent_collections(db: MySqlDatabase):
    query = "CREATE TABLE Sent_Collections ( " \
            "offer_id INT NOT NULL PRIMARY KEY, " \
            "collection_id INT NOT NULL, " \
            "publisher_id INT NOT NULL, " \
            "FOREIGN KEY (collection_id) " \
            "REFERENCES Collections(collection_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (publisher_id) " \
            "REFERENCES Publishers(publisher_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_sent_proses(db: MySqlDatabase):
    query = "CREATE TABLE Sent_Proses ( " \
            "offer_id INT NOT NULL PRIMARY KEY, " \
            "prose_id INT NOT NULL, " \
            "publisher_id INT NOT NULL, " \
            "FOREIGN KEY (prose_id) " \
            "REFERENCES Proses(prose_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (publisher_id) " \
            "REFERENCES Publishers(publisher_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_issues(db: MySqlDatabase):
    query = "CREATE TABLE Issues ( " \
            "issue_id INT NOT NULL PRIMARY KEY, " \
            "moderator_id INT NOT NULL, " \
            "FOREIGN KEY (moderator_id) " \
            "REFERENCES Moderators(moderator_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_offer_statuses(db: MySqlDatabase):
    query = "CREATE TABLE Offer_Statuses ( " \
            "status VARCHAR(60) CHARACTER SET utf8 NOT NULL PRIMARY KEY);"

    db.execute_query(query)


def _create_table_accepted_proses(db: MySqlDatabase):
    query = "CREATE TABLE Accepted_Proses ( " \
            "offer_id INT NOT NULL PRIMARY KEY, " \
            "prose_id INT NOT NULL, " \
            "publisher_id INT NOT NULL, " \
            "date DATE NOT NULL, " \
            "status VARCHAR(60) CHARACTER SET utf8 NOT NULL, " \
            "rating INT DEFAULT 0, " \
            "FOREIGN KEY (status) " \
            "REFERENCES Offer_Statuses(status) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (prose_id) " \
            "REFERENCES Proses(prose_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (publisher_id) " \
            "REFERENCES Publishers(publisher_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_accepted_collections(db: MySqlDatabase):
    query = "CREATE TABLE Accepted_Collections ( " \
            "offer_id INT NOT NULL PRIMARY KEY, " \
            "collection_id INT NOT NULL, " \
            "publisher_id INT NOT NULL, " \
            "date DATE NOT NULL, " \
            "status VARCHAR(60) CHARACTER SET utf8 NOT NULL, " \
            "rating INT DEFAULT 0, " \
            "FOREIGN KEY (status) " \
            "REFERENCES Offer_Statuses(status) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (collection_id) " \
            "REFERENCES Collections(collection_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (publisher_id) " \
            "REFERENCES Publishers(publisher_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_accepted_proses_dialogs(db: MySqlDatabase):
    query = "CREATE TABLE Accepted_Proses_Dialogs ( " \
            "offer_id INT NOT NULL PRIMARY KEY, " \
            "user_id INT NOT NULL, " \
            "date DATE NOT NULL, " \
            "message VARCHAR(300) CHARACTER SET utf8 NOT NULL, " \
            "FOREIGN KEY (offer_id) " \
            "REFERENCES Accepted_Proses(offer_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (user_id) " \
            "REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_table_accepted_collections_dialogs(db: MySqlDatabase):
    query = "CREATE TABLE Accepted_Collections_Dialogs ( " \
            "offer_id INT NOT NULL PRIMARY KEY, " \
            "user_id INT NOT NULL, " \
            "date DATE NOT NULL, " \
            "message VARCHAR(300) CHARACTER SET utf8 NOT NULL, " \
            "FOREIGN KEY (offer_id) " \
            "REFERENCES Accepted_Collections(offer_id) ON UPDATE CASCADE ON DELETE CASCADE, " \
            "FOREIGN KEY (user_id) " \
            "REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE CASCADE );"
    db.execute_query(query)


def _create_database(db: MySqlDatabase):
    _create_table_user_types(db)
    _create_table_users(db)
    _create_table_creators(db)
    _create_table_publishers(db)
    _create_table_moderators(db)
    _create_table_compositions(db)
    _create_table_prose_types(db)
    _create_table_poem_types(db)
    _create_table_poems(db)
    _create_table_proses(db)
    _create_table_types_proses(db)
    _create_table_types_poems(db)
    _create_table_comments(db)
    _create_table_collections(db)
    _create_table_poems_collections(db)
    _create_table_sent_collections(db)
    _create_table_sent_proses(db)
    _create_table_issues(db)
    _create_table_offer_statuses(db)
    _create_table_accepted_proses(db)
    _create_table_accepted_collections(db)
    _create_table_accepted_proses_dialogs(db)
    _create_table_accepted_collections_dialogs(db)


def create_dir_for_files():
    directory = "../data/"
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


# !!!! will delete all data !!!!
def refresh_database():
    database = MySqlDatabase(DATABASE_CONFIG)
    _delete_all_tables(database)
    _create_database(database)
    add_information()
    create_dir_for_files()
    print(database.all_tables())


if __name__ == "__main__":
    refresh_database()
