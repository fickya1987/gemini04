import sqlite3

## Connectt to SQlite
connection=sqlite3.connect("guesthouse.db")

# Create a cursor object to insert record,create table

cursor=connection.cursor()

## create the table
table_info="""
Create table Booking(mail VARCHAR(50),start_date Date,
end_date Date, booking_date Date, booking_ID varchar(21));

"""
cursor.execute(table_info)

## Insert Some more records

cursor.execute('''Insert Into Booking values('john@example.com', '2024-01-01', '2024-01-05', '2024-01-15','EC-GuestHouse-123456')''')
cursor.execute('''Insert Into Booking values('jane@example.com', '2024-01-04', '2024-01-07', '2024-02-25','EC-GuestHouse-123458')''')
cursor.execute('''Insert Into Booking values('jim@example.com', '2024-01-21', '2024-01-05', '2024-04-10','EC-GuestHouse-123459')''')
cursor.execute('''Insert Into Booking values('jessica@example.com', '2024-05-01', '2024-05-05', '2024-04-15','EC-GuestHouse-123461')''')
cursor.execute('''Insert Into Booking values('jacob@example.com', '2024-06-10', '2024-06-15', '2024-05-25','EC-GuestHouse-123462')''')

## Disspaly ALl the records

print("The isnerted records are")
data=cursor.execute('''Select * from Booking''')
for row in data:
    print(row)

## Commit your changes int he databse
connection.commit()
connection.close()