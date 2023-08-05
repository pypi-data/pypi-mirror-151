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