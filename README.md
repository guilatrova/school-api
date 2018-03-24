# TDD with Django Rest Framework

Example showing the right way to test a rest API with unit and integration tests.
We're having an API for a school.

# Bussiness Assumptions

- There are **Teachers**.
- There are **Students**.
- **Students** are in **classes** that **teachers** teach.
- **Teachers** can assign **quizzes** to **students**.
- **Students** solve/answer **questions** to complete the **quiz**, but they don't have to complete it at once. (Partial submissions can be made).
- **Quizzes** need to get **graded**.
- For each **teacher**, they can calculate each student's total grade accumulated over a semester for their classes.

# Extended Assumptions for our API

- We can manage (add, delete, update, retrieve, list) any data