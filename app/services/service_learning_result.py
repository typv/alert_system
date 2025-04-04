from typing import List, Dict, Optional

class LearningResultsService:
    @staticmethod
    def calculate_credit_warning(current_record: Dict, previous_records: List[Dict]) -> Optional[str]:

        try:
            registered_credits = float(current_record['registered_credits'])
            semester_average = float(current_record['semester_average'])
            cumulative_average = float(current_record['cumulative_average'])
            semester = int(current_record['semester'])
            accumulated_credits = float(current_record['accumulated_credits'])
            
            current_year = (semester + 1) // 2
            
            condition_b = (registered_credits == 0 and semester > 1)
            
            if condition_b:
                return 'Cảnh báo'
            
            condition_c = (
                (semester == 1 and semester_average < 0.8) or  
                (semester > 1 and semester_average < 1.0)      
            )
            
            if current_year == 1:
                min_cumulative_avg = 1.2
            elif current_year == 2:
                min_cumulative_avg = 1.4
            elif current_year == 3:
                min_cumulative_avg = 1.6
            else:
                min_cumulative_avg = 1.8
            
            condition_d = (cumulative_average < min_cumulative_avg)
            

            condition_a = False
            
            if condition_a or condition_b or condition_c or condition_d:
                return 'Cảnh báo'
            
            return None
        except (ValueError, KeyError):
            return None

    @staticmethod
    def process_academic_performance(students: List[Dict]) -> List[Dict]:

        student_records = {}
        for student in students:
            if student['id'] not in student_records:
                student_records[student['id']] = []
            student_records[student['id']].append(student)
        
        processed_students = []
        
        for student_id, records in student_records.items():
            sorted_records = sorted(records, key=lambda x: int(x['semester']))
            
            previous_records = []
            
            for record in sorted_records:
                processed_record = record.copy()
                
                warning = LearningResultsService.calculate_credit_warning(record, previous_records)
                processed_record['academic_processing'] = warning if warning else ""
                
                processed_students.append(processed_record)
                
                previous_records.append(record)
        
        return processed_students