
distance_to_target = lambda x, t: abs(t-x)

list_substraction = lambda x, y: [a - b for a, b in zip(x, y)]
list_addition = lambda x, y: [a + b for a, b in zip(x, y)]
absolute_list = lambda l: [abs(e) for e in l]
relative_list = lambda l,w: [e/w for e in l]
inverse_list = lambda l: [1-e for e in l]


def rollinger_difference(source_rgb, target_rgb):
    """Returns the elementwise substraction of target-source"""
    return list_substraction(target_rgb,source_rgb)

def rollinger_absolute_difference(source_rgb, target_rgb):
    """Returns the absolute elementwise substraction of target-source"""
    return absolute_list(list_substraction(target_rgb,source_rgb))

def rollinger_relative_difference(source_rgb, target_rgb, weight=256):
    """Returns the elementwise absolute fraction of target-source given a weight"""
    return inverse_list(relative_list(rollinger_absolute_difference(target_rgb,source_rgb), weight))

def rollinger_absolute_distance(source_rgb, target_rgb):
    """
    Returns the number of RGB value shifts needed for the source pixel to be equal to the target pixel.
    Similar to the Levensthein Distance for text.
    Contains the absolute sum of distance between RGB values of the source and the target
    """
    return sum(rollinger_absolute_difference(source_rgb, target_rgb))

def rollinger_relative_distance(source_rgb, target_rgb, weight=256):
    """Like absolute distance, but returns the average of RGB values as a fraction of the value range 0..255
    0.0 complete mismatch
    1.0 identical
    """
    difference = sum(rollinger_relative_difference(target_rgb, source_rgb, weight))
    return difference/len(source_rgb)

def rollinger_difference_target_range(source_rgb, target_rgb_range):
    """Similar to rollinger_distance, but the target rgb is a triple range
    ((Rmin,Rmax),(Gmin,Gmax),(Bmin,Bmax))
    distance is calculated until entering the target range
    """
    def distance_to_target_range(x, rmin, rmax):
        if x < rmin:
            return rmin - x
        elif x > rmax:
            return rmax - x
        else:
            return 0
    dR = distance_to_target_range(source_rgb[0],target_rgb_range[0][0],target_rgb_range[0][1])
    dG = distance_to_target_range(source_rgb[1],target_rgb_range[1][0],target_rgb_range[1][1])
    dB = distance_to_target_range(source_rgb[2],target_rgb_range[2][0],target_rgb_range[2][1])
    return (dR,dG,dB)

def rollinger_absolute_difference_target_range(source_rgb, target_rgb_range):
    """Returns the absolute elementwise substraction of target-source"""
    return absolute_list(rollinger_difference_target_range(source_rgb, target_rgb_range))

def rollinger_relative_difference_target_range(source_rgb, target_rgb_range, weight=256):
    """Returns the elementwise absolute fraction of target-source given a weight"""
    return inverse_list(relative_list(rollinger_absolute_difference_target_range(source_rgb, target_rgb_range),weight))

def rollinger_absolute_distance_target_range(source_rgb, target_rgb_range):
    return sum(rollinger_absolute_difference_target_range(source_rgb,target_rgb_range))

def rollinger_relative_distance_target_range(source_rgb, target_rgb, weight=256):
    difference = sum(rollinger_relative_difference_target_range(source_rgb, target_rgb_range))
    return difference/len(source_rgb)

if __name__ == "__main__":
    source = (52,65,127)
    target = (11,45,159)
    print(rollinger_difference(source,target))
    print(rollinger_absolute_difference(source,target))
    print(rollinger_relative_difference(source,target))

    print(rollinger_absolute_distance(source,target))
    print(rollinger_relative_distance(source,target))

    target_rgb_range = ((5,17),(41,67),(128,166))
    print(rollinger_difference_target_range(source, target_rgb_range)) # (-35,0,1)
    print(rollinger_absolute_difference_target_range(source, target_rgb_range))
    print(rollinger_relative_difference_target_range(source, target_rgb_range))

    print(rollinger_absolute_distance_target_range(source, target_rgb_range))
    print(rollinger_relative_distance_target_range(source, target_rgb_range))