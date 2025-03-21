from functools import wraps
from address_book import AddressBook, Record


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except KeyError:
            return "Error: Contact not found."
        except IndexError:
            return "Error: Incorrect number of arguments."

    return inner


def parse_input(user_input: str):
    cmd, *args = user_input.strip().casefold().split()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list, contacts: dict):
    if len(args) < 2:
        raise IndexError

    name, phone = args

    if name not in contacts:
        raise KeyError

    contacts[name] = phone
    return f"Contact {name} updated"


@input_error
def show_phone(args: list, contacts: dict):
    if not len(args) == 1:
        raise IndexError

    name = args[0]

    if name not in contacts:
        raise KeyError

    return f"{name}: {contacts[name]}"


@input_error
def show_all(contacts: dict):
    if not contacts:
        return "No contacts found."

    return "".join(f"\n{name}: {phone}" for name, phone in contacts.items())


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find_record(name)
    if isinstance(record, str):
        return "Contact not found."
    record.add_birthday(birthday)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find_record(name)
    if isinstance(record, str):
        return "Contact not found."
    if not record.birthday:
        return f"No birthday recorded for {name}."
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(_, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the upcoming week."
    return "\n".join(
        [f"{item['name']} - {item['congratulation_date']}" for item in upcoming]
    )


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match (command):
            case "close" | "exit":
                print("Good bye!")
                break
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(show_all(book))
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(birthdays(args, book))
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
