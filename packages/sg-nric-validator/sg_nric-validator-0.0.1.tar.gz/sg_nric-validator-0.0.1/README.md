# NRIC MY Validator
Python NRIC Singapore validator

Simple Validator just for Singapore NRIC validation

There is only 1 function validate_nric.

validate_nric  will be used to validate Singaporean NRIC , it 
will return true if the Singaporeb NRIC  is input correctly.

You just need call the function as the following:

    
    from sg_nric import validator


    def example():
        number = "S1240535I"
        is_nric_valid = validator.validate_nric(number)
    
        if is_nric_valid:
            print("Is Valid")
        else:
            print("Not Valid NRIC")


#TODO Feature
1. HTML / Javascript validation if for Django
2. SG NRIC generator __*(Unlikely)*__
