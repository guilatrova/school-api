# TDD with Django Rest Framework

Example showing the right way to test a rest API with unit and integration tests. 
We're not using selenium for E2E tests because we should extend this application with a front end to do so.
We're gonna use a school system for this.

I chose to go with a rest API due reusability and scaling.

>*Building RESTful web services, like other programming skills is **part art, part science**. As the Internet industry progresses, creating a REST API becomes more concrete with emerging best practices.*
> -- <cite>**Todd Fredrich, REST API Expert**</cite>

# Bussiness Assumptions

- There are **Teachers**.
- There are **Students**.
- **Students** are in **classes** that **teachers** teach.
- **Teachers** can **assign quizzes** to **students**.
- **Students** solve/answer **questions** to complete the **quiz**, but they don't have to complete it at once. (Partial **submissions** can be made).
- **Quizzes** need to get **graded**.
- For each **teacher**, they can calculate each student's total grade accumulated over a **semester** for their **classes**.

# Extended Assumptions for our API

- We can manage (add, delete, update, retrieve, list) teachers and students
- Quizzes can have as much questions as desired
- All questions should have exactly 4 options
- Questions can repeat
- Answers can't be duplicated (whether by choice or description)
- API will only exposes endpoint to quizzes - questions and choices should be handled through it (like [DDD's aggregate root](https://stackoverflow.com/questions/1958621/whats-an-aggregate-root))
- Users cannot edit submissions nor submit same question twice
- Assignments are automatically graded when all submissions are done
- Grade is calculated by just summing correct answers
- Semester is just a date referencing the start of it

# TDD approach