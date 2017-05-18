

# note im not fully sure if this is all the stuff
class ResultClass():
    def __init__(self,r_start, r_end, r_date,r_cost, max, traversed_segs):
        self.result_start = r_start
        self.result_end = r_end
        self.result_date = r_date
        self.result_cost = r_cost
        self.max_seats = max
        self.traversed_segments = traversed_segs


    result_start = ''
    result_end = ''
    traversed_segments=[] # idk if we need this
    result_date = ''
    result_cost = 0
    max_seats = 0
