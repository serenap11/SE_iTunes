from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_durata_album(min_duration):
        #seleziona gli album con durata > min_duration
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                   SELECT a.id, a.title, a.artist, SUM(t.milliseconds)/60000 AS durata
                   FROM album a, track t
                   WHERE a.id = t.album_id
                   GROUP BY a.id, a.title, a.artist
                   HAVING durata >= %s
                """
        cursor.execute(query, (min_duration,))
        for row in cursor:
            album = Album(row["id"], row["title"], row["artist"], row["durata"])
            result.append(album)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_playlist(albums):
        conn = DBConnect.get_connection()
        result = {a : set() for a in albums}
        album_ids = tuple(a.id for a in albums)
        if not album_ids:
            return result

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT t.album_id, p.playlist_id
                FROM track t, playlist_track p
                WHERE t.id = p.track_id and t.album_id in {album_ids}
                """
        cursor.execute(query, (album_ids,))
        for row in cursor:
            album = next((a for a in albums if a.id == row["album_id"]), None)
            if album:
                result[album.id].add(row["playlist_id"])
        cursor.close()
        conn.close()
        return result