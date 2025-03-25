# Inventory-Management-System

## Overview

The Inventory Management System is a Python-based application built with the Tkinter library for the user interface and MySQL for the database backend. It allows users to manage products, sailors, receivers, and generate bills for the sales process.

### Features:
- **Product Management**: Add new products to the inventory with their quantity and price.
- **Sailor Management**: Add sailors who manage the products.
- **Receiver Management**: Add receivers and store their contact details and shipping address.
- **Cart System**: Add products to a cart and generate a bill based on the selected products.
- **Real-time Updates**: The system reflects real-time changes in the available inventory.
- **MySQL Integration**: All data is saved into a MySQL database.

---

## Prerequisites

Before running the application, ensure that you have the following installed:

- **Python 3.x**: Make sure Python 3.x is installed on your machine.
- **Tkinter**: Tkinter is typically included with Python, but you can install it separately if needed.
- **MySQL**: A MySQL server running locally or remotely. You need to set up a database with the required tables.
- **mysql-connector-python**: Python library to interact with MySQL.

### Install mysql-connector-python

```bash
pip install mysql-connector-python
