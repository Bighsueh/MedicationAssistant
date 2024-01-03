from app.PostgreSQL import PostgreSQLConnector


class MedicationHandler:
    def __init__(self) -> None:
        self.pg_connector = PostgreSQLConnector()
        self.pg_connector.connect()
        pass
    
    def disconnect(self) -> None:
        self.pg_connector.close_connection()
    
    def get_generic_names_by_user_id(self, user_id):
        sql_query = f"""
            SELECT generic_name
            FROM medication_schema.medication_record_detail
            JOIN medication_schema.medication_records ON medication_record_detail.record_id = medication_records.record_id
            WHERE medication_records.user_id = '{user_id}';
        """
        self.pg_connector.execute_query(sql_query)
        result = self.pg_connector.fetch_all()
        return [item[0] for item in result]
    
    def get_side_effect(self, generic_name_list):       
        index:int = 1
        result:str = ""
        
        for generic_name in generic_name_list:
            query_string:str = f"SELECT side_effects FROM medication_schema.drugs_side_effects WHERE drug_name LIKE'%{generic_name}%'"
            
            self.pg_connector.execute_query(query_string)
            query_search = self.pg_connector.fetch_all()

            print(query_search)
            if len(query_search) > 0 :
                result += f"""
                {index}. {query_search}
                """
                index += 1
        
        self.disconnect()
        return result.strip()
    
    def get_side_effect_message_by_user_id(self, user_id):
        generic_name_list = self.get_generic_names_by_user_id(user_id)
        result = self.get_side_effect(generic_name_list)
        return result