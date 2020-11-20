def checkequalpixel(array, row, col, r):
    value_orig = array[row][col]
    count = 0
    print'+++++++++++++++++++++++++++++++++++++++++'
    print'Original Pixel value: ', value_orig

    try:
        value_right = array[row][col + r]
        print'Right Pixel value: ', value_right
        if value_orig == value_right:
            count = True
            print'Right value equal'
    except:
        print'None right value was found'

    if col - r >= 0:
        value_left = array[row][col - r]
        print'Left Pixel value: ', value_left
        if value_orig == value_left:
            count = True
            print'Left value equal'
    else:
        print'None left value was found'

    if row - r >= 0:
        value_top = array[row - r][col]
        print'Top Pixel value: ', value_top
        if value_orig == value_top:
            count = True
            print'Top value equal'
    else:
        print'None top value was found'

    try:
        value_down = array[row + r][col]
        print'Down Pixel value: ', value_down
        if value_orig == value_down:
            count = True
            print'Down value equal'
    except:
        print'None down value was found'

    if count == True:
        print'Found equal pixel'
    else:
        print'None equal pixel was found'
    print("++++++++++++++++++++++++++++++++++++++++")

    return count


def equal_pixel_prob(array, radius):
    global list_r0_val1
    global list_r0_val2
    list_r0_val1 = []
    list_r0_val2 = []
    all_pixel_img = float(len(array) * len(array[0]))
    print 'Looking for equal values in array/image with radius: {}'.format(radius)

    for r in range(radius + 1):
        print''
        print'---------------------------------'
        print'Start with radius: {}'.format(r)
        print'---------------------------------'
        print''

        if r == 0:

            for i in range(len(array)):
                print'Start with row: {}'.format(i)

                count_val1 = array[i].count(0)
                count_val2 = array[i].count(1)

                list_r0_val1.append(count_val1)
                list_r0_val2.append(count_val2)

            sum_prob_val1 = float(sum(list_r0_val1))
            sum_prob_val2 = float(sum(list_r0_val2))

            prob_val1_final = (sum_prob_val1 / all_pixel_img)
            prob_val2_final = (sum_prob_val2 / all_pixel_img)

            print'Probability that the pixel value without an radius is 0 is: {} or {}%'.format(prob_val1_final, round(prob_val1_final*100))
            print'Probability that the pixel value without an radius is 1 is: {} or {}%'.format(prob_val2_final, round(prob_val2_final*100))

        else:

            count = 0

            for x in range(len(array)):
                print'++++++++++++++++++++++++++++++++++++'
                print 'Start row: {}'.format(x)

                for c in range(len(array[x])):
                    print'Start column: {}'.format(c)
                    if checkequalpixel(array, x, c, r):
                        count = count + 1

            print'----'
            print'Found {} equal pixel with radius {}'.format(count, r)
            probability = float(count)/float(all_pixel_img)
            print'Probability that the pixel value is equal(radius {}): {} or {}%'.format(r, probability, round(probability*100))
            print'----'
            print'Continue with next radius'


equal_pixel_prob([[1, 0, 0, 1, 0, 1, 0],[0, 1, 0, 1, 0, 0, 0],[1, 0, 1, 1, 0, 1, 0],[0, 1, 1, 0, 1, 0, 1],[1, 1, 0, 0, 0, 1, 0],[1, 0, 1, 1, 0, 1, 0],[1, 1, 1, 0, 0, 0, 1]], 5)

array_bessere_ansicht = [

    [1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 0, 0, 0, 1]]

