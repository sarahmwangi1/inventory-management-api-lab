# Inventory Management REST API LAB

## Project Description

This project is a Python-based Inventory Management System built with Flask.

The application provides a REST API that allows users to create, read, update, and delete inventory items. It also integrates with the OpenFoodFacts API to retrieve product information using a barcode.

A command-line interface (CLI) is included to allow users to interact with the inventory system through the terminal.

## Features

- Flask REST API
- Create inventory items
- View all inventory items
- View a single inventory item
- Update inventory items using PATCH
- Delete inventory items
- Inventory item count helper route
- OpenFoodFacts API integration
- Search products by barcode
- Import products from OpenFoodFacts into the inventory
- Command-line interface
- Automated testing with pytest
- Error handling and validation

## Technologies Used

- Python 3
- Flask
- Requests
- Pytest
- OpenFoodFacts API
- Git and GitHub

## Project Structure

inventory-management-api-lab/
│
├── app.py
├── cli.py
├── external_api.py
├── inventory.py
├── test_app.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/

## OpenFoodFacts Integration

The OpenFoodFacts integration retrieves product information by barcode and can import the product into the inventory system.