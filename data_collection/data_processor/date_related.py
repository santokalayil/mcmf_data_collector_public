
from datetime import date



def is_under_18(dob):
    now = date.today()
    return now.year - dob.year < 18 \
        or (
                (now.year - dob.year == 18) \
                    and (now.month < dob.month or now.month == dob.month and now.day <= dob.day)
            )



if __name__ == "__main__":
    birth = date(1988,9,29)

    if is_under_18(birth):
        print('Under 18')
    else:
        print('Adult')

