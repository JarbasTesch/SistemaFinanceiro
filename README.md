# Financial and Employee Management System - CRUD Application

This system was developed during my internship at Instituto Beija-Flor to meet the demand for better financial and employee management. It provides the ability to create, read, update, and delete both employees and extra expenses (such as unforeseen costs). 

Additionally, the system can generate a PDF report containing the following details:
- **Current balance:** Total cash available.
- **Total planned expenses:** Total amount to be spent.
- **Remaining balance:** Remaining amount after payments.
- **Employee information:** Name, position, department, and payment details.
- **Extra expenses:** Description of the expense and its value.

The system also includes a **"PAYMENT" button**, which calculates the total expenses, updates the database, clears extra expenses, and starts a new month by retaining only the recurring payments for registered employees.

---

## Features

- Full CRUD operations for employee and expense management.
- Automatic calculation of financial data.
- PDF report generation with comprehensive financial and employee details.
- "Payment" functionality to reset monthly data while retaining employee expenses.

---

## Technologies Used

- **Python**: Core programming language.
- **QtDesigner**: Used to design the user interface.
- **SQLite**: Relational database for storing data.

---

## Personal Note

This was my first project with such complexity and structure, and I’m excited to share it. It was an incredible learning experience, and I hope it can inspire or assist others.
