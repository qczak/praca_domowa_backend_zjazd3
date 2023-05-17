from datetime import datetime
from .models import Measurement


def import_from_csv(file_name: str) -> str:
    with open('data/' + file_name, "r") as f:
        count = 0
        count_errors = 0
        for row in f:
            word = row.split(',', maxsplit=3)
            try:
                reckord = Measurement(value=float(word[0]),
                                      measured_date=datetime.strptime(word[1].strip(), '%Y-%m-%d'),
                                      notes=word[2].strip())
                reckord.save()
                count += 1
            except ValueError:
                print(f'Błąd odczytu danych: "{row.strip()}"  ->  zła wartość.')
                count_errors += 1
            except IndexError:
                print(f'Błąd odczytu danych, w linii: "{row.strip()}"  -> za mało parametrów.')
                count_errors += 1
        f.close()
    return f'Dodano {count} rekrdów z pomiarami. Było {count_errors} błędnych rekordów.'
