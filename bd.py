import psycopg2


class UsersBd:

    def __init__(self):
        self.database = 'vk_user'
        self.user = 'postgres'
        self.password = '...'
        self.connect = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        self.cursor = self.connect.cursor()
        self.connect.autocommit = True


    def drop_table(self):
        self.cursor.execute(
            """DROP TABLE favorite_person;
               DROP TABLE person;
               DROP TABLE find_person;
            
               """
        )


    def create_table(self):
        self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS person(
            person_id SERIAL PRIMARY KEY, 
            vk_id VARCHAR(64) NOT NULL, 
            firstname VARCHAR(64) NOT NULL, 
            lastname VARCHAR(64) NOT NULL, 
            age INT NOT NULL, 
            gender VARCHAR(32) NOT NULL, 
            city VARCHAR (64) NOT NULL);"""
        )

        self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS find_person(
            find_person_id SERIAL PRIMARY KEY,
            vk_id VARCHAR(64) NOT NULL, 
            firstname VARCHAR(64) NOT NULL, 
            lastname VARCHAR(64) NOT NULL, 
            link_found_person TEXT NOT NULL, 
            link_photo TEXT NOT NULL);"""
        )

        self.cursor.execute(
        """CREATE TABLE IF NOT EXISTS favorite_person(
            person_id INT REFERENCES person(person_id), 
            find_person_id INT REFERENCES find_person(find_person_id), 
            CONSTRAINT pk PRIMARY KEY(person_id, find_person_id))"""
            )
        
        return
    
    def add_user(self, user):
        self.cursor.execute(
            """INSERT INTO person(vk_id, firstname, lastname, age, gender, city)
               VALUES(%s,%s ,%s, %s, %s, %s );""", (user['id'], user['first_name'], user['last_name'], user['age'], user['sex'], user['city'])
            )
    
    def find_user_person(self, id_user):
        self.cursor.execute(
        """SELECT *
           FROM person;"""
        )
        all_users = self.cursor.fetchall()
        list_id_users = [i[1] for i in all_users]
        if id_user in list_id_users:
            return True
        else:
            return False
    
    
    def add_favorites(self, id_user, users_favorite):
        self.cursor.execute(
            """SELECT person_id 
               FROM person
               WHERE vk_id=%s;""", (id_user,))
        cl_id = self.cursor.fetchone()[0]

        self.cursor.execute(
        """SELECT *
           FROM find_person;"""
        )
        all_users_favorites = self.cursor.fetchall()
        list_id_users = [i[1] for i in all_users_favorites]
        if users_favorite['id']  not in list_id_users:
            self.cursor.execute(
                """INSERT INTO find_person(vk_id, firstname, lastname, link_found_person, link_photo)
                   VALUES(%s,%s ,%s, %s, %s );""", (users_favorite['id'], users_favorite['first_name'], users_favorite['last_name'], users_favorite['href'], users_favorite['photo'])
                )
        self.cursor.execute(
            """SELECT find_person_id 
               FROM find_person
               WHERE vk_id=%s;""", (users_favorite['id'],))
        find_cl_id = self.cursor.fetchone()[0]

        self.cursor.execute(
            """INSERT INTO favorite_person(person_id, find_person_id)
               VALUES(%s,%s );""", (cl_id, find_cl_id)
            )
        
    def find_all_favorites(self, user_id_vk):

        self.cursor.execute(
            """SELECT link_found_person FROM find_person fp
               LEFT JOIN favorite_person fap ON fap.find_person_id = fp.find_person_id
               LEFT JOIN person p ON p.person_id = fap.person_id
               WHERE p.vk_id =%s;""", (user_id_vk,)

            )
        favorites_users = self.cursor.fetchall()
        return '\n'.join([f'{i}: {favorites_users[i - 1][0]}' for i in range(1, len(favorites_users) + 1)])
