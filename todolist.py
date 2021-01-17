from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task, self.deadline

    def get_weekday_name(self, weekday):
        if weekday == 0:
            return 'Monday'
        elif weekday == 1:
            return 'Tuesday'
        elif weekday == 2:
            return 'Wednesday'
        elif weekday == 3:
            return 'Thursday'
        elif weekday == 4:
            return 'Friday'
        elif weekday == 5:
            return 'Saturday'
        else:
            return 'Sunday'

    def add_task(self):
        new_task = input('\nEnter task:\n')
        new_deadline = input('Enter deadline (YYYY-MM-DD):\n')
        session.add(Table(task=f'{new_task}',
                          deadline=datetime.strptime(new_deadline, '%Y-%m-%d').date()))
        session.commit()
        print('The task has been added!\n')

    def today_task(self):
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        print(f"\nToday {today.day} {today.strftime('%b')}")
        if len(rows) == 0:
            print('Nothing to do!\n')
        else:
            num = 1
            for i in rows:
                print(f'{num}. {i.task}')
                num += 1
            print()

    def week_task(self):
        print('')
        today = datetime.today()
        for i in range(0, 7):
            week = today + timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == week.date()).all()
            print(self.get_weekday_name(week.weekday()) + f" {week.day} {week.strftime('%b')}:")
            if len(rows) == 0:
                print('Nothing to do!')
            else:
                num = 1
                for n in rows:
                    print(f'{num}. {n.task}')
                    num += 1
            print('')

    def missed_task(self):
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        print('\nMissed tasks:')
        num = 1
        if len(rows) == 0:
            print('Nothing is missed!')
        else:
            for i in rows:
                print(f"{num}. {i.task}. {i.deadline.day} {i.deadline.strftime('%b')}")
                num += 1
            print('')

    def all_task(self):
        print('\nAll tasks:')
        num = 1
        rows = session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print('No tasks!')
        else:
            for i in rows:
                print(f"{num}. {i.task}. {i.deadline.day} {i.deadline.strftime('%b')}")
                num += 1
            print('')

    def delete_task(self):
        print('\nChoose the number of the task you want to delete:')
        num = 1
        rows = session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print('No tasks!')
        else:
            for i in rows:
                print(f"{num}. {i.task}. {i.deadline.day} {i.deadline.strftime('%b')}")
                num += 1
            print('')
        choice = int(input("Enter number:\n"))
        session.delete(rows[choice - 1])
        session.commit()
        print('The task has been deleted!\n')

    def start_app(self):
        while True:
            print("1) Today's tasks")
            print("2) Week's tasks")
            print("3) All tasks")
            print('4) Missed tasks')
            print("5) Add task")
            print('6) Delete task')
            print("0) Exit")
            choice = input("\nPlease enter an option number:\n")
            if choice == '1':
                self.today_task()
            elif choice == '2':
                self.week_task()
            elif choice == '3':
                self.all_task()
            elif choice == '4':
                self.missed_task()
            elif choice == '5':
                self.add_task()
            elif choice == '6':
                self.delete_task()
            elif choice == '0':
                print('\nBye!')
                break
            else:
                continue


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
table = Table()
table.start_app()

