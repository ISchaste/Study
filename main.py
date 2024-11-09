from fastapi import FastAPI, Body
from datetime import datetime

class Ticket:
    def __init__(self, number, day, month, year, device, problemType, description, client, status):
        self.number = number
        self.startDate = datetime(year, month, day)
        self.endDate = None
        self.device = device
        self.problemType = problemType
        self.description = description
        self.client = client
        self.status = status
        self.master = "не назначен"
        self.comments = []

app = FastAPI()

repo = [
    Ticket(1,24,9,2024,"Сандевистан", "Сломался", "Случайно сломал пополам его", "Ви(ж)", "Выполнено"),
    Ticket(2,24,9,2024,"Сандевистан", "Сломался", "Случайно сломал пополам его", "Ви(ж)", "В ожидании"),
    Ticket(3,24,9,2024,"Сандевистан", "Сломался", "Случайно сломал пополам его", "Ви(ж)", "Выполнено")
]

for o in repo:
    o.endDate = datetime.now()
    o.status = "Выполнено"

isUpdatedStatus = False
message = ""

@app.get("/")
def get_ticket():
        global isUpdatedStatus
        global massage
        if(isUpdatedStatus):
            buffer = massage
            isUpdatedStatus = False
            massage = ""
            return repo, buffer
        else:
            return repo

@app.post("/")
def create_ticket(data=Body()):
    ticket = Ticket(
        data["number"],

        data["device"],
        data["problemType"],
        data["description"],
        data["client"],
        data["status"],
    )
    repo.append(ticket)
    return ticket


@app.put("/{number}")
def update_ticket(number, dto = Body()):
    global isUpdatedStatus
    global massage
    isEmpty = True
    for ticket in repo:
        if ticket.number == int(number):
            isEmpty = False
            if (ticket.status != dto["status"]):
                ticket.status = dto["status"]
                isUpdatedStatus = True
                massage += f"Статус заявки номер {ticket.number} изменён\n"
                if ticket.status == "Выполнено":
                    ticket.endDate == datetime.now()
            if (ticket.description != dto["description"]):
                ticket.description = dto["description"]
            if(ticket.master != dto["master"]):
                ticket.master = dto["master"]
            if(dto["comment"] != None):
                ticket.comments.append(dto["comments"])
            return ticket
    if isEmpty:
        return "Такого нету"


@app.get("/{number}")
def ticketn(number: int):
    for ticket in repo:
        if ticket.number == number:
            return ticket


@app.get("/filter/{param}")
def getByNum(param):
    return [o for o in repo if
        o.device == param or
        o.problemType == param or
        o.description == param or
        o.client == param or
        o.status == param or
        o.master == param]

@app.get("/s/problems")
def get_problem_types():
    result = {}
    for o in repo:
        if o.problemType in result: result[o.problemType] += 1
        else: result[o.problemType] = 1
    return result

@app.get("/s/done")
def get_done():
    return len(done())


@app.get("/s/time")
def get_total_time():
    completed_tickets = done()
    times = []
    for o in completed_tickets:
        times.append(o.endDate-o.startDate)
    result = sum([t.days for t in times])/len(completed_tickets)
    return f"{result}"

def done():
    return [o for o in repo if o.status == "Выполнено"]