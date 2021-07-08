from sqlalchemy import Column, String, Integer, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread_=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='your_tasks')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_task(thing, time):
    new_row = Table(task=thing, deadline=time)
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')


def show_task(arg):
    if arg == '1':
        print(datetime.today().strftime('%A %#d %b:'))
        rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        if rows:
            for i, j in enumerate(rows):
                print(f'{i + 1}) {j.task}')
            print()
        else:
            print('Nothing to do!')
            print()
    elif arg == '2':
        for i in range(7):
            check = datetime.today().date() + timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == check).all()
            print(check.strftime('%A %#d %b:'))
            if rows:
                for p, j in enumerate(rows):
                    print(f'{p + 1}) {j.task}')
            else:
                print('Nothing to do!')
            print()
    elif arg == '3':
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            for i, j in enumerate(rows):
                print(f'{i + 1}) {j.task}. {j.deadline.strftime("%#d %b")}')
            print()
        else:
            print('Nothing to do!')
            print()


def up_for_dlt(arg):
    if arg == '4':
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        print('Missed tasks:')
        if rows:
            for i, j in enumerate(rows):
                print(f'{i + 1}) {j.task}. {j.deadline.strftime("%#d %b")}')
            print()
        else:
            print('Nothing is missed!')
            print()
    elif arg == '6':
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            for i, j in enumerate(rows):
                print(f'{i + 1}) {j.task}. {j.deadline.strftime("%#d %b")}')
            dlt = int(input('Choose the number of the task you want to delete:\n'))
            dlt_row = rows[dlt - 1]
            session.delete(dlt_row)
            session.commit()
            print('The task has been deleted!')
            print()
        else:
            print('Nothing to delete')
            print()


def menu():
    print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')


while True:
    menu()
    menu_option = input()
    print()
    if menu_option == '0':
        print('Bye!')
        break
    elif menu_option in ('1', '2', '3'):
        show_task(menu_option)
    elif menu_option == '4':
        up_for_dlt(menu_option)
    elif menu_option == '5':
        add_this = input("Enter task \n")
        do_by = datetime.strptime(input("Enter deadline \n"), '%Y-%m-%d')
        add_task(add_this, do_by)
    elif menu_option == '6':
        up_for_dlt(menu_option)
    else:
        print('Invalid input!')
        print()
