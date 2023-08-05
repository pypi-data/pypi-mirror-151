def validate_nric(nric_no):
    weight = (2, 7, 6, 5, 4, 3, 2)  # ()this is tuple and cannot be modified
    alpha_singaporean = ('J', 'Z', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A')
    alpha_foreigner = ('X', 'W', 'U', 'T', 'R', 'Q', 'P', 'N', 'M', 'L', 'K')

    try:
        total_sum = 0
        for i in range(len(weight)):
            current_product = weight[i] * int(nric_no[i + 1])
            total_sum += current_product

        # if 'T' or 'G' total_sum PLUS G1234567
        if (nric_no[0] == 'T') or (nric_no[0] == 'G'):
            total_sum += 4

        remainder = total_sum % 11

        # check if S or F else invalid NRIC
        if (nric_no[0] == 'S') or (nric_no[0] == 'T'):
            print("NRIC Owner is Singaporean")
            # return True
            return (alpha_singaporean[remainder]) == nric_no[8]
        elif (nric_no[0] == 'F') or (nric_no[0] == 'G'):
            print("NRIC Owner is foreigner")
            # return True
            return (alpha_singaporean[remainder]) == nric_no[8]
        else:
            print("Invalid NRIC number")
            return False

    except Exception as e:
        print(str(e))
        return False
