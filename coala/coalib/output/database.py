import sqlite3

def get_connection():
    return sqlite3.connect('database.sqlite')

class StoreException(Exception):
    def __init__(self, message, **errors):
        Exception.__init__(self, message)
        self.errors = errors

# base store class
class Store():
    def __init__(self):
        try:
            self.conn = get_connection()
        except Exception as e:
            raise StoreException(*e.args)
        self._complete = False

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        # can test for type and handle different situations
        self.close()

    def complete(self):
        self._complete = True

    def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise StoreException(*e.args)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise StoreException(*e.args)

class AnalyzerResultStore(Store):
    def __init__(self):        
        try:
            super().__init__()
            c = self.conn.cursor()
            c.execute('''create table if not exists AnalyzerResult
                        (origin text, language text, language_ver text, project_name text, project_version text,
                            source_file_path text, message text, severity integer, diffs text, confidence integer)''')
        except Exception as e:
            raise StoreException('error creating table')

    def addResult(self, result):
        try:
            c = self.conn.cursor()
            c.execute('''insert into AnalyzerResult 
                (origin, language, language_ver, project_name, project_version, source_file_path, message, severity, diffs, confidence)
                VALUES (?,?,?,?,?,?,?,?,?,?)''', 
                (result.origin, result.language, result.language_ver, result.project_name, result.project_version, result.source_file_path, result.message, result.severity, result.diffs, result.confidence,))
        except Exception as e:
                raise StoreException('error storing analyzer result')
