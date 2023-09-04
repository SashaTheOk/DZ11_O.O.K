from collections import UserDict
from datetime import datetime
import re

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Некоректний формат номера телефону. Використовуйте '+11-111-111-111'")
        super().__init__(value)

    @staticmethod
    def is_valid_phone(value):
        return re.match(r'^\+\d{2}-\d{3}-\d{3}-\d{3}$', value) is not None

class Birthday(Field):
    def __init__(self, value):
        if not self.is_valid_birthday(value):
            raise ValueError("Некоректний формат дня народження. Використовуйте 'yyyy-mm-dd'")
        super().__init__(value)

    @staticmethod
    def is_valid_birthday(value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [phone] if phone else []
        self._birthday = birthday  # Changed the name to _birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone

    def days_to_birthday(self):
        if self._birthday:
            # формат дати 'yyyy-mm-dd'
            birth_date = datetime.strptime(self._birthday, '%Y-%m-%d').date()
            today = datetime.now().date()
            next_birthday = birth_date.replace(year=today.year)

            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)

            days_until_birthday = (next_birthday - today).days
            return days_until_birthday

    @property
    def birthday(self):
        return self._birthday.value if self._birthday else None

    @birthday.setter
    def birthday(self, value):
        if value is None:
            self._birthday = None
        else:
            if not Birthday.is_valid_birthday(value):
                raise ValueError("Використовуйте 'yyyy-mm-dd'")
            self._birthday = Birthday(value)

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.page_size = 5

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self):
        records = list(self.data.values())
        total_records = len(records)
        current_page = 0

        while current_page * self.page_size < total_records:
            start_index = current_page * self.page_size
            end_index = (current_page + 1) * self.page_size
            yield records[start_index:end_index]
            current_page += 1

if __name__ == "__main__":