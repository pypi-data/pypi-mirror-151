import okmathutils

"""Package that is useful for math calculations
\nSuch as:
    Square millimeters, centimeters, meters
    And more
"""

#Square

def smm2(a: int):
    """For calculating square millimeters

    Args:
        a (int): One of the square sides

    Returns:
        Integer: Calculated square millimeters in millimeters
    """
    
    return a * a

def scm2(a: int):
    """For calculating square centimeters
    
    Args:
        a (int): One of the square sides

    Returns:
        Integer: Calculated square centimeters in centimeters
    """
    
    return a * a

def sm2(a: int):
    """For calculating square meters
    
    Args:
        a (int): One of the square sides

    Returns:
        Integer: Calculated square meters in meters
    """
    
    return a * a

def smm(a: int):
    """For calculating square perimeter in millimeters
    
    Args:
        a (int): One of the square sides

    Returns:
        Integer: Calculated square perimeter in millimeters
    """
    
    return a * 4

def scm(a: int):
    """For calculating square perimeter in centimeters
    
    Args:
        a (int): One of the square sides

    Returns:
        Integer: Calculated square perimeter in centimeters
    """
    
    return a * 4

def sm(a: int):
    """For calculating square perimeter in meters
    
    Args:
        a (int): One of the square sides

    Returns:
        Integer: Calculated square perimeter in meters
    """
    
    return a * 4

























#Rectangle

def rmm2(a: int, b: int):
    """For calculating rectangle millimeters
    
    Args:
        a (int): Length of the rectangle
        b (int): Width of the rectangle

    Returns:
        Integer: Calculated rectangle millimeters in millimeters
    """
    
    return a * b

def rcm2(a: int, b: int):
    """For calculating rectangle centimeters
    
    Args:
        a (int): Length of the rectangle
        b (int): Width of the rectangle

    Returns:
        Integer: Calculated rectangle centimeters in centimeters
    """
    
    return a * b

def rm2(a: int, b: int):
    """For calculating rectangle meters
    
    Args:
        a (int): Length of the rectangle
        b (int): Width of the rectangle

    Returns:
        Integer: Calculated rectangle meters in meters
    """
    
    return a * b

def rmm(a: int, b: int):
    """For calculating rectangle perimeter in millimeters
    
    Args:
        a (int): Length of the rectangle
        b (int): Width of the rectangle

    Returns:
        Integer: Calculated rectangle perimeter in millimeters
    """
    
    return (a * 2) + (b * 2)

def rcm(a: int, b: int):
    """For calculating rectangle perimeter in centimeters
    
    Args:
        a (int): Length of the rectangle
        b (int): Width of the rectangle

    Returns:
        Integer: Calculated rectangle perimeter in centimeters
    """
    
    return (a * 2) + (b * 2)

def rm(a: int, b: int):
    """For calculating rectangle perimeter in meters
    
    Args:
        a (int): Length of the rectangle
        b (int): Width of the rectangle

    Returns:
        Integer: Calculated rectangle perimeter in meters
    """
    
    return (a * 2) + (b * 2)

















#Triangle

def tmm2(a: int, b: int):
    """For calculating triangle millimeters
    
    Args:
        a (int): Height of the triangle
        b (int): Width of the triangle

    Returns:
        Integer: Calculated triangle millimeters in millimeters
    """
    
    return (a * b) / 2

def tcm2(a: int, b: int):
    """For calculating triangle centimeters
    
    Args:
        a (int): Height of the triangle
        b (int): Width of the triangle

    Returns:
        Integer: Calculated triangle centimeters in centimeters
    """
    
    return (a * b) / 2

def tm2(a: int, b: int):
    """For calculating triangle meters
    
    Args:
        a (int): Height of the triangle
        b (int): Width of the triangle

    Returns:
        Integer: Calculated triangle meters in meters
    """
    
    return (a * b) / 2































#Cube

def cmm3(a: int, b: int, c: int):
    """For calculating cube millimeters
    
    Args:
        a (int): Length
        b (int): Width
        c (int): Height

    Returns:
        Integer: Calculated cube millimeters in millimeters
    """
    
    return a * b * c

def ccm3(a: int, b: int, c: int):
    """For calculating cube centimeters
    
    Args:
        a (int): Length
        b (int): Width
        c (int): Height

    Returns:
        Integer: Calculated cube centimeters in centimeters
    """
    
    return a * b * c

def cm3(a: int, b: int, c: int):
    """For calculating cube meters
    
    Args:
        a (int): Length
        b (int): Width
        c (int): Height

    Returns:
        Integer: Calculated cube meters in meters
    """
    
    return a * b * c









#Rectangle Cuboid

def rcmm3(a: int, b: int, c: int):
    """For calculating rectangle cuboid millimeters
    
    Args:
        a (int): Length
        b (int): Width
        c (int): Height

    Returns:
        Integer: Calculated rectangle cuboid millimeters in millimeters
    """
    
    return a * b * c

def rccm3(a: int, b: int, c: int):
    """For calculating rectangle cuboid centimeters
    
    Args:
        a (int): Length
        b (int): Width
        c (int): Height

    Returns:
        Integer: Calculated rectangle cuboid centimeters in centimeters
    """
    
    return a * b * c

def rcm3(a: int, b: int, c: int):
    """For calculating rectangle cuboid meters
    
    Args:
        a (int): Length
        b (int): Width
        c (int): Height

    Returns:
        Integer: Calculated rectangle cuboid meters in meters
    """
    
    return a * b * c























#Circle

def cimma(a: int):
    """For calculating circle area in millimeters
    
    Args:
        a (int): Radius

    Returns:
        Integer: Calculated circle area in millimeters
    """
    
    return 3.14 * a * a

def cimca(a: int):
    """For calculating circle area in centimeters
    
    Args:
        a (int): Radius

    Returns:
        Integer: Calculated circle area in centimeters
    """
    
    return 3.14 * a * a

def cima(a: int):
    """For calculating circle area in meters
    
    Args:
        a (int): Radius

    Returns:
        Integer: Calculated circle area in meters
    """
    
    return 3.14 * a * a

def cimm(a: int):
    """For calculating circle circumference in millimeters
    
    Args:
        a (int): Radius

    Returns:
        Integer: Calculated circle circumference in millimeters
    """
    
    return 3.14 * a * 2

def cicm(a: int):
    """For calculating circle circumference in centimeters
    
    Args:
        a (int): Radius

    Returns:
        Integer: Calculated circle circumference in centimeters
    """
    
    return 3.14 * a * a

def cim(a: int):
    """For calculating circle circumference in meters
    
    Args:
        a (int): Radius

    Returns:
        Integer: Calculated circle circumference in meters
    """
    
    return 3.14 * a * a






























#Utils

def mm2cm(a: int):
    """For converting millimeters to centimeters
    
    Args:
        a (int): Millimeters

    Returns:
        Integer: Converted millimeters to centimeters
    """
    
    return a / 10

def cm2mm(a: int):
    """For converting centimeters to millimeters
    
    Args:
        a (int): Centimeters

    Returns:
        Integer: Converted centimeters to millimeters
    """
    
    return a * 10

def mm2m(a: int):
    """For converting millimeters to meters
    
    Args:
        a (int): Millimeters

    Returns:
        Integer: Converted millimeters to meters
    """
    
    return a / 1000

def m2mm(a: int):
    """For converting meters to millimeters
    
    Args:
        a (int): Meters

    Returns:
        Integer: Converted meters to millimeters
    """
    
    return a * 1000

def cm2m(a: int):
    """For converting centimeters to meters
    
    Args:
        a (int): Centimeters

    Returns:
        Integer: Converted centimeters to meters
    """
    
    return a / 100

def m2cm(a: int):
    """For converting meters to centimeters
    
    Args:
        a (int): Meters

    Returns:
        Integer: Converted meters to centimeters
    """
    
    return a * 100