from flask import request
from ortools.sat.python import cp_model

def runScheduler() : 
    
    data = request.get_json() 
    doctor_num = data['doctor_num']
    shift_num = data['shift_num']
    days_num = data['days_num']
    doctors_per_shift = data['doctors_per_shift']
    leave_requests = data['leave_requests']
    preference_requests = data['preference_requests']
    maxShifts = data['max_shifts']
    leave_requests_formatted = []
    preference_requests_formatted = []

    for i in leave_requests :
        leave_requests_formatted.append(tuple(i))
    for k in preference_requests : 
        preference_requests_formatted.append(tuple(k))
        
    print(doctor_num,shift_num,days_num,doctors_per_shift, leave_requests_formatted, preference_requests_formatted) # TODO: remove this
    
    '''
    setting up the date for the problem. Different problem, different data. 
    '''
    # doctor_num = 10
    # shift_num = 3
    # days_num = 10
    # doctors_per_shift = 2
    leave_requests = leave_requests_formatted
    preference_requests = preference_requests_formatted  

    # sort of an ID for each one. 
    all_doctors = range(doctor_num) 
    all_shifts = range(shift_num) 
    all_days = range(days_num) 

    #create model 
    model = cp_model.CpModel() 

    """
        problem: representing a solution 
        solution: solution is a set of tuples where (n,d,s) = 1 if nth doctor is assigned to sth shift on dth day.
    """

    shifts = {}
    for n in all_doctors :
        for d in all_days :
            for s in all_shifts : 
                shifts[(n,d,s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    """
        Adding constraints 
    """

    #constraint: only the number of doctors specified for a shift

    for d in all_days :
        for s in all_shifts : 
            model.Add(sum(shifts[(n,d,s)] for n in all_doctors) == doctors_per_shift)

    #constraint: include preference requests

    for key in preference_requests :
        model.Add(shifts[key] == 1)

    #constraint: include leave requests

    for key in leave_requests :
        model.Add(shifts[key] == 0)


    #constraint: at most one shift per doctor per day 

    # for n in all_doctors :
    #     for d in all_days : 
    #         model.AddAtMostOne(shifts[(n,d,s)] for s in all_shifts)

    #constraint: at most maxShift number of shifts per day

    for n in all_doctors :
        for d in all_days : 
            model.Add(sum(shifts[(n,d,s)] for s in all_shifts) <= maxShifts)

    #assign shifts evenly. each should have less than maximum and more than minimum, max min values are 

    total_shifts = shift_num*days_num*doctors_per_shift
    minimum_shifts = total_shifts//doctor_num 

    if total_shifts%doctor_num == 0 :
        maximum_shifts = minimum_shifts 
    else :
        maximum_shifts = minimum_shifts + 1 

    for n in range(doctor_num):
        shifts_total = [] 
        for d in all_days :
            for s in all_shifts : 
                shifts_total.append(shifts[(n,d,s)])

        model.Add(minimum_shifts <= sum(shifts_total))
        model.Add(maximum_shifts >= sum(shifts_total))

    print(model.ModelStats() + "\n") 
    solver = cp_model.CpSolver() 
    solver.parameters.linearization_level = 0
    solver.parameters.enumerate_all_solutions = True 


    class doctorsPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Print intermediate solutions."""

        def __init__(self, shifts, num_doctors, num_days, num_shifts, limit):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._shifts = shifts
            self._num_doctors = num_doctors
            self._num_days = num_days
            self._num_shifts = num_shifts
            self._solution_count = 0
            self._solution_limit = limit
            self._solution_output = [] 

        def on_solution_callback(self):
            self._solution_count += 1
            print('Solution %i' % self._solution_count)
            for d in range(self._num_days):
                day_dict = {} 
                print('Day %i' % d)
                for n in range(self._num_doctors):
                    is_working = False
                    for s in range(self._num_shifts):
                        
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            day_dict[s] = day_dict.get(s,[])+[n]
                            
                            print('  doctor %i works shift %i' % (n, s))
                    if not is_working:
                        print('  doctor {} does not work'.format(n))
                
                day_list = [] 
                for i in all_shifts : 
                    day_list.append(day_dict[i])
                self._solution_output.append(day_list)
            if self._solution_count >= self._solution_limit:
                print('Stop search after %i solutions' % self._solution_limit)
                self.StopSearch()

        def solution_count(self):
            return self._solution_count

    # Display the first five solutions.
    solution_limit = 1
    solution_printer = doctorsPartialSolutionPrinter(shifts, doctor_num,
                                                    days_num, shift_num,
                                                    solution_limit)

    solver.Solve(model, solution_printer) 

    if solution_printer._solution_output == [] :
        print("No solutions!")
        return {"message": "no model found"}, 422
    else :
        print(solution_printer._solution_output)
        return {"message": "Scheduler is running", "result": solution_printer._solution_output}, 200

def getVariablees() -> dict : 

    variables = {}
    return variables 