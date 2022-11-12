from flask import request


def runScheduler() : 
    
    data = request.get_json() 
    doctor_num = data['doctor_num']
    shift_num = data['shift_num']
    days_num = data['days_num']
    doctors_per_shift = data['doctors_per_shift']
    leave_requests = data['leave_requests']
    leave_requests_dict = {}
    for i in leave_requests :
        leave_requests_dict[tuple(i)] = 1
    
    print(doctor_num,shift_num,days_num,doctors_per_shift, leave_requests_dict) # TODO: remove this
    

    return {"message": "Scheduler is running"}, 200 











def getVariablees() -> dict : 

    variables = {}
    return variables 