from database.DB_connect import DBConnect
from model import Albums, Tracks
from model.PlaylistTrack import PlaylistTrack


class DAO():
    @staticmethod
    def getNodi(d):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select a.AlbumId as albumId , a.Title as title , a.ArtistId as artist
                    from(       select a.AlbumId as albumId, sum(t.Milliseconds) as somma
                                from track t, album a
                                where t.AlbumId=a.AlbumId 
                                group by a.AlbumId 
                                )as tt ,
                        album a
                    where a.AlbumId=tt.AlbumId  and somma>%s
                        """
        cursor.execute(query, (d, ))

        for row in cursor:
            result.append(Albums.Album(row["albumId"], row["title"], row["artist"]))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getPlaylistTrack():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from playlisttrack
                        """
        cursor.execute(query)

        for row in cursor:
            result.append(PlaylistTrack.PlaylistTrack(**row))
        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getArchi(dizionarioNodi):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select a1.AlbumId as a1, a2.AlbumId as a2
                    from album a1, album a2, track t1, track t2, playlisttrack pt1, playlisttrack pt2
                    where a1.AlbumId<a2.AlbumId 
                          and a1.AlbumId=t1.AlbumId
                          and a2.AlbumId=t2.AlbumId 
                          and t1.TrackId=pt1.TrackId
                          and t2.TrackId=pt2.TrackId 
                          and pt1.PlaylistId=pt2.PlaylistId"""
        cursor.execute(query)

        for row in cursor:
            if row["a1"] in dizionarioNodi and row["a2"] in dizionarioNodi:
                print(row["a1"], row["a2"])
                result.append((dizionarioNodi[row["a1"]], dizionarioNodi[row["a2"]]))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTrack():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select *
                        from track
                            """
        cursor.execute(query)

        for row in cursor:
            result.append(Tracks.Track(**row))
        cursor.close()
        conn.close()
        return result