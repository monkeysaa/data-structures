"""Functions to parse a file containing student data."""


def all_houses(filename):
    """Return a set of all house names in the given file.

    For example:
      >>> unique_houses('cohort_data.txt')
      {"Dumbledore's Army", 'Gryffindor', ..., 'Slytherin'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """

    houses = set()

    with open(filename, 'r') as student_database:
        for line in student_database:
            line = line.rstrip().split('|')
            if line[2] != '':
                houses.add(line[2])

    return houses


def students_by_cohort(filename, cohort='All'):
    """Return a list of students' full names by cohort.

    Names are sorted in alphabetical order. If a cohort isn't
    given, return a list of all students. For example:
      >>> students_by_cohort('cohort_data.txt')
      ['Adrian Pucey', 'Alicia Spinnet', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Fall 2015')
      ['Angelina Johnson', 'Cho Chang', ..., 'Terence Higgs', 'Theodore Nott']

      >>> students_by_cohort('cohort_data.txt', cohort='Winter 2016')
      ['Adrian Pucey', 'Andrew Kirke', ..., 'Roger Davies', 'Susan Bones']

      >>> students_by_cohort('cohort_data.txt', cohort='Spring 2016')
      ['Cormac McLaggen', 'Demelza Robins', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Summer 2016')
      ['Alicia Spinnet', 'Dean Thomas', ..., 'Terry Boot', 'Vincent Crabbe']

    Arguments:
      - filename (str): the path to a data file
      - cohort (str): optional, the name of a cohort

    Return:
      - list[list]: a list of lists
    """

    students = []

    with open(filename, 'r') as student_database:
        for line in student_database:
            line = line.rstrip().split('|')
            name = f"{line[0]} {line[1]}"
            if line[4] == 'G' or line[4] == 'I':
                continue
            elif line[4] == cohort or cohort == 'All':
                students.append(name)

    return sorted(students)


def all_names_by_house(filename):
    """Return a list that contains rosters for all houses, ghosts, instructors.

    Rosters appear in this order:
    - Dumbledore's Army
    - Gryffindor
    - Hufflepuff
    - Ravenclaw
    - Slytherin
    - Ghosts
    - Instructors

    Each roster is a list of names sorted in alphabetical order.

    For example:
      >>> rosters = hogwarts_by_house('cohort_data.txt')
      >>> len(rosters)
      7

      >>> rosters[0]
      ['Alicia Spinnet', ..., 'Theodore Nott']
      >>> rosters[-1]
      ['Filius Flitwick', ..., 'Severus Snape']

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[list]: a list of lists
    """
    all_houses = []  # master list

    # lines 104-110 given
    dumbledores_army = []
    gryffindor = []
    hufflepuff = []
    ravenclaw = []
    slytherin = []
    ghosts = []
    instructors = []

    houses = {"Dumbledore's Army": dumbledores_army, "Gryffindor": gryffindor,
              "Hufflepuff": hufflepuff, "Ravenclaw": ravenclaw,
              "Slytherin": slytherin, "G": ghosts, "I": instructors}

    with open(filename, 'r') as student_database:
        for line in student_database:
            line = line.rstrip().split('|')
            name = f"{line[0]} {line[1]}"
            if line[4] == 'G' or line[4] == 'I':
                house_str = line[4]
            else:
                house_str = line[2]
            # Use houses dict to append name to appropriate house list
            houses[house_str].append(name)

    # Sort each list, then append to all_houses master list
    [all_houses.append(sorted(houses[h])) for h in houses]

    return all_houses


def all_data(filename):
    """Return all the data in a file.

    Each line in the file is a tuple of (full_name, house, advisor, cohort)

    Iterate over the data to create a big list of tuples that individually
    hold all the data for each person. (full_name, house, advisor, cohort)

    For example:
      >>> all_student_data('cohort_data.txt')
      [('Harry Potter', 'Gryffindor', 'McGonagall', 'Fall 2015'), ..., ]

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[tuple]: a list of tuples
    """

    all_data = []

    with open(filename, 'r') as student_database:
        for line in student_database:
            line = line.rstrip().split('|')
            student_data = (f"{line[0]} {line[1]}", line[2], line[3], line[4])
            all_data.append(student_data)

    return all_data


def get_cohort_for(filename, name):
    """Given someone's name, return the cohort they belong to.

    Return None if the person doesn't exist. For example:
      >>> get_cohort_for('cohort_data.txt', 'Harry Potter')
      'Fall 2015'

      >>> get_cohort_for('cohort_data.txt', 'Hannah Abbott')
      'Winter 2016'

      >>> get_cohort_for('cohort_data.txt', 'Balloonicorn')
      None

    Arguments:
      - filename (str): the path to a data file
      - name (str): a person's full name

    Return:
      - str: the person's cohort or None
    """

    with open(filename) as student_database:
        for line in student_database:
            line = line.rstrip().split('|')
            if name == f"{line[0]} {line[1]}":
                return line[4]

    return None


def find_duped_last_names(filename):
    """Return a set of duplicated last names that exist in the data.

    For example:
      >>> find_name_duplicates('cohort_data.txt')
      {'Creevey', 'Weasley', 'Patil'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """
    last_names = set()
    duped_last_names = set()

    with open(filename) as student_database:
        for line in student_database:
            line = line.rstrip().split('|')
            if line[1] in last_names:
                duped_last_names.add(line[1])
            else:
                last_names.add(line[1])

    return duped_last_names


def get_housemates_for(filename, name):
    """Return a set of housemates for the given student.

    Given a student's name, return a list of their housemates. Housemates are
    students who belong to the same house and were in the same cohort as the
    given student.

    For example:
    >>> get_housemates_for('cohort_data.txt', 'Hermione Granger')
    {'Angelina Johnson', ..., 'Seamus Finnigan'}
    """
    housemates = set()
    
    student_list = all_data(filename)

    # 1. Use all_data() to extract house & cohort.
    # all_data returns a list of student tuples (full_name, house, advisor, cohort)
    for student in student_list:
        if name == student[0]:
            cohort = student[3]
            house = student[1]
            break
    
    for student in student_list:
        if student[3] == cohort and student[1] == house:
            housemates.add(student[0])
    
    housemates.remove(name)

    return housemates


##############################################################################
# END OF MAIN EXERCISE.  Yay!  You did it! You Rock!
#
if __name__ == '__main__':
    import doctest

    result = doctest.testfile('doctests.py',
                              report=False,
                              optionflags=(
                                  doctest.REPORT_ONLY_FIRST_FAILURE
                              ))
    doctest.master.summarize(1)
    if result.failed == 0:
        print('ALL TESTS PASSED')
