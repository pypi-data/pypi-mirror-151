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
    """For calculating square environment in millimeters
    
    Args:
        a (int): One of the square sides

    Returns:
        Integer: Calculated square environment in millimeters
    """
    
    return a * 4

def scm(a: int):
    """For calculating square environment in centimeters
    
    Args:
        a (int): One of the square sides

    Returns:
        Integer: Calculated square environment in centimeters
    """
    
    return a * 4

def sm(a: int):
    """For calculating square environment in meters
    
    Args:
        a (int): One of the square sides

    Returns:
        Integer: Calculated square environment in meters
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
    """For calculating rectangle environment in millimeters
    
    Args:
        a (int): Length of the rectangle
        b (int): Width of the rectangle

    Returns:
        Integer: Calculated rectangle environment in millimeters
    """
    
    return (a * 2) + (b * 2)

def rcm(a: int, b: int):
    """For calculating rectangle environment in centimeters
    
    Args:
        a (int): Length of the rectangle
        b (int): Width of the rectangle

    Returns:
        Integer: Calculated rectangle environment in centimeters
    """
    
    return (a * 2) + (b * 2)

def rm(a: int, b: int):
    """For calculating rectangle environment in meters
    
    Args:
        a (int): Length of the rectangle
        b (int): Width of the rectangle

    Returns:
        Integer: Calculated rectangle environment in meters
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

def tmm(a: int, b: int):
    """For calculating triangle environment in millimeters
    
    Args:
        a (int): Height of the triangle
        b (int): Width of the triangle

    Returns:
        Integer: Calculated triangle environment in millimeters
    """
    
    return a + b

def tcm(a: int, b: int):
    """For calculating triangle environment in centimeters
    
    Args:
        a (int): Height of the triangle
        b (int): Width of the triangle

    Returns:
        Integer: Calculated triangle environment in centimeters
    """
    
    return a + b

def tm(a: int, b: int):
    """For calculating triangle environment in meters
    
    Args:
        a (int): Height of the triangle
        b (int): Width of the triangle

    Returns:
        Integer: Calculated triangle environment in meters
    """
    
    return a + b







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