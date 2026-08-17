from fastapi import FastAPI

app = FastAPI()


@app.post("/enrollments", status_code=201)
def create_enrollment():
    pass


@app.get("/students/{student_id}/courses")
def get_student_courses(student_id: int):
    pass
