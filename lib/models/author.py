from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id = None):
      self.id = id
      self.name = name
    
    def save (self):
       conn = get_connection()
       cursor = conn.cursor()

       if self.id:
          cursor.execute(
             "UPDATE authors SET name = ? WHERE id = ?",
                (self.name, self.id)
          )

       else:
          cursor.execute(
              "INSERT INTO authors (name) VALUES (?)",
                (self.name,)
            )
       self.id = cursor.lastrowid

       conn.commit()
       conn.close()

    def articles(self):
       """Returns all articles by this author"""
       conn = get_connection()
       cursor = conn.cursor()
       cursor.execute(
            "SELECT * FROM articles WHERE author_id = ?",
            (self.id,)
        )
       articles = cursor.fetchall()
       conn.close()
       return articles
    
    def magazines(self):
        """Returns unique magazines this author has written for"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?""",
            (self.id,)
        )
        magazines = cursor.fetchall()
        conn.close()
        return magazines
    
    def add_article(self, title, magazine):
        """Creates and saves a new article for this author"""
        from lib.models.article import Article
        article = Article(title=title, magazine_id=magazine.id, author_id=self.id)
        article.save()
        return article
    
    @classmethod
    def top_author(cls):
        """Returns the author with the most articles"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            GROUP BY authors.id
            ORDER BY article_count DESC
            LIMIT 1"""
        )
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None
    
    @classmethod
    def find_by_id(cls, id):
        """Finds author by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM authors WHERE id = ?",
            (id,)
        )
        row = cursor.fetchone()
        conn.close()
        return cls(**row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
       conn = get_connection()
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
       row = cursor.fetchone()
       conn.close()
       return cls(**row) if row else None


    @classmethod
    def all(cls):
        """Returns all authors"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        authors = [cls(**row) for row in cursor.fetchall()]
        conn.close()
        return authors
    
          