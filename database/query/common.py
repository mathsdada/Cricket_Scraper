class Common:
    @staticmethod
    def generate_dict_from_lists(columns, row):
        result = {}
        for key, val in zip(columns, row):
            result[key] = val
        return result

    @staticmethod
    def get_columns(cursor):
        columns = []
        for column in cursor.description:
            columns.append(column.name)
        return columns

    @staticmethod
    def extract_query_results(cursor):
        results = []
        columns = Common.get_columns(cursor)
        for row in cursor.fetchall():
            results.append(Common.generate_dict_from_lists(columns, row))
        return results
